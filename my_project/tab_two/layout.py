import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from my_project.global_scheme import config

def tab_two():
    """ Contents in the second tab 'Climate Summary'.
    """
    return html.Div(
        className = "container-col", 
        id = 'tab-two-container',
        children = [
            map_section(),
            graph_section()
        ]        
    )

def map_section():
    """ Returns the contents of the map section which includes
    location information, world map, location description.
    """
    return html.Div(
        className = 'container-col tab-two-section',
        id = "tab2-sec1-container",
        children = [
            html.Div(
                className = 'container-col tab-two-section',
                id = 'location-info',
                children = [
                    html.B(id = 'tab-two-location'),
                    html.P(id = 'tab-two-long'),
                    html.P(id = 'tab-two-lat'),
                    html.P(id = 'tab-two-elevation')
                ]
            ),
            dcc.Graph(
                className = 'tab-two-section',
                id = "world-map",
                config = config
            ),
            html.Div(
                className = 'container-col tab-two-section',
                id = 'location-description',
                children = [
                    html.P('Koeppen Geiger Climate Classification: '),
                    html.P(
                        'Lorem ipsum dolor sit amet, consectetur adipiscing elitsed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
                ]
            ),
        ]
    )
    
def graph_section():
    """ Returns the contents of the graph section which includes 
    the 'Climate Profiles' title and the graphs. 
    """
    return dcc.Loading(
        type = "circle",
        children = [
            html.Div(
                className = "tab-container tab-two-section container-col",
                id = "tab2-sec2-container",
                children = [
                    climate_profiles_title(), 
                    climate_profiles_graphs()
                ]
            )
        ]
    )

def climate_profiles_title():
    """
    """
    return html.Div(
            id = "tooltip-title-container",
            className = "container-row",
            children = [
                html.H5('Climate Profiles'),
                html.Div([
                    html.Span(
                        "?",
                        id = "tooltip-target",
                        style = {
                                "textAlign": "center", 
                                "color": "white"
                        },
                        className = "dot"),
                    dbc.Tooltip(
                        "Some information text",
                        target = "tooltip-target",
                        placement = "right"
                    )
                ])
            ]
        )

def climate_profiles_graphs():
    """
    """
    return html.Div(
            id = "graph-container",
            className = "container-row",
            children = [
                dcc.Loading(
                    type = "circle",
                    children = [
                        dcc.Graph(
                            id = 'temp-profile-graph',
                            config = config
                        ), 
                    ]
                ),
                dcc.Loading(
                    type = "circle",
                    children = [
                        dcc.Graph(
                            id = 'humidity-profile-graph',
                            config = config
                        ), 
                    ]
                ),
                dcc.Loading(
                    type = "circle",
                    children = [
                        dcc.Graph(
                            id = 'solar-radiation-graph',
                            config = config
                        ), 
                    ]
                ),
                dcc.Loading(
                    type = "circle",
                    children = [
                        dcc.Graph(
                            id = 'wind-speed-graph',
                            config = config
                        ), 
                    ]
                ),
            ]
        )
