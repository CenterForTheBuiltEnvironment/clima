from copy import deepcopy

import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import html, dcc
from dash_extensions.enrich import Output, Input, State, callback

from config import PageUrls, DocLinks
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

dash.register_page(__name__, name="Sun and Clouds", path=PageUrls.SUN.value, order=3)


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
                    text="Sun path chart",
                    id_button="sun-path-chart-label",
                    doc_link=DocLinks.SUN_PATH_DIAGRAM,
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
                        id="custom-sun-view-dropdown",
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
                        id="custom-sun-var-dropdown",
                        options=sc_dropdown_names,
                        value="None",
                        style={"width": "20rem"},
                    ),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(
                    id="custom-sunpath",
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
                        id="tab4-explore-dropdown",
                        options=sun_cloud_tab_explore_dropdown_names,
                        value="glob_hor_rad",
                        style={"width": "20rem"},
                    ),
                ],
            ),
            dcc.Loading(type="circle", children=html.Div(id="tab4-daily")),
            dcc.Loading(
                type="circle",
                children=html.Div(id="tab4-heatmap"),
            ),
        ],
    )


def static_section():
    return html.Div(
        id="static-section",
        className="container-col full-width",
        children=[
            # ...
        ],
    )


def layout():
    """Contents of tab four."""
    return html.Div(
        className="container-col",
        id="tab-four-container",
        children=[sun_path(), static_section(), explore_daily_heatmap()],
    )


@callback(Output("static-section", "children"), [Input("si-ip-radio-input", "value")])
def update_static_section(si_ip):
    if si_ip == "si":
        hor_unit = "Wh/m²"
    if si_ip == "ip":
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
            children=html.Div(id="monthly-solar"),
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
            children=html.Div(id="cloud-cover"),
        ),
    ]


@callback(
    [
        Output("monthly-solar", "children"),
        Output("cloud-cover", "children"),
    ],
    [
        Input("df-store", "modified_timestamp"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
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
    Output("custom-sunpath", "children"),
    [
        Input("df-store", "modified_timestamp"),
        Input("custom-sun-view-dropdown", "value"),
        Input("custom-sun-var-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
def sun_path_chart(ts, view, var, global_local, df, meta, si_ip):
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
    Output("tab4-daily", "children"),
    [
        Input("df-store", "modified_timestamp"),
        Input("tab4-explore-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
def daily(ts, var, global_local, df, meta, si_ip):
    """Update the contents of tab four section two. Passing in the general info (df, meta)."""
    custom_inputs = generate_custom_inputs(var)
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name("daily", meta, custom_inputs, units),
        figure=daily_profile(df, var, global_local, si_ip),
    )


@callback(
    Output("tab4-heatmap", "children"),
    [
        Input("df-store", "modified_timestamp"),
        Input("tab4-explore-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
def update_heatmap(_, var, global_local, df, meta, si_ip):
    custom_inputs = generate_custom_inputs(var)
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name("heatmap", meta, custom_inputs, units),
        figure=heatmap(df, var, global_local, si_ip),
    )
