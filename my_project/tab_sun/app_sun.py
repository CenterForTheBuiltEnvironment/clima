import dash_core_components as dcc
import dash_html_components as html
from my_project.global_scheme import (
    fig_config,
    tab4_dropdown_names,
    tab4_explore_dropdown_names,
    tight_margins,
)
from dash.dependencies import Input, Output, State

from my_project.tab_sun.charts_sun import (
    monthly_solar,
    polar_graph,
    custom_cartesian_solar,
)
from my_project.template_graphs import heatmap, barchart, daily_profile
import pandas as pd
from my_project.utils import title_with_tooltip, generate_chart_name

from app import app, cache, TIMEOUT


def sun_path():
    """Return the layout for the custom sun path and its dropdowns."""
    return html.Div(
        className="container-col full-width",
        id="tab-four-custom-sun-container",
        children=[
            html.Div(
                children=title_with_tooltip(
                    text="Sun path chart",
                    tooltip_text="Sun path chart",
                    id_button="sun-path-chart-label",
                ),
            ),
            html.Div(
                className="container-row justify-center align-center",
                children=[
                    html.H6(
                        className="text-next-to-input",
                        children=["View: "],
                        style={"width": "10rem"},
                    ),
                    dcc.Dropdown(
                        id="custom-sun-view-dropdown",
                        options=[
                            {"label": "Spherical", "value": "polar"},
                            {"label": "Cartesian", "value": "cartesian"},
                        ],
                        value="polar",
                        style={"width": "20rem"},
                    ),
                ],
            ),
            html.Div(
                className="container-row justify-center align-center",
                children=[
                    html.H6(
                        className="text-next-to-input",
                        children=["Variable: "],
                        style={"width": "10rem"},
                    ),
                    dcc.Dropdown(
                        id="custom-sun-var-dropdown",
                        options=[
                            {"label": i, "value": tab4_dropdown_names[i]}
                            for i in tab4_dropdown_names
                        ],
                        value="None",
                        style={"width": "20rem"},
                    ),
                ],
            ),
            html.Div(
                id="sunpath-container",
                children=[
                    dcc.Loading(
                        type="circle",
                        children=html.Div(
                            id="custom-sunpath",
                            className="container-row full-width align-center justify-center",
                        ),
                    ),
                ],
            ),
        ],
    )


def explore_daily_heatmap():
    """ Contents of the bottom part of the tab"""
    return html.Div(
        className="container-col full-width",
        children=[
            html.Div(
                children=title_with_tooltip(
                    text="Daily charts",
                    tooltip_text="Daily charts",
                    id_button="daily-chart-label",
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
                    dcc.Dropdown(
                        id="tab4-explore-dropdown",
                        options=[
                            {"label": i, "value": tab4_explore_dropdown_names[i]}
                            for i in tab4_explore_dropdown_names
                        ],
                        value="GHrad",
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
        className="container-col full-width",
        children=[
            html.Div(
                children=title_with_tooltip(
                    text="Global and Diffuse Horizontal Solar Radiation (KWh/m²)",
                    tooltip_text="Global and Diffuse Horizontal Solar Radiation chart",
                    id_button="monthly-chart-label",
                ),
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(id="monthly-solar"),
            ),
            html.Div(
                children=title_with_tooltip(
                    text="Cloud coverage",
                    tooltip_text="Cloud coverage",
                    id_button="cloud-chart-label",
                ),
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(id="cloud-cover"),
            ),
        ],
    )


def layout_sun():
    """Contents of tab four."""
    return html.Div(
        className="container-col",
        id="tab-four-container",
        children=[sun_path(), static_section(), explore_daily_heatmap()],
    )


@app.callback(
    [
        Output("monthly-solar", "children"),
        Output("cloud-cover", "children"),
    ],
    [
        Input("df-store", "modified_timestamp"),
    ],
    [State("df-store", "data"), State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def monthly_and_cloud_chart(ts, df, meta):
    """Update the contents of tab four. Passing in the polar selection and the general info (df, meta)."""
    df = pd.read_json(df, orient="split")

    # Sun Radiation
    monthly = monthly_solar(df)
    monthly = monthly.update_layout(margin=tight_margins)

    # Cloud Cover
    cover = barchart(df, "Tskycover", [False], [False, "", 3, 7], True)
    cover = cover.update_layout(margin=tight_margins, title="")

    return dcc.Graph(
        config=generate_chart_name("monthly_sun", meta),
        figure=monthly,
    ), dcc.Graph(
        config=generate_chart_name("cloud_cover_sun", meta),
        figure=cover,
    )


@app.callback(
    Output("custom-sunpath", "children"),
    [
        Input("custom-sun-view-dropdown", "value"),
        Input("custom-sun-var-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [State("df-store", "data"), State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def sun_path_chart(view, var, global_local, df, meta):
    """Update the contents of tab four. Passing in the polar selection and the general info (df, meta)."""
    df = pd.read_json(df, orient="split")

    if view == "polar":
        return dcc.Graph(
            config=generate_chart_name("spherical_sun_path_sun", meta),
            figure=polar_graph(df, meta, global_local, var),
        )
    else:
        return dcc.Graph(
            config=generate_chart_name("cartesian_sun_path_sun", meta),
            figure=custom_cartesian_solar(df, meta, global_local, var),
        )


@app.callback(
    Output("tab4-daily", "children"),
    [
        Input("tab4-explore-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [State("df-store", "data"), State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def daily(var, global_local, df, meta):
    """Update the contents of tab four section two. Passing in the general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    return dcc.Graph(
        config=generate_chart_name("daily_sun", meta),
        figure=daily_profile(df, var, global_local),
    )


@app.callback(
    Output("tab4-heatmap", "children"),
    [
        Input("tab4-explore-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [State("df-store", "data"), State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_heatmap(var, global_local, df, meta):
    df = pd.read_json(df, orient="split")
    return dcc.Graph(
        config=generate_chart_name("heatmap_sun", meta),
        figure=heatmap(df, var, global_local),
    )
