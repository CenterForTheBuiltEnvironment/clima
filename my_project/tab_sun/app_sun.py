import dash_core_components as dcc
import dash_html_components as html
from my_project.global_scheme import (
    config,
    tab4_dropdown_names,
    tab4_explore_dropdown_names,
)
from dash.dependencies import Input, Output, State

from my_project.tab_sun.charts_sun import (
    monthly_solar,
    polar_graph,
    custom_cartesian_solar,
)
from my_project.template_graphs import heatmap, barchart, daily_profile
import pandas as pd

from app import app, cache, TIMEOUT


def sunpath():
    """Return the layout for the custom sun path and its dropdowns."""
    return html.Div(
        className="container-col full-width",
        id="tab-four-custom-sun-container",
        children=[
            html.Div(
                className="container-row container-center full-width text-dropdown-container",
                children=[
                    html.H6(className="text-next-to-input", children=["Variable: "]),
                    dcc.Dropdown(
                        id="custom-sun-var-dropdown",
                        options=[
                            {"label": i, "value": tab4_dropdown_names[i]}
                            for i in tab4_dropdown_names
                        ],
                        value="DBT",
                    ),
                ],
            ),
            html.Div(
                className="container-row container-center full-width text-dropdown-container",
                children=[
                    html.H6(className="text-next-to-input", children=["View: "]),
                    dcc.Dropdown(
                        id="custom-sun-view-dropdown",
                        options=[
                            {"label": "Spherical", "value": "polar"},
                            {"label": "Cartesian", "value": "cartesian"},
                        ],
                        value="polar",
                    ),
                ],
            ),
            html.Div(
                id="sunpath-container",
                children=[
                    dcc.Graph(id="custom-sunpath", config=config),
                ],
            ),
        ],
    )


def explore_daily_heatmap():
    """ Contents of the bottom part of the tab"""
    return html.Div(
        className="container-col full-width",
        children=[
            dcc.Dropdown(
                id="tab4-explore-dropdown",
                options=[
                    {"label": i, "value": tab4_explore_dropdown_names[i]}
                    for i in tab4_explore_dropdown_names
                ],
                value="GHrad",
            ),
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="tab4-daily", config=config),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="tab4-heatmap", config=config),
                ],
            ),
        ],
    )


def static_section():
    return html.Div(
        className="container-col full-width",
        children=[
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="monthly-solar", config=config),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="cloud-cover", config=config),
                ],
            ),
        ],
    )


def layout_sun():
    """Contents of tab four."""
    return html.Div(
        className="container-col",
        id="tab-four-container",
        children=[sunpath(), static_section(), explore_daily_heatmap()],
    )


# TAB 4: SUN
@app.callback(
    Output("monthly-solar", "figure"),
    Output("cloud-cover", "figure"),
    [Input("df-store", "modified_timestamp")],
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_four_section_one(ts, global_local, df, meta):
    """Update the contents of tab four. Passing in the polar selection and the general info (df, meta)."""
    df = pd.read_json(df, orient="split")

    # Sun Radiation
    monthly = monthly_solar(df, meta)
    monthly = monthly.update_layout(
        title="Global and Diffuse Horizontal Solar Radiation (KWh/m²)"
    )

    # Cloud Cover
    cover = barchart(df, "Tskycover", [False], [False, "", 3, 7], True)
    cover = cover.update_layout(title="Cloud Coverage")

    return monthly, cover


# custom sun path
@app.callback(
    Output("custom-sunpath", "figure"),
    [Input("custom-sun-view-dropdown", "value")],
    [Input("custom-sun-var-dropdown", "value")],
    [Input("df-store", "modified_timestamp")],
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_four(view, var, ts, global_local, df, meta):
    """Update the contents of tab four. Passing in the polar selection and the general info (df, meta)."""
    df = pd.read_json(df, orient="split")

    # Sunpaths

    if view == "polar":
        return polar_graph(df, meta, global_local, var)

    else:
        return custom_cartesian_solar(df, meta, global_local, var)


# DAILY
@app.callback(
    Output("tab4-daily", "figure"),
    [Input("tab4-explore-dropdown", "value")],
    [Input("df-store", "modified_timestamp")],
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_four_daily_profile(var, ts, global_local, df, meta):
    """Update the contents of tab four section two. Passing in the general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    return daily_profile(df, var, global_local)


# HEATMAP
@app.callback(
    Output("tab4-heatmap", "figure"),
    [Input("tab4-explore-dropdown", "value")],
    [Input("df-store", "modified_timestamp")],
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_four_heatmap(var, ts, global_local, df, meta):
    """Update the contents of tab four section two. Passing in the general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    return heatmap(df, var, global_local)