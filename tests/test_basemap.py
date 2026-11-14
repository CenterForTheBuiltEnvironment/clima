from pages.lib.basemap import CARTO_STYLE_URL, add_key, build_keyed_style

TILES = "https://tiles.basemaps.cartocdn.com/v/1/vectortiles/carto.streets/v2/{z}/{x}/{y}.mvt"


def fake_fetch(responses):
    """Return a fetch stub that serves canned JSON by URL (ignoring the query)."""

    def fetch(url):
        return responses[url.split("?")[0]]

    return fetch


def style(**sources):
    return {
        "sprite": "https://tiles.basemaps.cartocdn.com/v/1/gl/positron-gl-style/sprite",
        "glyphs": "https://tiles.basemaps.cartocdn.com/v/1/fonts/{fontstack}/{range}.pbf",
        "sources": sources,
        "layers": [],
    }


def test_add_key_keeps_placeholders_and_skips_other_hosts():
    assert add_key(TILES, "K") == TILES + "?key=K"
    assert add_key("https://example.com/a.json", "K") == "https://example.com/a.json"
    assert add_key(TILES, "") == TILES


def test_key_added_to_sprite_glyphs_and_tiles():
    fetch = fake_fetch({CARTO_STYLE_URL: style(streets={"tiles": [TILES]})})
    result = build_keyed_style("K", fetch)

    assert result["sprite"].endswith("/sprite?key=K")
    assert result["glyphs"].endswith("/{fontstack}/{range}.pbf?key=K")
    assert result["sources"]["streets"]["tiles"] == [TILES + "?key=K"]


def test_tilejson_source_is_inlined_with_key():
    tilejson_url = "https://tiles.basemaps.cartocdn.com/tiles.json"
    fetch = fake_fetch(
        {
            CARTO_STYLE_URL: style(streets={"type": "vector", "url": tilejson_url}),
            tilejson_url: {"tiles": [TILES], "maxzoom": 14},
        }
    )
    source = build_keyed_style("K", fetch)["sources"]["streets"]

    assert "url" not in source
    assert source["tiles"] == [TILES + "?key=K"]
    assert source["maxzoom"] == 14


def test_no_key_returns_style_unchanged():
    original = style(streets={"tiles": [TILES]})
    fetch = fake_fetch({CARTO_STYLE_URL: original})

    assert build_keyed_style("", fetch) == style(streets={"tiles": [TILES]})
