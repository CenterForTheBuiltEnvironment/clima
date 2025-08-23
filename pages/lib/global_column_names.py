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
    ENABLE_CONDENSATION = "enable-condensation"
    ID_EXPLORER_DF_STORE = "df-store"
    ID_EXPLORER_META_STORE = "meta-store"
    ID_NATURAL_DF_STORE = "df-store"
    ID_NATURAL_GLOBAL_LOCAL_RADIO_INPUT = "global-local-radio-input"
    DROPDOWN = "dropdown"
    CUSTOM_SUMMARY = "custom-summary"
    CUSTOM_HEATMAP = "custom-heatmap"
    GLOBAL_LOCAL_RADIO_INPUT = "global-local-radio-input"
    HEATMAP = "heatmap"
    MAIN_NV_SECTION = "main-nv-section"
    ID_NATURAL_META_STORE = "meta-store"
    NORMALIZE = "normalize"
    NV_BAR_CHART = "nv-bar-chart"
    NV_DBT_FILTER = "nv-dbt-filter"
    NV_DPT_FILTER = "nv-dpt-filter"
    NV_DPT_MAX_VAL = "nv-dpt-max-val"
    NV_TDB_MIN_VAL = "nv-tdb-min-val"
    NV_TDB_MAX_VAL = "nv-tdb-max-val"
    NV_HEATMAP_CHART = "nv-heatmap-chart"
    HOUR_SLIDER = "outdoor-comfort-hour-slider"
    NV_MONTH_HOUR_FILTER = "nv-month-hour-filter"
    NV_MONTH_SLIDER = "nv-month-slider"
    IMAGE_SELECTION = "image-selection"
    INVERT_HOUR = "invert-hour-outdoor-comfort"
    INVERT_MONTH = "invert-month-outdoor-comfort"
    INVERT_MONTH_NV = "invert-month-nv"
    ID_EXPLORER_GLOBAL_LOCAL_RADIO_INPUT = "global-local-radio-input"
    INVERT_HOUR_EXPLORE_DESCRIPTIVE = "invert-hour-explore-descriptive"
    INVERT_MONTH_EXPLORE_DESCRIPTIVE = "invert-month-explore-descriptive"
    INVERT_MONTH_EXPLORE_HEATMAP = "invert-month-explore-heatmap"
    INVERT_HOUR_EXPLORE_HEATMAP = "invert-hour-explore-heatmap"
    INVERT_MONTH_EXPLORE_MORE_CHARTS = "invert-month-explore-more-charts"
    INVERT_HOUR_EXPLORE_MORE_CHARTS = "invert-hour-explore-more-charts"
    INVERT_HOUR_NV = "invert-hour-nv"
    ID_EXPLORER_SI_IP_UNIT_STORE = "si-ip-unit-store"
    ID_NATURAL_SI_IP_UNIT_STORE = "si-ip-unit-store"
    META_STORE = "meta-store"
    MONTH_SLIDER = "outdoor-comfort-month-slider"
    NORMALIZE_SWITCH = "outdoor-comfort-switches-input"
    NV_HOUR_SLIDER = "nv-hour-slider"
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
    SEC1_HOUR_SLIDER = "sec1-hour-slider"
    SEC1_MONTH_SLIDER = "sec1-month-slider"
    SEC1_TIME_FILTER_INPUT = "sec1-time-filter-input"
    SEC1_VAR_DROPDOWN = "sec1-var-dropdown"
    SEC2_DATA_FILTER_INPUT = "sec2-data-filter-input"
    SEC2_DATA_FILTER_VAR = "sec2-data-filter-var"
    SEC2_VAR_DROPDOWN = "sec2-var-dropdown"
    SEC2_HOUR_SLIDER = "sec2-hour-slider"
    SEC2_TIME_FILTER_INPUT = "sec2-time-filter-input"
    SEC2_MONTH_SLIDER = "sec2-month-slider"
    SEC2_MIN_VAL = "sec2-min-val"
    SEC2_MAX_VAL = "sec2-max-val"
    SCENARIO_DROPDOWN = "tab7-dropdown"
    SI_IP_UNIT_STORE = "si-ip-unit-store"
    SWITCHES_INPUT = "switches-input"
    TABLE_TMP_HUM = "table-tmp-hum"
    TABLE_DATA_EXPLORER = "table-data-explorer"
    TAB6_SEC2_CONTAINER = "tab6-sec2-container"
    TAB6_SEC3_DATA_FILTER_INPUT = "tab6-sec3-data-filter-input"
    TAB6_SEC3_FILTER_VAR_DROPDOWN = "tab6-sec3-filter-var-dropdown"
    TAB6_SEC3_MIN_VAL = "tab6-sec3-min-val"
    TAB6_SEC3_MAX_VAL = "tab6-sec3-max-val"
    TAB6_SEC3_TIME_FILTER_INPUT = "tab6-sec3-time-filter-input"
    TAB6_SEC3_QUERY_HOUR_SLIDER = "tab6-sec3-query-hour-slider"
    TAB6_SEC3_QUERY_MONTH_SLIDER = "tab6-sec3-query-month-slider"
    TAB6_SEC3_VAR_X_DROPDOWN = "tab6-sec3-var-x-dropdown"
    TAB6_SEC3_VAR_Y_DROPDOWN = "tab6-sec3-var-y-dropdown"
    TAB6_SEC3_COLORBY_DROPDOWN = "tab6-sec3-colorby-dropdown"
    TIME_FILTER_BTN = "month-hour-filter-outdoor-comfort"
    TWO_VAR = "two-var"
    THREE_VAR = "three-var"
    QUERY_DAILY = "query-daily"
    QUERY_HEATMAP = "query-heatmap"
    UTCI_CATEGORY_HEATMAP = "utci-category-heatmap"
    UTCI_HEATMAP = "utci-heatmap"
    UTCI_SUMMARY_CHART = "utci-summary-chart"
    YEARLY_CHART = "yearly-chart"
    YEARLY_EXPLORE = "yearly-explore"


class ComponentProperty:
    # ==================== Define common attribute name constants for components ====================
    CHILDREN = "children"
    DATA = "data"
    MODIFIED_TIMESTAMP = "modified_timestamp"
    VALUE = "value"


class Type:
    # ==================== Defines type constants available for UI components ====================
    CIRCLE = "circle"
