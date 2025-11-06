from copy import deepcopy
from pages.lib.global_element_ids import ElementIds

import dash
import dash_mantine_components as dmc

from dash import dcc
from dash_extensions.enrich import Output, Input, State, callback

from pages.lib.global_variables import Variables
from pages.lib.global_id_buttons import IdButtons
from pages.lib.global_tab_names import TabNames
from config import PageUrls, DocLinks, PageInfo, UnitSystem
from pages.lib.charts_sun import (
    monthly_solar,
    polar_graph,
    custom_cartesian_solar,
)
from pages.lib.global_scheme import (
    sun_cloud_tab_dropdown_names,
    sun_cloud_tab_explore_dropdown_names,
    dropdown_names,
    tight_margins,
)
from pages.lib.template_graphs import heatmap, barchart, daily_profile
from pages.lib.utils import (
    dropdown,
    generate_chart_name,
    generate_units,
    generate_custom_inputs,
    title_with_link,
)

dash.register_page(
    __name__, name=PageInfo.SUN_NAME, path=PageUrls.SUN.value, order=PageInfo.SUN_ORDER
)


sc_dropdown_names = {
    "None": "None",
    "Frequency": "Frequency",
}
sc_dropdown_names.update(deepcopy(dropdown_names))
sc_dropdown_names.update(deepcopy(sun_cloud_tab_dropdown_names))
sc_dropdown_names.update(deepcopy(sun_cloud_tab_explore_dropdown_names))
# Remove the keys from the dictionary
sc_dropdown_names.pop("Vapor partial pressure", None)
sc_dropdown_names.pop("Absolute humidity", None)
sc_dropdown_names.pop("UTCI: Sun & Wind : categories", None)
sc_dropdown_names.pop("UTCI: no Sun & Wind : categories", None)
sc_dropdown_names.pop("UTCI: Sun & no Wind : categories", None)
sc_dropdown_names.pop("UTCI: no Sun & no Wind : categories", None)


def layout():
    """Contents of tab four."""
    return dmc.Stack(
        p="md",
        id=ElementIds.TAB_FOUR_CONTAINER,
        children=[
            sun_path(),
            dmc.Stack(
                id=ElementIds.STATIC_SECTION,
                w="100%",
            ),
            explore_daily_heatmap(),
        ],
    )


def sun_path():
    """Return the layout for the custom sun path and its dropdowns."""
    return dmc.Stack(
        children=[
            title_with_link(
                text="Sun path chart",
                id_button=IdButtons.SUN_PATH_CHART_LABEL,
                doc_link=DocLinks.SUN_PATH_DIAGRAM,
            ),
            dmc.Group(
                align="center",
                justify="center",
                children=[
                    dmc.Title("View: ", order=5),
                    dropdown(
                        id=ElementIds.CUSTOM_SUN_VIEW_DROPDOWN,
                        options={
                            "Spherical": "polar",
                            "Cartesian": "cartesian",
                        },
                        value="polar",
                    ),
                ],
            ),
            dmc.Group(
                align="center",
                justify="center",
                children=[
                    dmc.Title("Select Variable: ", order=5),
                    dropdown(
                        id=ElementIds.CUSTOM_SUN_VAR_DROPDOWN,
                        options=sc_dropdown_names,
                        value="None",
                    ),
                ],
            ),
            dmc.Skeleton(
                visible=False,
                h=450,
                children=dmc.Center(
                    id=ElementIds.CUSTOM_SUNPATH,
                ),
            ),
        ],
    )


def explore_daily_heatmap():
    """Contents of the bottom part of the tab"""
    return dmc.Stack(
        w="100%",
        children=[
            title_with_link(
                text="Daily charts",
                id_button=IdButtons.DAILY_CHART_LABEL,
                doc_link=DocLinks.CUSTOM_HEATMAP,
            ),
            dmc.Group(
                align="center",
                justify="center",
                children=[
                    dmc.Title("Select variable: ", order=5),
                    dropdown(
                        id=ElementIds.SUN_EXPLORE_DROPDOWN,
                        options=sun_cloud_tab_explore_dropdown_names,
                        value="glob_hor_rad",
                    ),
                ],
            ),
            dmc.Skeleton(
                visible=False,
                h=520,
                children=dmc.Stack(id=ElementIds.SUN_DAILY),
            ),
            dmc.Skeleton(
                visible=False,
                h=520,
                children=dmc.Stack(id=ElementIds.SUN_HEATMAP),
            ),
        ],
    )


