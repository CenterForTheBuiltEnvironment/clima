from dataclasses import dataclass
from typing import Optional, List, Any
from config import UnitSystem
import colorcet as cc
from plotly.colors import sequential as pseq

@dataclass
class IP:
    """Metadata for the Imperial Units (IP)"""

    unit: str
    range: List[float]


@dataclass
class VariableInfo:
    """Column metadata: default unit/range/color represent the common display;
    if SI or IP is provided, they will override the default values as needed."""

    col_name: str
    name: Optional[str] = None
    unit: Optional[str] = None
    range: Optional[List[float]] = None
    color: Optional[List[Any]] = None
    IP: Optional[IP] = None

    def get_name(self) -> Optional[str]:
        """Returns the display name of the variable."""
        return self.name

    def get_unit(self, system: str) -> Optional[str]:
        """Returns the unit of the variable based on the specified unit system."""
        if system == UnitSystem.IP and self.IP:
            return self.IP.unit
        return self.unit

    def get_range(self, system: str) -> Optional[List[float]]:
        """Returns the valid value range of the variable based on the specified unit system."""
        if system == UnitSystem.IP and self.IP:
            return self.IP.range
        return self.range

    def get_color(self) -> Optional[List[Any]]:
        """Returns the color settings of the variable, if available."""
        return self.color

    @classmethod
    def from_col_name(cls, col_name: str) -> "VariableInfo":
        """Returns the VariableInfo object by matching the column name."""
        for attr_name in dir(Variables):
            variable = getattr(Variables, attr_name)
            if isinstance(variable, cls) and variable.col_name == col_name:
                return variable
        raise KeyError(f"No VariableInfo found for col_name='{col_name}'")


