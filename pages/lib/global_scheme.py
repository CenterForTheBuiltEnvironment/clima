import plotly.io as pio
import colorcet as cc
from plotly.colors import sequential as pseq
from pages.lib.global_variables import Variables, VariableInfo

# Colors Dictionary
blue_red_yellow = ["#00b3ff", "#000082", "#ff0000", "#ffff00"]
dry_humid = ["#ffe600", "#00c8ff", "#0000ff"]
sun_colors = [
    "#293a59",
    "#960c2c",
    "#ff0000",
    "#ff7b00",
    "#fffc00",
    "#ffff7b",
    "#ffffff",
]
light_colors = ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"]
bright_colors = ["#730a8c", "#0d0db3", "#0f85be", "#0f85be", "#b11421", "#fdf130"]
wind_speed_color = list(cc.CET_L19)
wind_dir_color = list(pseq.Viridis)
cloud_colors = [
    "#08306b",
    "#7ec9f3",
    "#e6eae9",
]
utci_categories_color = [
    # Let first 10% (0.1) of the values have color rgb(0, 0, 0)
    [0, "#2B2977"],
    [0.0555, "#2B2977"],
    [0.0555, "#38429B"],
    [0.0555 + 0.111 * 1, "#38429B"],
    [0.0555 + 0.111 * 1, "#4253A4"],
    [0.0555 + 0.111 * 2, "#4253A4"],
    [0.0555 + 0.111 * 2, "#4B62AD"],
    [0.0555 + 0.111 * 3, "#4B62AD"],
    [0.0555 + 0.111 * 3, "#68B8E7"],
    [0.0555 + 0.111 * 4, "#68B8E7"],
    [0.0555 + 0.111 * 4, "#53B848"],
    [0.0555 + 0.111 * 5, "#53B848"],
    [0.0555 + 0.111 * 5, "#EE8522"],
    [0.0555 + 0.111 * 6, "#EE8522"],
    [0.0555 + 0.111 * 6, "#EA2C24"],
    [0.0555 + 0.111 * 7, "#EA2C24"],
    [0.0555 + 0.111 * 7, "#B12224"],
    [0.0555 + 0.111 * 8, "#B12224"],
    [0.0555 + 0.111 * 8, "#751613"],
    [1.0, "#751613"],
]

# containers
container_row_center_full = "container-row row-center"
container_col_center_one_of_three = (
    "container-col justify-center one-of-three-container"
)

# Misc
month_lst = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

clima_template = "plotly_white"

pio.templates.default = clima_template
template = clima_template

fig_config = {
    "modeBarButtonsToRemove": [
        "toggleSpikelines",
        "hoverCompareCartesian",
        "select2d",
        "zoom2d",
        "autoScale2d",
        "pan2d",
        "lasso2d",
        "zoomIn2d",
        "zoomOut2d",
        "hoverClosestCartesian",
    ],
    "displaylogo": False,
    "displayModeBar": "hover",
    "toImageButtonOptions": {"format": "svg", "filename": "Clima tool graph"},
}

tight_margins = dict(l=20, r=20, t=33, b=20)

# Units Dictionary
degrees_unit = "\u00b0deg"
temperature_unit = "\u00b0C"
thermal_stress_label = "Thermal stress"

