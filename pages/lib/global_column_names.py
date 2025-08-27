from enum import Enum


class ColNames(str, Enum):
    # ==================== Time related column ====================
    YEAR = "year"  # year
    PERIOD = "period"  # period
    MONTH = "month"  # month
    DAY = "day"  # day
    HOUR = "hour"  # hour
    MINUTE = "minute"  # minute

    # ==================== Location related column ====================
    LAT = "lat"  # Latitude
    LON = "lon"  # Longitude
    CITY = "city"  # City
    COUNTRY = "country"  # Country
    TIME_ZONE = "time_zone"  # Time Zone

    # ==================== Meteorological data column ====================
    DBT = "DBT"  # Dry Bulb Temperature
    DPT = "DPT"  # Dew Point Temperature
    RH = "RH"  # Relative Humidity
    HI_RH = "hiRH"  # High Relative Humidity
    LO_RH = "loRH"  # Low Relative Humidity
    HR = "hr"
    P_ATM = "p_atm"  # Atmospheric Pressure

    # ==================== Radiation-related column ====================
    EXTR_HOR_RAD = "extr_hor_rad"  # Extraterrestrial Horizontal Radiation
    HOR_IR_RAD = "hor_ir_rad"  # Horizontal Infrared Radiation
    GLOB_HOR_RAD = "glob_hor_rad"  # Global Horizontal Radiation
    DIR_NOR_RAD = "dir_nor_rad"  # Direct Normal Radiation
    DIF_HOR_RAD = "dif_hor_rad"  # Diffuse Horizontal Radiation

    # ==================== Lighting-related columns ====================
    GLOB_HOR_ILL = "glob_hor_ill"  # Global Horizontal Illuminance
    DIR_NOR_ILL = "dir_nor_ill"  # Direct Normal Illuminance
    DIF_HOR_ILL = "dif_hor_ill"  # Diffuse Horizontal Illuminance

    # ==================== Other columns ====================
    ZLUMI = "Zlumi"  # Luminance
    WIND_DIR = "wind_dir"  # Wind Direction
    WIND_SPEED = "wind_speed"  # Wind Speed
    WIND_SPEED_UTCI = "wind_speed_utci"  # Wind Speed Utci
    WIND_SPEED_UTCI_0 = "wind_speed_utci_0"  # Wind Speed Utci 0
    TOT_SKY_COVER = "tot_sky_cover"  # Total Sky Cover
    OSKYCOVER = "Oskycover"  # Opaque Sky Cover
    VIS = "Vis"  # Visibility
    CHEIGHT = "Cheight"  # Cloud Height
    #     PWobs = "PWobs"  # Precipitation Observation
    #     PWcodes = "PWcodes"  # Precipitation Codes
    #     Pwater = "Pwater"  # Precipitation Water
    #     AsolOptD = "AsolOptD"  # Aerosol Optical Depth
    #     SnowD = "SnowD"  # Snow Depth
    #     DaySSnow = "DaySSnow"  # Daily Snow
    ELEVATION = "elevation"  # Elevation
    APPARENT_ELEVATION = "apparent_elevation"  # Apparent Elevation
    APPARENT_ZENITH = "apparent_zenith"  # Apparent Zenith
    AZIMUTH = "azimuth"  # Azimuth
    MRT = "MRT"
    DELTA_MRT = "delta_mrt"
    UTCI_SUN_WIND = "utci_Sun_Wind"  # Utci Sun Wind
    UTCI_SUN_NO_WIND = "utci_Sun_noWind"  # Utci Sun no Wind
    UTCI_NO_SUN_WIND = "utci_noSun_Wind"  # Utci no Sun Wind
    UTCI_NO_SUN_NO_WIND = "utci_noSun_noWind"  # Utci no Sun no Wind
    UTCI_SUN_WIND_CATEGORIES = "utci_Sun_Wind_categories"  # Utci Sun Wind Categories
    UTCI_SUN_NOWIND_CATEGORIES = "utci_Sun_noWind_categories"  # Utci Sun no Wind Categories
    UTCI_NOSUN_WIND_CATEGORIES = "utci_noSun_Wind_categories"  # Utci no Sun Wind Categories
    UTCI_NOSUN_NOWIND_CATEGORIES = "utci_noSun_noWind_categories"  # Utci no Sun no Wind Categories
    ADAPTIVE_COMFORT = "adaptive_comfort"  # Adaptive comfort
    ADAPTIVE_CMF_80_LOW = "adaptive_cmf_80_low"  # Adaptive comfort 80 low
    ADAPTIVE_CMF_80_UP = "adaptive_cmf_80_up"  # Adaptive comfort 80 up
    ADAPTIVE_CMF_90_LOW = "adaptive_cmf_90_low"  # Adaptive comfort 90 low
    ADAPTIVE_CMF_90_UP = "adaptive_cmf_90_up"  # Adaptive comfort 90 up
    ADAPTIVE_CMF_RMT = "adaptive_cmf_rmt"  # Adaptive comfort rmt
    NV_ALLOWED = "nv_allowed"
    TMP_CMF = "tmp_cmf"
    TMP_CMF_80_LOW = "tmp_cmf_80_low"
    TMP_CMF_80_UP = "tmp_cmf_80_up"
    TMP_CMF_90_LOW = "tmp_cmf_90_low"
    TMP_CMF_90_UP = "tmp_cmf_90_up"
    CONVERSION_FUNCTION = "conversion_function"


    # ==================== Calculation column ====================
    FAKE_YEAR = "fake_year"  # Fake Year
    MONTH_NAMES = "month_names"  # Month names
    UTC_TIME = "UTC_time"  # UTC Time
    DOY = "DOY"  # Day of Year

    COLOR = "color"
    NAME = "name"
    RANGE = "range"
    UNIT = "unit"
    TWENTY_FOUR_HOUR = "24h"
    TIMES = "times"
