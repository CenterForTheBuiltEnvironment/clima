import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from my_project.server import app 
from my_project.global_scheme import config

def tab_five():
    """ Contents in the fifth tab 'Wind'.
    """
    return html.Div(
        className = 'container-col',
        children = [
            sliders(),
            dcc.Graph(
                id = 'wind-rose'
            )
        ]
    )

def sliders():
    """ Returns 2 sliders for the hour
    """
    return html.Div(
        className = 'container-col',
        children = [
            dcc.RangeSlider(
                id = 'month-slider',
                min = 1,
                max = 12,
                step = 1,
                value = [1, 12]
            ),
            dcc.RangeSlider(
                id = 'hour-slider',
                min = 1,
                max = 24,
                step = 1,
                value = [1, 24]
            )
        ]
    )