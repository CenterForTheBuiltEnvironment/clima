import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from my_project.global_scheme import config

def tab_seven():
    """ Return the contents for tab 7.
    """
    return html.Div(
        className = "container-col",
        children = [
            dcc.Loading(
                type = "circle",
                children = [
                    dcc.Graph(
                        id = "utci-heatmap",
                        config = config 
                    )
                ]
            )
        ]
    )