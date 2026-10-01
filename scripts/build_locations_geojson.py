"""
Build assets/data/locations.geojson.gz from the two source data files.
Run from the repo root: pipenv run python scripts/build_locations_geojson.py
"""

import gzip
import json
import math
import re
import pandas as pd
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EPW_JSON = REPO_ROOT / "assets" / "data" / "epw_location.json"
ONE_BUILDING_CSV = REPO_ROOT / "assets" / "data" / "one_building.csv"
OUT = REPO_ROOT / "assets" / "data" / "locations.geojson.gz"
NAMES_OUT = REPO_ROOT / "assets" / "data" / "location_names.json"

URL_RE = re.compile(r'href=[\'"]?([^\'" >]+)')

# Historical trim size carried over from the old Plotly map's df.head(2585);
# exact original rationale isn't recoverable from history — preserved as-is here
# to avoid an unreviewed dataset-size change bundled into this PR.
MAX_ENERGYPLUS_LOCATIONS = 2585

# OneBuilding filenames look like "<dotted.station.name>.<WMO id>_<edition>.zip",
# e.g. "USA_CA_San.Francisco.Intl.AP.724940_TMYx.2011-2025.zip". This pulls out the
# station id and the edition suffix so duplicate editions of the same station can be
# compared.
STATION_EDITION_RE = re.compile(r"\.(\d{4,7})_(.+)$")

# Editions that encode a human-readable period/vintage directly in their suffix.
_DATED_TMYX_RE = re.compile(r"^TMYx\.(\d{4}-\d{4})$")
_NORMALS_RE = re.compile(r"^US\.Normals\.(\d{4}-\d{4})$")
_CTZ_RE = re.compile(r"^CTZ(\d{4})$")
_CWEC_RE = re.compile(r"^CWEC(\d{4})$")


def extract_url(html: str) -> str:
    m = URL_RE.search(html)
    return m.group(1) if m else ""


def _clean(val, default="N/A"):
    """Return a clean string or default for NaN / None values."""
    try:
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return default
    except TypeError:
        pass
    return str(val).strip() or default


def _station_and_edition(url: str):
    """Split a OneBuilding download URL into (station_id, edition), or (None, None)
    if the filename doesn't match the expected naming convention."""
    stem = re.sub(r"\.zip$", "", url.rsplit("/", 1)[-1], flags=re.IGNORECASE)
    m = STATION_EDITION_RE.search(stem)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def _parse_edition_label(edition: str) -> str:
    """Turn a OneBuilding edition suffix into a human-readable period/vintage label
    for the map tooltip, instead of the raw code (or "N/A" when it's missing)."""
    if edition is None:
        return "N/A"
    if edition == "TMYx":
        return "TMYx (latest)"
    if m := _DATED_TMYX_RE.match(edition):
        return f"TMYx {m.group(1)}"
    if m := _NORMALS_RE.match(edition):
        return f"NOAA Normals {m.group(1)}"
    if m := _CTZ_RE.match(edition):
        return f"CA Title 24 Climate Zone ({m.group(1)} ed.)"
    if m := _CWEC_RE.match(edition):
        return f"CWEC {m.group(1)}"
    if edition in ("TMY3", "TMY"):
        return edition
    # Fallback: humanize an unrecognised edition code rather than hiding it.
    return edition.replace("_", " ").replace(".", " ").strip()


def _drop_undated_tmyx_aliases(rows):
    """OneBuilding's undated "_TMYx.zip" is their own "always latest" alias — it
    duplicates whichever dated "_TMYx.<range>.zip" edition is current for that
    station. Drop the undated row only when a dated sibling is present, so we never
    remove the only entry for a location."""
    stations_with_dated_tmyx = set()
    for row in rows:
        sid, edition = row["_station_id"], row["_edition"]
        if sid and edition and _DATED_TMYX_RE.match(edition):
            stations_with_dated_tmyx.add(sid)

    kept = []
    dropped = 0
    for row in rows:
        sid, edition = row["_station_id"], row["_edition"]
        if sid and edition == "TMYx" and sid in stations_with_dated_tmyx:
            dropped += 1
            continue
        kept.append(row)
    return kept, dropped