@callback(
    Output(ElementIds.STATIC_SECTION, "children"),
    [Input(ElementIds.ID_SUN_SI_IP_RADIO_INPUT, "value")],
)
def update_static_section(si_ip):
    hor_unit = "Wh/m²"
    if si_ip == UnitSystem.IP:
        hor_unit = "Btu/ft²"
    return [
        title_with_link(
            text="Global and Diffuse Horizontal Solar Radiation (" + hor_unit + ")",
            id_button=IdButtons.MONTHLY_CHART_LABEL,
            doc_link=DocLinks.SOLAR_RADIATION,
        ),
        dmc.Skeleton(
            visible=False,
            h=520,
            children=dmc.Stack(id=ElementIds.MONTHLY_SOLAR),
        ),
        title_with_link(
            text="Cloud coverage",
            id_button=IdButtons.CLOUD_CHART_LABEL,
            doc_link=DocLinks.CLOUD_COVER,
        ),
        dmc.Skeleton(
            visible=False,
            h=520,
            children=dmc.Stack(id=ElementIds.CLOUD_COVER),
        ),
    ]


@callback(
    [
        Output(ElementIds.MONTHLY_SOLAR, "children"),
        Output(ElementIds.CLOUD_COVER, "children"),
    ],
    [
        Input(ElementIds.ID_SUN_DF_STORE, "modified_timestamp"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_SUN_DF_STORE, "data"),
        State(ElementIds.ID_SUN_META_STORE, "data"),
        State(ElementIds.ID_SUN_SI_IP_UNIT_STORE, "data"),
    ],
)
def monthly_and_cloud_chart(_, global_filter_data, df, meta, si_ip):
    """Update the contents of tab four. Passing in the polar selection and the general info (df, meta)."""

    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(
            df,
            global_filter_data,
            [
                Variables.GLOB_HOR_RAD.col_name,
                Variables.DIF_HOR_RAD.col_name,
                Variables.TOT_SKY_COVER.col_name,
            ],
        )
        # Don't filter out the filtered rows - keep them for gray display
        # The monthly_solar and barchart functions will handle filtering

    # Sun Radiation - ensure all necessary columns are included
    base_columns = [
        Variables.GLOB_HOR_RAD.col_name,
        Variables.DIF_HOR_RAD.col_name,
        Variables.MONTH.col_name,
        Variables.HOUR.col_name,
        Variables.MONTH_NAMES.col_name,
    ]
    if "_is_filtered" in df.columns:
        base_columns.append("_is_filtered")
    if f"_{Variables.GLOB_HOR_RAD.col_name}_original" in df.columns:
        base_columns.append(f"_{Variables.GLOB_HOR_RAD.col_name}_original")
    if f"_{Variables.DIF_HOR_RAD.col_name}_original" in df.columns:
        base_columns.append(f"_{Variables.DIF_HOR_RAD.col_name}_original")
    monthly = monthly_solar(df[base_columns], si_ip)
    monthly = monthly.update_layout(margin=tight_margins)

    # Cloud Cover - ensure all necessary columns are included
    cloud_base_columns = [
        Variables.TOT_SKY_COVER.col_name,
        Variables.MONTH.col_name,
        Variables.DOY.col_name,
    ]
    if "_is_filtered" in df.columns:
        cloud_base_columns.append("_is_filtered")
    if f"_{Variables.TOT_SKY_COVER.col_name}_original" in df.columns:
        cloud_base_columns.append(f"_{Variables.TOT_SKY_COVER.col_name}_original")
    cover = barchart(
        df[cloud_base_columns],
        Variables.TOT_SKY_COVER.col_name,
        [False],
        [False, "", 3, 7],
        True,
        si_ip,
    )
    cover = cover.update_layout(
        margin=tight_margins,
        title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
    )
    # Remove the hardcoded x-axis update - let barchart handle it dynamically
    units = generate_units(si_ip)
    return dcc.Graph(
        style={"width": "100%", "height": "520px"},
        config=generate_chart_name(
            TabNames.GLOBAL_AND_DIFFUSE_HORIZONTAL_SOLAR_RADIATION, meta, units
        ),
        figure=monthly,
    ), dcc.Graph(
        style={"width": "100%", "height": "520px"},
        config=generate_chart_name(TabNames.CLOUD_COVER, meta, units),
        figure=cover,
    )


