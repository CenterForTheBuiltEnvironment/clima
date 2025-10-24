import plotly.io as pio
import numpy as np
from pages.lib.global_variables import Variables, VariableInfo

WIND_ROSE_BINS = [-1, 0.5, 1.5, 3.3, 5.5, 7.9, 10.7, 13.8, 17.1, 20.7, np.inf]


def _stepped_colorscale_from_bins(bins, colors):
    """
    Build a stepped colorscale from bin edges and colors.

    Args:
        bins: sequence/list of N+1 bin edges (ascending). The last edge may be np.inf.
        colors: sequence/list of N colors, one per interval.

    Returns:
        List of (position, color) tuples for a Plotly colorscale with positions in [0, 1].
    """
    if len(bins) != len(colors) + 1:
        raise ValueError(
            f"Expected {len(colors) + 1} bin edges for {len(colors)} colors, "
            f"got {len(bins)}"
        )

    if any(b2 < b1 for b1, b2 in zip(bins, bins[1:])):
        raise ValueError("bins must be in non-decreasing order")

    finite_edges = [b for b in bins if np.isfinite(b)]
    if not finite_edges:
        raise ValueError("All bin edges are non-finite; cannot build colorscale.")

    vmin, vmax = finite_edges[0], finite_edges[-1]
    span = (vmax - vmin) or 1.0

    cs = []
    for i, c in enumerate(colors):
        left_edge, right_edge = bins[i], bins[i + 1]

        left = 0.0 if not np.isfinite(left_edge) else (left_edge - vmin) / span
        right = 1.0 if not np.isfinite(right_edge) else (right_edge - vmin) / span

        left = max(0.0, min(1.0, float(left)))
        right = max(0.0, min(1.0, float(right)))

        cs.append((left, c))
        cs.append((right, c))

    return cs


wind_speed_colorscale_rose = _stepped_colorscale_from_bins(
    WIND_ROSE_BINS, Variables.WIND_SPEED.color
)

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
