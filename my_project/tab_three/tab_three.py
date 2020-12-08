import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from my_project.server import app
from my_project.global_scheme import config

def tab_three():
    return html.Div(
        className = "container-col", 
        children = [
            html.H5('Dry Bulb Temperature'),
            dcc.Graph(
                id = 'yearly-dbt',
                config = config
            ), 
            dcc.Graph(
                id = 'daily-dbt',
                config = config
            ), 
            dcc.Graph(
                id = 'heatmap-dbt',
                config = config
            ), 
            html.H5('Relative Humidity'),
            dcc.Graph(
                id = 'yearly-rh',
                config = config
            ), 
            dcc.Graph(
                id = 'daily-rh',
                config = config
            ), 
            dcc.Graph(
                id = 'heatmap-rh',
                config = config
            )
        ]
    )