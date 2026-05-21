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

URL_RE = re.compile(r'href=[\'"]?([^\'" >]+)')


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


def build():
    features = []

    # EnergyPlus locations (first 2585 to match current behaviour)
    with open(EPW_JSON, encoding="utf-8") as f:
        epw_data = json.load(f)

    for feat in epw_data["features"][:2585]:
        props = feat["properties"]
        lon, lat = feat["geometry"]["coordinates"]
        features.append({
            "type": "Feature",
            "properties": {
                "title": props["title"],
                "url": extract_url(props["epw"]),
                "source": "ep",
            },
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
        })

    # OneBuilding locations — exclude future-climate scenario files (_Future/ in URL)
    df = pd.read_csv(ONE_BUILDING_CSV, compression="gzip")
    df = df[~df["Source"].str.contains("_Future/", na=False)]
    for _, row in df.iterrows():
        features.append({
            "type": "Feature",
            "properties": {
                "title": row["name"],
                "url": extract_url(str(row["Source"])),
                "source": "ob",
                "period": _clean(row.get("period")),
                "elev": _clean(row.get("elevation (m)")),
                "tz": _clean(row.get("time zone (GMT)")),
                "heat99": _clean(row.get("99% Heating DB")),
                "cool1": _clean(row.get("1% Cooling DB ")),
            },
            "geometry": {"type": "Point", "coordinates": [float(row["lon"]), float(row["lat"])]},
        })

    geojson = {"type": "FeatureCollection", "features": features}
    payload = json.dumps(geojson, separators=(",", ":")).encode("utf-8")

    with gzip.open(OUT, "wb", compresslevel=9) as f:
        f.write(payload)

    print(f"Written {len(features)} features → {OUT} ({OUT.stat().st_size / 1024:.0f} KB gzipped)")
    ep = sum(1 for feat in features if feat["properties"]["source"] == "ep")
    ob = sum(1 for feat in features if feat["properties"]["source"] == "ob")
    print(f"  EnergyPlus: {ep}  OneBuilding: {ob}")


if __name__ == "__main__":
    build()