# Dropdown Names
variables_sun_cloud_tab_dropdown = [
    Variables.NONE.col_name,
    Variables.T_WB.col_name,
    Variables.DPT.col_name,
    Variables.DBT.col_name,
    Variables.RH.col_name,
    Variables.P_VAP.col_name,
    Variables.HR.col_name,
    Variables.EXTR_HOR_RAD.col_name,
    Variables.HOR_IR_RAD.col_name,
    Variables.GLOB_HOR_RAD.col_name,
    Variables.DIR_NOR_RAD.col_name,
    Variables.DIF_HOR_RAD.col_name,
    Variables.GLOB_HOR_ILL.col_name,
    Variables.DIR_NOR_ILL.col_name,
    Variables.DIF_HOR_ILL.col_name,
    Variables.ZLUMI.col_name,
    Variables.WIND_DIR.col_name,
    Variables.WIND_SPEED.col_name,
    Variables.TOT_SKY_COVER.col_name,
    Variables.OPAQUE_SKY_COVER.col_name,
    Variables.VIS.col_name,
]
variables_dropdown = [
    Variables.T_WB.col_name,
    Variables.DPT.col_name,
    Variables.DBT.col_name,
    Variables.RH.col_name,
    Variables.P_VAP.col_name,
    Variables.HR.col_name,
    Variables.EXTR_HOR_RAD.col_name,
    Variables.HOR_IR_RAD.col_name,
    Variables.GLOB_HOR_RAD.col_name,
    Variables.DIR_NOR_RAD.col_name,
    Variables.DIF_HOR_RAD.col_name,
    Variables.GLOB_HOR_ILL.col_name,
    Variables.DIR_NOR_ILL.col_name,
    Variables.DIF_HOR_ILL.col_name,
    Variables.ZLUMI.col_name,
    Variables.WIND_DIR.col_name,
    Variables.WIND_SPEED.col_name,
    Variables.TOT_SKY_COVER.col_name,
    Variables.OPAQUE_SKY_COVER.col_name,
    Variables.VIS.col_name,
]
variables_more_variables_dropdown = [
    Variables.UTCI_SUN_WIND.col_name,
    Variables.UTCI_NO_SUN_WIND.col_name,
    Variables.UTCI_SUN_NO_WIND.col_name,
    Variables.UTCI_NO_SUN_NO_WIND.col_name,
    Variables.UTCI_SUN_WIND_CATEGORIES.col_name,
    Variables.UTCI_NOSUN_WIND_CATEGORIES.col_name,
    Variables.UTCI_SUN_NOWIND_CATEGORIES.col_name,
    Variables.UTCI_NOSUN_NOWIND_CATEGORIES.col_name,
    Variables.T_DP.col_name,
    Variables.ELEVATION.col_name,
    Variables.AZIMUTH.col_name,
    Variables.P_SAT.col_name,
]
variables_sun_cloud_tab_explore_dropdown = [
    Variables.EXTR_HOR_RAD.col_name,
    Variables.HOR_IR_RAD.col_name,
    Variables.GLOB_HOR_RAD.col_name,
    Variables.DIR_NOR_RAD.col_name,
    Variables.DIF_HOR_RAD.col_name,
    Variables.GLOB_HOR_ILL.col_name,
    Variables.DIR_NOR_ILL.col_name,
    Variables.DIF_HOR_ILL.col_name,
    Variables.ZLUMI.col_name,
    Variables.OPAQUE_SKY_COVER.col_name,
]
variables_outdoor_dropdown = [
    Variables.UTCI_SUN_WIND.col_name,
    Variables.UTCI_SUN_NO_WIND.col_name,
    Variables.UTCI_NO_SUN_WIND.col_name,
    Variables.UTCI_NO_SUN_NO_WIND.col_name,
]

sun_cloud_tab_dropdown_names = {
    VariableInfo.from_col_name(key).get_name(): key
    for key in variables_sun_cloud_tab_dropdown
}

dropdown_names = {
    VariableInfo.from_col_name(key).get_name(): key for key in variables_dropdown
}

more_variables_dropdown = {
    VariableInfo.from_col_name(key).get_name(): key
    for key in variables_more_variables_dropdown
}

sun_cloud_tab_explore_dropdown_names = {
    VariableInfo.from_col_name(key).get_name(): key
    for key in variables_sun_cloud_tab_explore_dropdown
}

outdoor_dropdown_names = {
    VariableInfo.from_col_name(key).get_name(): key
    for key in variables_outdoor_dropdown
}