def _build_name_index(features):
    """Map station title -> [lon, lat], first occurrence wins. features is already
    sorted by (lat, lon, title) at the call site, so this is deterministic across
    rebuilds. Called before jitter runs, so coordinates are the true station
    location rather than a jittered offset."""
    index = {}
    for feat in features:
        title = feat["properties"]["title"]
        if title and title not in index:
            index[title] = feat["geometry"]["coordinates"]
    return index


def _jitter_duplicates(features, radius_m=150):
    """Spread features that share the exact same coordinates (e.g. an EnergyPlus and
    a OneBuilding entry for the same physical station) radially around their shared
    point, so they remain individually clickable at any zoom level instead of
    permanently overlapping. Offsets are computed in meters and converted to lon/lat
    deltas with a latitude correction, so separation stays visually consistent at any
    latitude (the old Plotly map's fixed "+0.010 degrees" hack this replaces did not
    have that correction, and distorted badly near the poles)."""
    groups = {}
    for feat in features:
        lon, lat = feat["geometry"]["coordinates"]
        groups.setdefault((lon, lat), []).append(feat)

    for (lon, lat), group in groups.items():
        n = len(group)
        if n <= 1:
            continue
        for i, feat in enumerate(group):
            angle = 2 * math.pi * i / n
            dlat = (radius_m / 111_320) * math.sin(angle)
            dlon = (radius_m / (111_320 * math.cos(math.radians(lat)))) * math.cos(
                angle
            )
            feat["geometry"]["coordinates"] = [lon + dlon, lat + dlat]

    return features


def build():
    features = []

    # EnergyPlus locations (first MAX_ENERGYPLUS_LOCATIONS to match current behaviour)
    with open(EPW_JSON, encoding="utf-8") as f:
        epw_data = json.load(f)

    for feat in epw_data["features"][:MAX_ENERGYPLUS_LOCATIONS]:
        props = feat["properties"]
        lon, lat = feat["geometry"]["coordinates"]
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "title": props["title"],
                    "url": extract_url(props["epw"]),
                    "source": "ep",
                },
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
            }
        )

    # OneBuilding locations — exclude future-climate scenario files (_Future/ in URL)
    df = pd.read_csv(ONE_BUILDING_CSV, compression="gzip")
    df = df[~df["Source"].str.contains("_Future/", na=False)]

    ob_rows = []
    for _, row in df.iterrows():
        url = extract_url(str(row["Source"]))
        sid, edition = _station_and_edition(url)
        ob_rows.append(
            {
                "row": row,
                "url": url,
                "_station_id": sid,
                "_edition": edition,
            }
        )

    ob_rows, dropped = _drop_undated_tmyx_aliases(ob_rows)

    for entry in ob_rows:
        row = entry["row"]
        period = _parse_edition_label(entry["_edition"])
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "title": row["name"],
                    "url": entry["url"],
                    "source": "ob",
                    "period": period,
                    "elev": _clean(row.get("elevation (m)")),
                    "tz": _clean(row.get("time zone (GMT)")),
                    "heat99": _clean(row.get("99% Heating DB")),
                    "cool1": _clean(row.get("1% Cooling DB ")),
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(row["lon"]), float(row["lat"])],
                },
            }
        )

    features.sort(
        key=lambda f: (
            f["geometry"]["coordinates"][1],
            f["geometry"]["coordinates"][0],
            f["properties"]["title"],
        )
    )

    name_index = _build_name_index(features)
    with open(NAMES_OUT, "w", encoding="utf-8") as f:
        json.dump(name_index, f, separators=(",", ":"))

    features = _jitter_duplicates(features)

    geojson = {"type": "FeatureCollection", "features": features}
    payload = json.dumps(geojson, separators=(",", ":")).encode("utf-8")

    with gzip.open(OUT, "wb", compresslevel=9) as f:
        f.write(payload)

    print(
        f"Written {len(features)} features → {OUT} ({OUT.stat().st_size / 1024:.0f} KB gzipped)"
    )
    ep = sum(1 for feat in features if feat["properties"]["source"] == "ep")
    ob = sum(1 for feat in features if feat["properties"]["source"] == "ob")
    print(f"  EnergyPlus: {ep}  OneBuilding: {ob}")
    print(f"  Dropped {dropped} undated-TMYx alias rows (dated edition already kept)")
    print(
        f"  Name index: {len(name_index)} unique titles → {NAMES_OUT} "
        f"({NAMES_OUT.stat().st_size / 1024:.0f} KB)"
    )


if __name__ == "__main__":
    build()
