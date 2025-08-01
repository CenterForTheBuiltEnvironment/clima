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


class PageUrls(str, Enum):
    """
    Stores application routes.
    Inheriting from `str` allows the enum members to be used as strings directly.
    """

    SELECT: str = "/"
    SUMMARY: str = "/summary"
    T_RH: str = "/t-rh"
    SUN: str = "/sun"
    WIND: str = "/wind"
    PSY_CHART: str = "/psy-chart"
    NATURAL_VENTILATION: str = "/natural-ventilation"
    OUTDOOR: str = "/outdoor"
    EXPLORER: str = "/explorer"
    CHANGELOG: str = "/changelog"
    NOT_FOUND: str = "/404"


class FilePaths:
    """Stores file paths used in the application."""

    CHANGELOG = "CHANGELOG.md"


class Assets:
    """Stores paths to assets."""

    NOT_FOUND_ANIMATION = "/assets/animations/page_not_found.json"


# You can also store other constants or settings here
DEFAULT_UNITS = "si"
