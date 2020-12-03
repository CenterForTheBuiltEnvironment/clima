import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from my_project.server import app 
from my_project.global_scheme import config
from .tab_four_graphs import polar_solar, lat_long_solar, monthly_solar, horizontal_solar, diffuse_solar, direct_solar, cloud_cover

def tab_four():
    """ Contents of tab four.
    """
    return html.Div(
        className = "container-col tab-container",
        id = "tab-four-container",
        children = [
            dcc.Dropdown(
                id = "solar-dropdown", 
                options = [
                    {'label': 'Polar', 'value': 'polar'},
                    {'label': 'Latitude/Longitude', 'value': 'lat/long'}
                ], 
                value = 'polar'
            ),
            dcc.Graph(
                id = 'solar-dropdown-output',
                config = config
            ), 
            dcc.Graph(
                id = 'monthly-solar',
                config = config
            ), 
            dcc.Graph(
                id = 'horizontal-solar',
                config = config
            ), 
            dcc.Graph(
                id = 'diffuse-solar',
                config = config
            ), 
            dcc.Graph(
                id = 'direct-solar',
                config = config
            ), 
            dcc.Graph(
                id = 'cloud-cover',
                config = config
            )
        ]
    )