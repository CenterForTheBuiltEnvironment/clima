from copy import deepcopy
from pages.lib.global_elementids import ElementIds

import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import html, dcc
from dash_extensions.enrich import Output, Input, State, callback

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
    month_lst,
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


def sun_path():
    """Return the layout for the custom sun path and its dropdowns."""
    return html.Div(
        className="container-col justify-center",
        children=[
            html.Div(
                children=title_with_link(
                    text="Sun path chart",
                    id_button="sun-path-chart-label",
                    doc_link=DocLinks.SUN_PATH_DIAGRAM,
                ),
            ),
            dbc.Row(
                align="center",
                justify="center",
                children=[
                    html.H6(
                        className="text-next-to-input",
                        children=["View: "],
                        style={"width": "10rem"},
                    ),
                    dropdown(
                        id= ElementIds.CUSTOM_SUN_VIEW_DROPDOWN,
                        options={
                            "Spherical": "polar",
                            "Cartesian": "cartesian",
                        },
                        value="polar",
                        style={"width": "10rem"},
                    ),
                ],
            ),
            dbc.Row(
                align="center",
                justify="center",
                children=[
                    html.H6(
                        className="text-next-to-input",
                        children=["Select variable: "],
                        style={"width": "10rem"},
                    ),
                    dropdown(
                        id= ElementIds.CUSTOM_SUN_VAR_DROPDOWN,
                        options=sc_dropdown_names,
                        value="None",
                        style={"width": "20rem"},
                    ),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(
                    id= ElementIds.CUSTOM_SUNPATH,
                ),
            ),
        ],
    )


def explore_daily_heatmap():
    """Contents of the bottom part of the tab"""
    return html.Div(
        className="container-col full-width",
        children=[
            html.Div(
                children=title_with_link(
                    text="Daily charts",
                    id_button="daily-chart-label",
                    doc_link=DocLinks.CUSTOM_HEATMAP,
                ),
            ),
            html.Div(
                className="container-row justify-center align-center mb-2",
                children=[
                    html.H6(
                        className="text-next-to-input",
                        children=["Select variable: "],
                        style={"width": "10rem"},
                    ),
                    dropdown(
                        id=ElementIds.TAB_EXPLORE_DROPDOWN,
                        options=sun_cloud_tab_explore_dropdown_names,
                        value="glob_hor_rad",
                        style={"width": "20rem"},
                    ),
                ],
            ),
            dcc.Loading(type="circle", children=html.Div(id= ElementIds.TAB4_DAILY)),
            dcc.Loading(
                type="circle",
                children=html.Div(id=ElementIds.TAB4_HEATMAP),
            ),
        ],
    )


def static_section():
    return html.Div(
        id= ElementIds.STATIC_SECTION,
        className="container-col full-width",
        children=[
            # ...
        ],
    )


def layout():
    """Contents of tab four."""
    return html.Div(
        className="container-col",
        id= ElementIds.TAB_FOUR_CONTAINER,
        children=[sun_path(), static_section(), explore_daily_heatmap()],
    )


@callback(Output(ElementIds.STATIC_SECTION, "children"), [Input(ElementIds.ID_SUN_SI_IP_RADIO_INPUT, "value")])
def update_static_section(si_ip):
    hor_unit = "Wh/m²"
    if si_ip == UnitSystem.IP:
        hor_unit = "Btu/ft²"
    return [
        html.Div(
            children=title_with_link(
                text="Global and Diffuse Horizontal Solar Radiation (" + hor_unit + ")",
                id_button="monthly-chart-label",
                doc_link=DocLinks.SOLAR_RADIATION,
            ),
        ),
        dcc.Loading(
            type="circle",
            children=html.Div(id= ElementIds.MONTHLY_SOLAR),
        ),
        html.Div(
            children=title_with_link(
                text="Cloud coverage",
                id_button="cloud-chart-label",
                doc_link=DocLinks.CLOUD_COVER,
            ),
        ),
        dcc.Loading(
            type="circle",
            children=html.Div(id= ElementIds.CLOUD_COVER),
        ),
    ]


@callback(
    [
        Output(ElementIds.MONTHLY_SOLAR, "children"),
        Output(ElementIds.CLOUD_COVER, "children"),
    ],
    [
        Input(ElementIds.ID_SUN_DF_STORE, "modified_timestamp"),
    ],
    [
        State(ElementIds.ID_SUN_DF_STORE, "data"),
        State(ElementIds.ID_SUN_META_STORE, "data"),
        State(ElementIds.ID_SUN_SI_IP_UNIT_STORE, "data"),
    ],
)
def monthly_and_cloud_chart(_, df, meta, si_ip):
    """Update the contents of tab four. Passing in the polar selection and the general info (df, meta)."""

    # Sun Radiation
    monthly = monthly_solar(df, si_ip)
    monthly = monthly.update_layout(margin=tight_margins)

    # Cloud Cover
    cover = barchart(df, "tot_sky_cover", [False], [False, "", 3, 7], True, si_ip)
    cover = cover.update_layout(
        margin=tight_margins,
        title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
    )
    cover.update_xaxes(
        dict(tickmode="array", tickvals=np.arange(0, 12, 1), ticktext=month_lst)
    )
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name(
            "Global_and_Diffuse_Horizontal_Solar_Radiation", meta, units
        ),
        figure=monthly,
    ), dcc.Graph(
        config=generate_chart_name("cloud_cover", meta, units),
        figure=cover,
    )


