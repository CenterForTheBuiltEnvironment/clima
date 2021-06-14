import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from my_project.global_scheme import config
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app, cache, TIMEOUT
from my_project.tab_two.tab_two_graphs import world_map
from my_project.template_graphs import violin
from my_project.utils import code_timer


def tab_two():
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
            dcc.Graph(className="tab-two-section", id="world-map", config=config),
            html.Div(
                className="container-col tab-two-section",
                id="location-description",
                children=[
                    html.P("Koeppen Geiger Climate Classification: "),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elitsed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                    ),
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
                className="violin-container",
                children=[
                    dcc.Graph(id="temp-profile-graph", config=config),
                ],
            ),
            html.Div(
                className="violin-container",
                children=[
                    dcc.Graph(id="humidity-profile-graph", config=config),
                ],
            ),
            html.Div(
                className="violin-container",
                children=[
                    dcc.Graph(id="solar-radiation-graph", config=config),
                ],
            ),
            html.Div(
                className="violin-container",
                children=[
                    dcc.Graph(id="wind-speed-graph", config=config),
                ],
            ),
        ],
    )


# TAB TWO: CLIMATE
@app.callback(
    Output("world-map", "figure"),
    Output("temp-profile-graph", "figure"),
    Output("humidity-profile-graph", "figure"),
    Output("solar-radiation-graph", "figure"),
    Output("wind-speed-graph", "figure"),
    Output("tab-two-location", "children"),
    Output("tab-two-long", "children"),
    Output("tab-two-lat", "children"),
    Output("tab-two-elevation", "children"),
    [Input("df-store", "modified_timestamp")],
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
@code_timer
def update_tab_two(ts, global_local, df, meta):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    location = "Location: " + meta[1] + ", " + meta[3]
    lon = "Longitude: " + str(meta[-4])
    lat = "Latitude: " + str(meta[-5])
    elevation = "Elevation above sea level: " + meta[-2]

    # Violin Graphs
    dbt = violin(df, "DBT", global_local)
    rh = violin(df, "RH", global_local)
    ghrad = violin(df, "GHrad", global_local)
    wspeed = violin(df, "Wspeed", global_local)

    return world_map(meta), dbt, rh, ghrad, wspeed, location, lon, lat, elevation