class Variables:
    # ==================== Basic Variables ====================
    NONE = VariableInfo(col_name="None", name="None", unit="", range=[])

    # ==================== Time Related Variables ====================
    DOY = VariableInfo(
        col_name="DOY", name="Day of the year", unit="days", range=[0, 365]
    )
    DAY = VariableInfo(col_name="day", name="day", unit="", range=[1, 31])
    YEAR = VariableInfo(col_name="year")
    PERIOD = VariableInfo(col_name="period")
    MINUTE = VariableInfo(col_name="minute")
    FAKE_YEAR = VariableInfo(col_name="fake_year")
    MONTH_NAMES = VariableInfo(col_name="month_names")
    UTC_TIME = VariableInfo(col_name="UTC_time")
    MONTH = VariableInfo(col_name="month", name="months", unit="months", range=[1, 12])
    HOUR = VariableInfo(
        col_name="hour",
        name="Hour",
        unit="h",
        range=[1, 24],
        color=[
            "#000000",
            "#355e7e",
            "#6b5c7b",
            "#c06c84",
            "#f8b195",
            "#c92a42",
            "#c92a42",
            "#c92a42",
            "#000000",
        ],
    )

    # ==================== Location Related Variables ====================
    LAT = VariableInfo(col_name="lat")  # Latitude
    LON = VariableInfo(col_name="lon")  # Longitude
    CITY = VariableInfo(col_name="city")
    COUNTRY = VariableInfo(col_name="country")
    TIME_ZONE = VariableInfo(col_name="time_zone")
    SITE_ELEVATION = VariableInfo(col_name="site_elevation")

    # ==================== Basic Meteorological Data ====================
    DBT = VariableInfo(
        col_name="DBT",
        name="Dry bulb temperature",
        unit="°C",
        range=[-40, 50],
        color=["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        IP=IP(unit="°F", range=[-40, 122]),
    )
    DPT = VariableInfo(
        col_name="DPT",
        name="Dew point temperature",
        unit="°C",
        range=[-50, 35],
        color=["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        IP=IP(unit="°F", range=[-58, 95]),
    )
    RH = VariableInfo(
        col_name="RH",
        name="Relative humidity",
        unit="%",
        range=[0, 100],
        color=["#ffe600", "#00c8ff", "#0000ff"],
    )

    P_ATM = VariableInfo(
        col_name="p_atm",
        name="Atmospheric pressure",
        unit="Pa",
        range=[95000, 105000],
        color=[
            "#ffffff",
            "#b2f2ff",
            "#33ddff",
            "#00aaff",
            "#0055ff",
            "#0000ff",
            "#aa00ff",
            "#ff00ff",
            "#cc0000",
            "#ffaa00",
        ],
        IP=IP(unit="Psi", range=[95000 * 0.000145038, 105000 * 0.000145038]),
    )

    # ==================== Radiation Related Variables ====================
    EXTR_HOR_RAD = VariableInfo(
        col_name="extr_hor_rad",
        name="Extraterrestrial horizontal irradiation",
        unit="Wh/m<sup>2</sup>",
        range=[0, 1200],
        color=[
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        IP=IP(unit="Btu/ft<sup>2</sup>", range=[0, 1200 * 0.3169983306]),
    )
    HOR_IR_RAD = VariableInfo(
        col_name="hor_ir_rad",
        name="Horizontal infrared radiation",
        unit="Wh/m<sup>2</sup>",
        range=[0, 500],
        color=[
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        IP=IP(unit="Btu/ft<sup>2</sup>", range=[0, 500 * 0.3169983306]),
    )
    GLOB_HOR_RAD = VariableInfo(
        col_name="glob_hor_rad",
        name="Global horizontal radiation",
        unit="Wh/m<sup>2</sup>",
        range=[0, 1200],
        color=[
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        IP=IP(unit="Btu/ft<sup>2</sup>", range=[0, 1200 * 0.3169983306]),
    )
    DIR_NOR_RAD = VariableInfo(
        col_name="dir_nor_rad",
        name="Direct normal radiation",
        unit="Wh/m<sup>2</sup>",
        range=[0, 1200],
        color=[
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        IP=IP(unit="Btu/ft<sup>2</sup>", range=[0, 1200 * 0.3169983306]),
    )
    DIF_HOR_RAD = VariableInfo(
        col_name="dif_hor_rad",
        name="Diffuse horizontal radiation",
        unit="Wh/m<sup>2</sup>",
        range=[0, 1200],
        color=[
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        IP=IP(unit="Btu/ft<sup>2</sup>", range=[0, 1200 * 0.3169983306]),
    )

    # ==================== Lighting Related Variables ====================
    GLOB_HOR_ILL = VariableInfo(
        col_name="glob_hor_ill",
        name="Global horizontal illuminance",
        unit="lux",
        range=[0, 120000],
        color=["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],
        IP=IP(unit="fc", range=[0, 120000 * 0.0929]),
    )
    DIR_NOR_ILL = VariableInfo(
        col_name="dir_nor_ill",
        name="Direct normal illuminance",
        unit="lux",
        range=[0, 120000],
        color=["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],
        IP=IP(unit="fc", range=[0, 120000 * 0.0929]),
    )
    DIF_HOR_ILL = VariableInfo(
        col_name="dif_hor_ill",
        name="Diffuse horizontal illuminance",
        unit="lux",
        range=[0, 120000],
        color=["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],
        IP=IP(unit="fc", range=[0, 120000 * 0.0929]),
    )

    ZLUMI = VariableInfo(
        col_name="Zlumi",
        name="Zenith luminance",
        unit="cd/m<sup>2</sup>",
        range=[0, 60000],
        color=["#730a8c", "#0d0db3", "#0f85be", "#0f85be", "#b11421", "#fdf130"],
        IP=IP(unit="cd/ft<sup>2</sup>", range=[0, 60000 * 0.0929]),
    )

    # ==================== Wind Related Variables ====================
    WIND_DIR = VariableInfo(
        col_name="wind_dir",
        name="Wind direction",
        unit="°deg",
        range=[0, 360],
        color=list(pseq.Viridis),
    )
    WIND_SPEED = VariableInfo(
        col_name="wind_speed",
        name="Wind speed",
        unit="m/s",
        range=[0, 20],
        color=[cc.CET_L19[int(round(i*(len(cc.CET_L19)-1)/(9)))] for i in range(10)],
        IP=IP(unit="fpm", range=[0, 20 * 196.85039370078738]),
    )

    TOT_SKY_COVER = VariableInfo(
        col_name="tot_sky_cover",
        name="Total sky cover",
        unit="tenths",
        range=[0, 10],
        color=[
            "#08306b",
            "#7ec9f3",
            "#e6eae9",
        ],
    )
    OPAQUE_SKY_COVER = VariableInfo(
        col_name="Oskycover",
        name="Opaque sky cover",
        unit="tenths",
        range=[0, 10],
        color=[
            "#08306b",
            "#7ec9f3",
            "#e6eae9",
        ],
    )
    VIS = VariableInfo(
        col_name="Vis",
        name="Visibility",
        unit="km",
        range=[0, 100],
        color=[
            "#08306b",
            "#7ec9f3",
            "#e6eae9",
        ],
        IP=IP(unit="miles", range=[0, 100 * 0.6215]),
    )

    # ==================== Solar Position Related Variables ====================
    APPARENT_ZENITH = VariableInfo(
        col_name="apparent_zenith",
        name="Apparent zenith",
        unit="°deg",
        range=[0, 180],
        color=[
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
    )
    ZENITH = VariableInfo(
        col_name="zenith",
        name="Zenith",
        unit="°deg",
        range=[0, 180],
        color=[
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
    )
    APPARENT_ELEVATION = VariableInfo(
        col_name="apparent_elevation",
        name="Apparent elevation",
        unit="°deg",
        range=[-90, 90],
        color=[
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
    )
    ELEVATION = VariableInfo(
        col_name="elevation",
        name="Elevation",
        unit="°deg",
        range=[-90, 90],
        color=[
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
    )
    AZIMUTH = VariableInfo(
        col_name="azimuth",
        name="Azimuth",
        unit="°deg",
        range=[0, 360],
        color=[
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
    )
    EQUATION_OF_TIME = VariableInfo(
        col_name="equation_of_time",
        name="Equation of time",
        unit="°deg",
        range=[-20, 20],
        color=[
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
    )

    # ==================== UTCI Comfort Related Variables ====================
    UTCI_SUN_WIND = VariableInfo(
        col_name="utci_Sun_Wind",
        name="UTCI: Sun & Wind",
        unit="°C",
        range=[-70, 70],
        color=["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        IP=IP(unit="°F", range=[-94, 158]),
    )
    UTCI_NO_SUN_WIND = VariableInfo(
        col_name="utci_noSun_Wind",
        name="UTCI: no Sun & Wind",
        unit="°C",
        range=[-70, 70],
        color=["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        IP=IP(unit="°F", range=[-94, 158]),
    )
    UTCI_SUN_NO_WIND = VariableInfo(
        col_name="utci_Sun_noWind",
        name="UTCI: Sun & no Wind",
        unit="°C",
        range=[-70, 70],
        color=["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        IP=IP(unit="°F", range=[-94, 158]),
    )
    UTCI_NO_SUN_NO_WIND = VariableInfo(
        col_name="utci_noSun_noWind",
        name="UTCI: no Sun & no Wind",
        unit="°C",
        range=[-70, 70],
        color=["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        IP=IP(unit="°F", range=[-94, 158]),
    )

    UTCI_SUN_WIND_CATEGORIES = VariableInfo(
        col_name="utci_Sun_Wind_categories",
        name="UTCI: Sun & Wind : categories",
        unit="Thermal stress",
        range=[-5, 4],
        color=[
            [0, "#2B2977"],
            [0.0555, "#2B2977"],
            [0.0555, "#38429B"],
            [0.1665, "#38429B"],
            [0.1665, "#4253A4"],
            [0.2775, "#4253A4"],
            [0.2775, "#4B62AD"],
            [0.3885, "#4B62AD"],
            [0.3885, "#68B8E7"],
            [0.4995, "#68B8E7"],
            [0.4995, "#53B848"],
            [0.6105, "#53B848"],
            [0.6105, "#EE8522"],
            [0.7215, "#EE8522"],
            [0.7215, "#EA2C24"],
            [0.8325, "#EA2C24"],
            [0.8325, "#B12224"],
            [0.9435, "#B12224"],
            [0.9435, "#751613"],
            [1.0, "#751613"],
        ],
    )
    UTCI_NOSUN_WIND_CATEGORIES = VariableInfo(
        col_name="utci_noSun_Wind_categories",
        name="UTCI: no Sun & Wind : categories",
        unit="Thermal stress",
        range=[-5, 4],
        color=[
            [0, "#2B2977"],
            [0.0555, "#2B2977"],
            [0.0555, "#38429B"],
            [0.1665, "#38429B"],
            [0.1665, "#4253A4"],
            [0.2775, "#4253A4"],
            [0.2775, "#4B62AD"],
            [0.3885, "#4B62AD"],
            [0.3885, "#68B8E7"],
            [0.4995, "#68B8E7"],
            [0.4995, "#53B848"],
            [0.6105, "#53B848"],
            [0.6105, "#EE8522"],
            [0.7215, "#EE8522"],
            [0.7215, "#EA2C24"],
            [0.8325, "#EA2C24"],
            [0.8325, "#B12224"],
            [0.9435, "#B12224"],
            [0.9435, "#751613"],
            [1.0, "#751613"],
        ],
    )
    UTCI_SUN_NOWIND_CATEGORIES = VariableInfo(
        col_name="utci_Sun_noWind_categories",
        name="UTCI: Sun & no Wind : categories",
        unit="Thermal stress",
        range=[-5, 4],
        color=[
            [0, "#2B2977"],
            [0.0555, "#2B2977"],
            [0.0555, "#38429B"],
            [0.1665, "#38429B"],
            [0.1665, "#4253A4"],
            [0.2775, "#4253A4"],
            [0.2775, "#4B62AD"],
            [0.3885, "#4B62AD"],
            [0.3885, "#68B8E7"],
            [0.4995, "#68B8E7"],
            [0.4995, "#53B848"],
            [0.6105, "#53B848"],
            [0.6105, "#EE8522"],
            [0.7215, "#EE8522"],
            [0.7215, "#EA2C24"],
            [0.8325, "#EA2C24"],
            [0.8325, "#B12224"],
            [0.9435, "#B12224"],
            [0.9435, "#751613"],
            [1.0, "#751613"],
        ],
    )
    UTCI_NOSUN_NOWIND_CATEGORIES = VariableInfo(
        col_name="utci_noSun_noWind_categories",
        name="UTCI: no Sun & no Wind : categories",
        unit="Thermal stress",
        range=[-5, 4],
        color=[
            [0, "#2B2977"],
            [0.0555, "#2B2977"],
            [0.0555, "#38429B"],
            [0.1665, "#38429B"],
            [0.1665, "#4253A4"],
            [0.2775, "#4253A4"],
            [0.2775, "#4B62AD"],
            [0.3885, "#4B62AD"],
            [0.3885, "#68B8E7"],
            [0.4995, "#68B8E7"],
            [0.4995, "#53B848"],
            [0.6105, "#53B848"],
            [0.6105, "#EE8522"],
            [0.7215, "#EE8522"],
            [0.7215, "#EA2C24"],
            [0.8325, "#EA2C24"],
            [0.8325, "#B12224"],
            [0.9435, "#B12224"],
            [0.9435, "#751613"],
            [1.0, "#751613"],
        ],
    )

    # ==================== Additional Meteorological Data ====================
    P_VAP = VariableInfo(
        col_name="p_vap",
        name="Vapor partial pressure",
        unit="Pa",
        range=[0, 5000],
        color=["#ffe600", "#00c8ff", "#0000ff"],
        IP=IP(unit="Psi", range=[0, 5000 * 0.000145038]),
    )
    P_SAT = VariableInfo(
        col_name="p_sat",
        name="Saturation pressure",
        unit="Pa",
        range=[0, 5000],
        IP=IP(unit="Psi", range=[0, 5000 * 0.000145038]),
    )
    HR = VariableInfo(
        col_name="hr",
        name="Absolute humidity",
        unit="g water/kg dry air",
        range=[0, 0.03 * 1000],
        color=["#ffe600", "#00c8ff", "#0000ff"],
        IP=IP(unit="lb water/klb dry air", range=[0, 0.03 * 1000]),
    )
    T_WB = VariableInfo(
        col_name="t_wb",
        name="Wet bulb temperature",
        unit="°C",
        range=[-40, 50],
        color=["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        IP=IP(unit="°F", range=[-40, 122]),
    )
    T_DP = VariableInfo(
        col_name="t_dp",
        name="Dew point temperature",
        unit="°C",
        range=[-40, 50],
        color=["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        IP=IP(unit="°F", range=[-40, 122]),
    )
    EH = VariableInfo(
        col_name="h",
        name="Enthalpy",
        unit="J/kg dry air",
        range=[0, 110000],
        color=["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        IP=IP(unit="Btu/lb dry air", range=[0, 110000 * 0.000429923]),
    )

    # ==================== Additional Humidity Data ====================
    HI_RH = VariableInfo(col_name="hiRH")
    LO_RH = VariableInfo(col_name="loRH")

    # ==================== Additional Wind Data ====================
    WIND_SPEED_UTCI = VariableInfo(col_name="wind_speed_utci")
    WIND_SPEED_UTCI_0 = VariableInfo(col_name="wind_speed_utci_0")

    # ==================== Additional Weather Data ====================
    CLOUD_HEIGHT = VariableInfo(col_name="Cheight")
    PRECIPITATION_OBSERVATION = VariableInfo(
        col_name="PWobs"
    )  # Precipitation Observation
    PRECIPITATION_CODES = VariableInfo(col_name="PWcodes")  # Precipitation Codes
    PRECIPITATION_WATER = VariableInfo(col_name="Pwater")  # Precipitation Water
    AEROSOL_OPTICAL_DEPTH = VariableInfo(col_name="AsolOptD")  # Aerosol Optical Depth
    SNOW_DEPTH = VariableInfo(col_name="SnowD")  # Snow Depth
    DAILY_SNOW = VariableInfo(col_name="DaySSnow")  # Daily Snow
    MRT = VariableInfo(col_name="MRT")
    DELTA_MRT = VariableInfo(col_name="delta_mrt")

    # ==================== Adaptive Comfort Variables ====================
    ADAPTIVE_COMFORT = VariableInfo(col_name="adaptive_comfort")
    ADAPTIVE_CMF_80_LOW = VariableInfo(col_name="adaptive_cmf_80_low")
    ADAPTIVE_CMF_80_UP = VariableInfo(col_name="adaptive_cmf_80_up")
    ADAPTIVE_CMF_90_LOW = VariableInfo(col_name="adaptive_cmf_90_low")
    ADAPTIVE_CMF_90_UP = VariableInfo(col_name="adaptive_cmf_90_up")
    ADAPTIVE_CMF_RMT = VariableInfo(col_name="adaptive_cmf_rmt")
    NV_ALLOWED = VariableInfo(col_name="nv_allowed")
    TMP_CMF = VariableInfo(col_name="tmp_cmf")
    TMP_CMF_80_LOW = VariableInfo(col_name="tmp_cmf_80_low")
    TMP_CMF_80_UP = VariableInfo(col_name="tmp_cmf_80_up")
    TMP_CMF_90_LOW = VariableInfo(col_name="tmp_cmf_90_low")
    TMP_CMF_90_UP = VariableInfo(col_name="tmp_cmf_90_up")
    CONVERSION_FUNCTION = VariableInfo(col_name="conversion_function")

    # ==================== UI and Display Variables ====================
    COLOR = VariableInfo(col_name="color")
    NAME = VariableInfo(col_name="name")
    RANGE = VariableInfo(col_name="range")
    UNIT = VariableInfo(col_name="unit")
    TWENTY_FOUR_HOUR = VariableInfo(col_name="24h")
    FIVE_MINUTE = VariableInfo(col_name="5min")
    TIMES = VariableInfo(col_name="times")
    PATH = VariableInfo(col_name="path")
    FILE_NAME = VariableInfo(col_name="filename")
    WIND_DIR_BINS = VariableInfo(col_name="WindDir_bins")
    WIND_SPD_BINS = VariableInfo(col_name="WindSpd_bins")
    TO_IMAGE_BUTTON_OPTIONS = VariableInfo(col_name="toImageButtonOptions")
    INVERT = VariableInfo(col_name="invert")
    FEATURES = VariableInfo(col_name="features")
    GEOMETRY_COORDINATES = VariableInfo(col_name="geometry.coordinates")
    PROP_ID = VariableInfo(col_name="prop_id")
