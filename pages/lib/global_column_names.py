from enum import Enum


class ColNames(str, Enum):
    # ==================== Time related column ====================
    YEAR = "year"  # year
    MONTH = "month"  # month
    DAY = "day"  # day
    HOUR = "hour"  # hour
    MINUTE = "minute"  # minute

    # ==================== Meteorological data column ====================
    DBT = "DBT"  # Dry Bulb Temperature
    DPT = "DPT"  # Dew Point Temperature
    RH = "RH"  # Relative Humidity
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
    TOT_SKY_COVER = "tot_sky_cover"  # Total Sky Cover
    OSKYCOVER = "Oskycover"  # Opaque Sky Cover
    VIS = "Vis"  # Visibility
    CHEIGHT = "Cheight"  # Cloud Height
    PWobs = "PWobs"  # Precipitation Observation
    PWcodes = "PWcodes"  # Precipitation Codes
    Pwater = "Pwater"  # Precipitation Water
    AsolOptD = "AsolOptD"  # Aerosol Optical Depth
    SnowD = "SnowD"  # Snow Depth
    DaySSnow = "DaySSnow"  # Daily Snow

    # ==================== Calculation column ====================
    FAKE_YEAR = "fake_year"  # Fake Year
    MONTH_NAMES = "month_names"  # Month names
    UTC_TIME = "UTC_time"  # UTC Time
    DOY = "DOY"  # Day of Year


class ElementIds:
    # ==================== Defines the unique ID constant for each element in the front-end page ====================
    BEST_CONDITION_TEXT = "outdoor-comfort-output"
    DAILY = "daily"
    DF_STORE = "df-store"
    DROPDOWN = "dropdown"
    GLOBAL_LOCAL_RADIO_INPUT = "global-local-radio-input"
    HEATMAP = "heatmap"
    HOUR_SLIDER = "outdoor-comfort-hour-slider"
    IMAGE_SELECTION = "image-selection"
    INVERT_HOUR = "invert-hour-outdoor-comfort"
    INVERT_MONTH = "invert-month-outdoor-comfort"
    META_STORE = "meta-store"
    MONTH_SLIDER = "outdoor-comfort-month-slider"
    NORMALIZE_SWITCH = "outdoor-comfort-switches-input"
    PSYCH_CHART = "psych-chart"
    PSY_COLOR_BY_DROPDOWN = "psy-color-by-dropdown"
    PSY_DATA_FILTER_BTN = "data-filter"
    PSY_FILTER_VAR_DROPDOWN = "psy-var-dropdown"
    PSY_HOUR_SLIDER = "psy-hour-slider"
    PSY_INVERT_HOUR = "invert-hour-psy"
    PSY_INVERT_MONTH = "invert-month-psy"
    PSY_MAX_VAL_INPUT = "psy-max-val"
    PSY_MIN_VAL_INPUT = "psy-min-val"
    PSY_MONTH_SLIDER = "psy-month-slider"
    PSY_TIME_FILTER_BTN = "month-hour-filter"
    SCENARIO_DROPDOWN = "tab7-dropdown"
    SI_IP_UNIT_STORE = "si-ip-unit-store"
    TABLE_TMP_HUM = "table-tmp-hum"
    TIME_FILTER_BTN = "month-hour-filter-outdoor-comfort"
    UTCI_CATEGORY_HEATMAP = "utci-category-heatmap"
    UTCI_HEATMAP = "utci-heatmap"
    UTCI_SUMMARY_CHART = "utci-summary-chart"
    YEARLY_CHART = "yearly-chart"



class ComponentProperty:
    # ==================== Define common attribute name constants for components ====================
    CHILDREN = "children"
    DATA = "data"
    MODIFIED_TIMESTAMP = "modified_timestamp"
    VALUE = "value"



class Type:
    # ==================== Defines type constants available for UI components ====================
    CIRCLE = "circle"
