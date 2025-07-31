from enum import Enum


class PageUrls(Enum):
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
    NOT_FOUND: str = '"../assets/animations/page_not_found.json"'
