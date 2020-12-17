import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from my_project.server import app 
from my_project.global_scheme import config, var_name_lst

def custom():
    """ Return the layout for the custom sunpath and its dropdowns.
    """
    return html.Div(
        className = 'container-col',
        id = "tab-four-custom-sun-container",
        children = [
            dcc.Dropdown(
                id = "custom-sun-var-dropdown", 
                options = [
                    {'label': i, 'value': i} for i in var_name_lst
                ], 
                value = 'RH'
            ),
            dcc.Graph(
                id = 'custom-sunpath',
                config = config
            )
        ]
    )


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
            html.Div(
                className = 'container-row',
                id = 'tab-four-subcontainer',
                children = [
                    dcc.Graph(
                        id = 'yearly-solar',
                        config = config
                    ),
                    dcc.Graph(
                        id = 'monthly-solar',
                        config = config
                    ), 
                ]
            ),
            dcc.Graph(
                id = 'cloud-cover',
                config = config
            ),
            custom(),
            dcc.Graph(
                id = 'daily-ghrad',
                config = config
            ), 
            dcc.Graph(
                id = 'heatmap-ghrad',
                config = config
            ), 
            dcc.Graph(
                id = 'daily-dnrad',
                config = config
            ), 
            dcc.Graph(
                id = 'heatmap-dnrad',
                config = config
            ),
            dcc.Graph(
                id = 'daily-difhrad',
                config = config
            ), 
            dcc.Graph(
                id = 'heatmap-difhrad',
                config = config
            )
        ]
    )