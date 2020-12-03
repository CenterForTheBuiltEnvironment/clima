import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from my_project.server import app
from my_project.global_scheme import config
from .tab_three_graphs import daily_dbt, daily_humidity, monthly_dbt3, monthly_humidity, heatmap_dbt, heatmap_humidity

def tab_three():
    return html.Div(
        className = "container-col", 
        children = [
            dcc.Graph(
                id = 'daily-dbt',
                config = config
            ), 
            dcc.Graph(
                id = 'daily-humidity',
                config = config
            ), 
            dcc.Graph(
                id = 'monthly-dbt-3',
                config = config
            ), 
            dcc.Graph(
                id = 'monthly-humidity',
                config = config
            ), 
            dcc.Graph(
                id = 'heatmap-dbt',
                config = config
            ), 
            dcc.Graph(
                id = 'heatmap-humidity',
                config = config
            )
        ]
    )