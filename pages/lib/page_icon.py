class PageIcon:
    """Page icon mappings - optimized with dictionary."""

    # Page Name to icon Mapping
    _ICON_MAP = {
        "Select Weather File": "tabler:upload",
        "Climate Summary": "tabler:chart-bar",
        "Temperature and Humidity": "tabler:temperature",
        "Sun and Clouds": "tabler:sun",
        "Wind": "tabler:wind",
        "Psychrometric Chart": "tabler:chart-dots",
        "Natural Ventilation": "tabler:windmill",
        "Outdoor Comfort": "tabler:thermometer",
        "Data Explorer": "tabler:database",
        "Changelog": "tabler:history",
    }

    SELECT_WEATHER_FILE = _ICON_MAP["Select Weather File"]
    CLIMATE_SUMMARY = _ICON_MAP["Climate Summary"]
    TEMPERATURE_AND_HUMIDITY = _ICON_MAP["Temperature and Humidity"]
    SUN_AND_CLOUDS = _ICON_MAP["Sun and Clouds"]
    WIND = _ICON_MAP["Wind"]
    PSYCHROMETRIC_CHART = _ICON_MAP["Psychrometric Chart"]
    NATURAL_VENTILATION = _ICON_MAP["Natural Ventilation"]
    OUTDOOR_COMFORT = _ICON_MAP["Outdoor Comfort"]
    DATA_EXPLORER = _ICON_MAP["Data Explorer"]
    CHANGELOG = _ICON_MAP["Changelog"]

    @classmethod
    def get_icon(cls, page_name):
        """Get icon for a page name."""
        return cls._ICON_MAP.get(page_name, "tabler:circle")