@callback(
    Output(ElementIds.CUSTOM_SUNPATH, "children"),
    [
        Input(ElementIds.ID_SUN_DF_STORE, "modified_timestamp"),
        Input(ElementIds.CUSTOM_SUN_VIEW_DROPDOWN, "value"),
        Input(ElementIds.CUSTOM_SUN_VAR_DROPDOWN, "value"),
        Input(ElementIds.ID_SUN_GLOBAL_LOCAL_RADIO_INPUT, "value"),
    ],
    [
        State(ElementIds.ID_SUN_DF_STORE, "data"),
        State(ElementIds.ID_SUN_META_STORE, "data"),
        State(ElementIds.ID_SUN_SI_IP_UNIT_STORE, "data"),
    ],
)
def sun_path_chart(_, view, var, global_local, df, meta, si_ip):
    """Update the contents of tab four. Passing in the polar selection and the general info (df, meta)."""
    custom_inputs = "" if var == "None" else f"{var}"
    units = "" if var == "None" else generate_units(si_ip)
    if view == "polar":
        return dcc.Graph(
            config=generate_chart_name("spherical_sunpath", meta, custom_inputs, units),
            figure=polar_graph(df, meta, global_local, var, si_ip),
        )
    else:
        return dcc.Graph(
            config=generate_chart_name("cartesian_sunpath", meta, custom_inputs, units),
            figure=custom_cartesian_solar(df, meta, global_local, var, si_ip),
        )


@callback(
    Output(ElementIds.TAB4_DAILY, "children"),
    [
        Input(ElementIds.ID_SUN_DF_STORE, "modified_timestamp"),
        Input(ElementIds.TAB_EXPLORE_DROPDOWN, "value"),
        Input(ElementIds.ID_SUN_GLOBAL_LOCAL_RADIO_INPUT, "value"),
    ],
    [
        State(ElementIds.ID_SUN_DF_STORE, "data"),
        State(ElementIds.ID_SUN_META_STORE, "data"),
        State(ElementIds.ID_SUN_SI_IP_UNIT_STORE, "data"),
    ],
)
def daily(_, var, global_local, df, meta, si_ip):
    """Update the contents of tab four section two. Passing in the general info (df, meta)."""
    custom_inputs = generate_custom_inputs(var)
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name("daily", meta, custom_inputs, units),
        figure=daily_profile(df, var, global_local, si_ip),
    )


@callback(
    Output(ElementIds.TAB4_HEATMAP, "children"),
    [
        Input(ElementIds.ID_SUN_DF_STORE, "modified_timestamp"),
        Input(ElementIds.TAB_EXPLORE_DROPDOWN, "value"),
        Input(ElementIds.ID_SUN_GLOBAL_LOCAL_RADIO_INPUT, "value"),
    ],
    [
        State(ElementIds.ID_SUN_DF_STORE, "data"),
        State(ElementIds.ID_SUN_META_STORE, "data"),
        State(ElementIds.ID_SUN_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_heatmap(_, var, global_local, df, meta, si_ip):
    custom_inputs = generate_custom_inputs(var)
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name("heatmap", meta, custom_inputs, units),
        figure=heatmap(df, var, global_local, si_ip),
    )
