import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app, cache, TIMEOUT
from my_project.tab_summary.charts_summary import world_map
from my_project.template_graphs import violin
from my_project.utils import generate_chart_name


def layout_summary():
    """Contents in the second tab 'Climate Summary'."""
    return html.Div(
        className="container-col",
        id="tab-two-container",
        children=[map_section(), graph_section()],
    )


def map_section():
    """Returns the contents of the map section which includes
    location information, world map, location description.
    """
    return html.Div(
        className="container-col tab-two-section",
        id="tab2-sec1-container",
        children=[
            html.Div(
                className="container-col tab-two-section",
                id="location-info",
                children=[
                    html.B(id="tab-two-location"),
                    html.P(id="tab-two-long"),
                    html.P(id="tab-two-lat"),
                    html.P(id="tab-two-elevation"),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(className="tab-two-section", id="world-map"),
            ),
            html.Div(
                className="container-col tab-two-section",
                id="location-description",
                children=[
                    html.P("Koeppen Geiger Climate Classification: "),
                    html.P("Placeholder text"),
                ],
            ),
        ],
    )


def graph_section():
    """Returns the contents of the graph section which includes
    the 'Climate Profiles' title and the graphs.
    """
    return html.Div(
        className="tab-container container-col",
        id="tab2-sec2-container",
        children=[climate_profiles_title(), climate_profiles_graphs()],
    )


def climate_profiles_title():
    """"""
    return html.Div(
        id="tooltip-title-container",
        className="container-row",
        children=[
            html.H5("Climate Profiles"),
            html.Div(
                [
                    html.Span(
                        "?",
                        id="tooltip-target",
                        style={"textAlign": "center", "color": "white"},
                        className="dot",
                    ),
                    dbc.Tooltip(
                        "Some information text",
                        target="tooltip-target",
                        placement="right",
                    ),
                ]
            ),
        ],
    )


def climate_profiles_graphs():
    """"""
    return html.Div(
        id="graph-container",
        className="container-row",
        children=[
            html.Div(
                id="temp-profile-graph",
            ),
            html.Div(
                id="humidity-profile-graph",
            ),
            html.Div(
                id="solar-radiation-graph",
            ),
            html.Div(
                id="wind-speed-graph",
            ),
        ],
    )


@app.callback(
    Output("world-map", "children"),
    Output("tab-two-location", "children"),
    Output("tab-two-long", "children"),
    Output("tab-two-lat", "children"),
    Output("tab-two-elevation", "children"),
    [Input("df-store", "modified_timestamp")],
    [Input("global-local-radio-input", "value")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_map(ts, global_local, meta):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    location = "Location: " + meta[1] + ", " + meta[3]
    lon = "Longitude: " + str(meta[-4])
    lat = "Latitude: " + str(meta[-5])
    elevation = "Elevation above sea level: " + meta[-2]

    map_world = dcc.Graph(
        id="gh_rad-profile-graph",
        config=generate_chart_name("summary", meta),
        figure=world_map(meta),
    )

    return map_world, location, lon, lat, elevation


@app.callback(
    Output("temp-profile-graph", "children"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_violin_tdb(global_local, df, meta):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    df = pd.read_json(df, orient="split")

    return dcc.Graph(
        id="tdb-profile-graph",
        className="violin-container",
        config=generate_chart_name("summary", meta),
        figure=violin(df, "DBT", global_local),
    )


@app.callback(
    Output("wind-speed-graph", "children"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_wind(global_local, df, meta):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    df = pd.read_json(df, orient="split")

    return dcc.Graph(
        id="wind-profile-graph",
        className="violin-container",
        config=generate_chart_name("summary", meta),
        figure=violin(df, "Wspeed", global_local),
    )


@app.callback(
    Output("humidity-profile-graph", "children"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_rh(global_local, df, meta):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    df = pd.read_json(df, orient="split")

    return dcc.Graph(
        id="rh-profile-graph",
        className="violin-container",
        config=generate_chart_name("summary", meta),
        figure=violin(df, "RH", global_local),
    )


@app.callback(
    Output("solar-radiation-graph", "children"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_gh_rad(global_local, df, meta):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    df = pd.read_json(df, orient="split")

    return dcc.Graph(
        id="gh_rad-profile-graph",
        className="violin-container",
        config=generate_chart_name("summary", meta),
        figure=violin(df, "GHrad", global_local),
    )