@callback(
    Output(ElementIds.CUSTOM_SUNPATH, "children"),
    [
        Input(ElementIds.ID_SUN_DF_STORE, "modified_timestamp"),
        Input(ElementIds.CUSTOM_SUN_VIEW_DROPDOWN, "value"),
        Input(ElementIds.CUSTOM_SUN_VAR_DROPDOWN, "value"),
        Input(ElementIds.ID_SUN_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_SUN_DF_STORE, "data"),
        State(ElementIds.ID_SUN_META_STORE, "data"),
        State(ElementIds.ID_SUN_SI_IP_UNIT_STORE, "data"),
    ],
)
def sun_path_chart(_, view, var, global_local, global_filter_data, df, meta, si_ip):
    """Update the contents of tab four. Passing in the polar selection and the general info (df, meta)."""
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        # For sun path chart, we need to filter all sun position related columns
        target_cols = [
            Variables.GLOB_HOR_RAD.col_name,
            Variables.DIF_HOR_RAD.col_name,
            Variables.APPARENT_ELEVATION.col_name,
            Variables.APPARENT_ZENITH.col_name,
            Variables.AZIMUTH.col_name,
            Variables.ELEVATION.col_name,
            Variables.DAY.col_name,
            Variables.MONTH_NAMES.col_name,
            Variables.HOUR.col_name,
        ]
        # Add the selected variable if it's not "None"
        if var != "None":
            target_cols.append(var)
        df = apply_global_month_hour_filter(df, global_filter_data, target_cols)

    # Ensure all necessary columns are included for filtered data display
    base_columns = [
        Variables.APPARENT_ELEVATION.col_name,
        Variables.APPARENT_ZENITH.col_name,
        Variables.AZIMUTH.col_name,
        Variables.ELEVATION.col_name,
        Variables.DAY.col_name,
        Variables.MONTH_NAMES.col_name,
        Variables.HOUR.col_name,
    ]
    if "_is_filtered" in df.columns:
        base_columns.append("_is_filtered")
    if var != "None" and f"_{var}_original" in df.columns:
        base_columns.append(f"_{var}_original")
    if var != "None":
        base_columns.append(var)

    custom_inputs = "" if var == "None" else f"{var}"
    units = "" if var == "None" else generate_units(si_ip)
    if view == "polar":
        return dcc.Graph(
            style={"maxWidth": "50em", "height": "520px"},
            config=generate_chart_name(
                TabNames.SPHERICAL_SUNPATH, meta, custom_inputs, units
            ),
            figure=polar_graph(df[base_columns], meta, global_local, var, si_ip),
        )
    else:
        return dcc.Graph(
            style={"maxWidth": "50em", "height": "520px"},
            config=generate_chart_name(
                TabNames.CARTESIAN_SUNPATH, meta, custom_inputs, units
            ),
            figure=custom_cartesian_solar(
                df[base_columns], meta, global_local, var, si_ip
            ),
        )


@callback(
    Output(ElementIds.SUN_DAILY, "children"),
    [
        Input(ElementIds.ID_SUN_DF_STORE, "modified_timestamp"),
        Input(ElementIds.SUN_EXPLORE_DROPDOWN, "value"),
        Input(ElementIds.ID_SUN_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_SUN_DF_STORE, "data"),
        State(ElementIds.ID_SUN_META_STORE, "data"),
        State(ElementIds.ID_SUN_SI_IP_UNIT_STORE, "data"),
    ],
)
def daily(_, var, global_local, global_filter_data, df, meta, si_ip):
    """Update the contents of tab four section two. Passing in the general info (df, meta)."""
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(df, global_filter_data, var)

    custom_inputs = generate_custom_inputs(var)
    units = generate_units(si_ip)
    return dcc.Graph(
        style={"width": "100%", "height": "520px"},
        config=generate_chart_name(TabNames.DAILY, meta, custom_inputs, units),
        figure=daily_profile(df, var, global_local, si_ip),
    )


@callback(
    Output(ElementIds.SUN_HEATMAP, "children"),
    [
        Input(ElementIds.ID_SUN_DF_STORE, "modified_timestamp"),
        Input(ElementIds.SUN_EXPLORE_DROPDOWN, "value"),
        Input(ElementIds.ID_SUN_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_SUN_DF_STORE, "data"),
        State(ElementIds.ID_SUN_META_STORE, "data"),
        State(ElementIds.ID_SUN_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_heatmap(_, var, global_local, global_filter_data, df, meta, si_ip):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(df, global_filter_data, var)

    custom_inputs = generate_custom_inputs(var)
    units = generate_units(si_ip)
    return dcc.Graph(
        style={"width": "100%", "height": "520px"},
        config=generate_chart_name(TabNames.HEATMAP, meta, custom_inputs, units),
        figure=heatmap(df, var, global_local, si_ip),
    )
