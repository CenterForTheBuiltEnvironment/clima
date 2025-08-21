from enum import Enum
import platform


class AppConfig:
    """Stores application configuration."""

    TITLE = "CBE Clima Tool"
    DEBUG: bool = "macOS" in platform.platform()
    HOST = "0.0.0.0"
    PORT = 8080
    PROCESSES = 1
    THREADED = True


class UnitSystem(str, Enum):
    """Unit systems."""

    SI = "si"
    IP = "ip"


class PageUrls(str, Enum):
    """
    Stores application routes.
    Inheriting from `str` allows the enum members to be used as strings directly.
    """

    SELECT = "/"
    SUMMARY = "/summary"
    T_RH = "/t-rh"
    SUN = "/sun"
    WIND = "/wind"
    PSY_CHART = "/psy-chart"
    NATURAL_VENTILATION = "/natural-ventilation"
    OUTDOOR = "/outdoor"
    EXPLORER = "/explorer"
    CHANGELOG = "/changelog"
    NOT_FOUND = "/404"


class FilePaths:
    """Stores file paths used in the application."""

    CHANGELOG = "CHANGELOG.md"


class Assets:
    """Stores paths to assets."""

    NOT_FOUND_ANIMATION = "/assets/animations/page_not_found.json"


class PageInfo:
    """Stores page names and orders for registration."""

    SELECT_NAME = "Select Weather File"
    SELECT_ORDER = 0
    SUMMARY_NAME = "Climate Summary"
    SUMMARY_ORDER = 1
    TEMP_RH_NAME = "Temperature and Humidity"
    TEMP_RH_ORDER = 2
    SOLAR_RADIATION_NAME = "Solar Radiation"
    SOLAR_RADIATION_ORDER = 3
    SUN_NAME = "Sun and Clouds"
    SUN_ORDER = 4
    WIND_NAME = "Wind"
    WIND_ORDER = 5
    PSYCHROMETRIC_NAME = "Psychrometric Chart"
    PSYCHROMETRIC_ORDER = 6
    NATURAL_VENTILATION_NAME = "Natural Ventilation"
    NATURAL_VENTILATION_ORDER = 7
    UTCI_NAME = "Outdoor Comfort"
    UTCI_ORDER = 8
    EXPLORER_NAME = "Data Explorer"
    EXPLORER_ORDER = 9
    CHANGELOG_NAME = "Changelog"
    CHANGELOG_ORDER = 10
    NOT_FOUND_NAME = "404"


class DocLinks(str, Enum):
    """Stores documentation links."""

    MAIN = "https://cbe-berkeley.gitbook.io/clima"
    TEMP_HUMIDITY_EXPLAINED = "https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/temperature-and-humidity/temperatures-explained"
    SUN_PATH_DIAGRAM = "https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/sun-and-cloud/how-to-read-a-sun-path-diagram"
    WIND_ROSE = "https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/wind/how-to-read-a-wind-rose"
    NATURAL_VENTILATION = "https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/natural-ventilation"
    UTCI_CHART = "https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/outdoor-comfort/utci-explained"
    PSYCHROMETRIC_CHART = "https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/psychrometric-chart"
    CLOUD_COVER = "https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/sun-and-cloud/cloud-coverage"
    CUSTOM_HEATMAP = "https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/sun-and-cloud/customizable-daily-and-hourly-maps"
    DEGREE_DAYS = "https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/tab-summary/degree-days-explained"
    CLIMATE_PROFILES = "https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/tab-summary/climate-profiles-explained"
    SOLAR_RADIATION = "https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/sun-and-cloud/global-and-diffuse-horizontal-solar-radiation"


# You can also store other constants or settings here
DEFAULT_UNITS = UnitSystem.SI
