"""CARTO vector basemap: a copy of the Positron style with our API key on every URL.

CARTO requires the key on every style, tile, glyph and sprite request, but the
published style.json does not carry it. Both maps load the style from our own
route (see app.py), which serves the keyed copy built here.
"""

import functools
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests

from config import AppConfig

CARTO_STYLE_URL = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
# also hard-coded in assets/carto_basemap.js
CARTO_STYLE_ROUTE = "/basemap/positron.json"


def add_key(url: str, key: str) -> str:
    """Append the key to a cartocdn.com URL, keeping {placeholders} intact."""
    if not key or "cartocdn.com" not in urlsplit(url).netloc:
        return url
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query))
    query["key"] = key
    return urlunsplit(parts._replace(query=urlencode(query, safe="{}")))


def _fetch_json(url: str) -> dict:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def build_keyed_style(key: str, fetch=_fetch_json) -> dict:
    """Return the Positron style with the key added to all CARTO URLs."""
    style = fetch(add_key(CARTO_STYLE_URL, key))
    if not key:
        return style

    for name in ("sprite", "glyphs"):
        if isinstance(style.get(name), str):
            style[name] = add_key(style[name], key)

    for source in style.get("sources", {}).values():
        if "url" in source:
            # inline the TileJSON so its tile URLs can carry the key too
            tilejson = fetch(add_key(source.pop("url"), key))
            for field in ("tiles", "minzoom", "maxzoom", "attribution", "bounds"):
                if field in tilejson:
                    source.setdefault(field, tilejson[field])
        if "tiles" in source:
            source["tiles"] = [add_key(tile, key) for tile in source["tiles"]]

    return style


@functools.lru_cache(maxsize=1)
def keyed_style() -> dict:
    """Keyed style, fetched from CARTO once per server process."""
    return build_keyed_style(AppConfig.CARTO_API_KEY)
