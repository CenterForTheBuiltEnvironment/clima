import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from my_project.global_scheme import config

def tab_six():
    """ Return the contents of tab six."
    """
    return html.Div(
        className = 'continer-col',
        children = [
            dcc.Dropdown(
                id = 'tab-six-dropdown',
                options = [
                    {'label': 'Polar', 'value': 'polar'},
                    {'label': 'Latitude/Longitude', 'value': 'lat/long'}
                ],
                value = ''
            ),
            dcc.Graph(
                id = 'query-yearly',
                config = config
            ),
            dcc.Graph(
                id = 'query-daily',
                config = config
            ), 
            dcc.Graph(
                id = 'query-heatmap',
                config = config
            )
        ]
    )