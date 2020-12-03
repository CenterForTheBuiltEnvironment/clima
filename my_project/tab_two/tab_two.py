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
        children = [
            dcc.Graph(
                id = "world-map"
            ),
            section_one()
        ]        
    )
    
def section_one():
    """
    """
    return html.Div(
            className = "tab-container",
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
            id = "tab-two-4-container",
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