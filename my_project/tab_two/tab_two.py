import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from my_project.server import app 
from my_project.global_scheme import config
from .tab_two_graphs import world_map, dbt_violin, humidity_violin, solar_violin, wind_violin

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
                id = "world-map"
            ),
            html.Div(
                className = 'container-col tab-two-section',
                id = 'location-description',
                children = [
                    html.P('Koeppen Geiger Climate Classification: '),
                    html.P('Filler text'),
                    html.P('Filler text')
                ]
            ),
        ]
    )
    
def graph_section():
    """ Returns the contents of the graph section which includes 
    the 'Climate Profiles' title and the graphs. 
    """
    return html.Div(
            className = "tab-container tab-two-section",
            children = [
                html.Div(
                    className = "container-col",
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
                dcc.Graph(
                    id = 'temp-profile-graph',
                    config = config
                ), 
                dcc.Graph(
                    id = 'humidity-profile-graph',
                    config = config
                ), 
                dcc.Graph(
                    id = 'solar-radiation-graph',
                    config = config
                ), 
                dcc.Graph(
                    id = 'wind-speed-graph',
                    config = config
                )
            ]
        )