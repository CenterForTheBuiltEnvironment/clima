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
            month_sliders(),
            hour_sliders(),
            dcc.Graph(
                id = 'wind-rose'
            )
        ]
    )

def month_sliders():
    """ Returns 2 sliders for the months
    """
    return html.Div(
        className = 'container-col',
        children = [
            dcc.Slider(
                id = 'start-month-slider',
                min = 1,
                max = 12,
                step = None,
                marks = {
                    1: '1',
                    3: '3',
                    6: '6',
                    9: '9',
                    12: '12'
                },
                value = 1
            ),  
            dcc.Slider(
                id = 'end-month-slider',
                min = 1,
                max = 12,
                step = None,
                marks = {
                    1: '1',
                    3: '3',
                    6: '6',
                    9: '9',
                    12: '12'
                },
                value = 12
            ) 
        ]
    )

def hour_sliders():
    """ Returns 2 sliders for the hour
    """
    return html.Div(
        className = 'container-col',
        children = [
            dcc.Slider(
                id = 'start-hour-slider',
                min = 1,
                max = 24,
                step = None,
                marks = {
                    1: '1',
                    6: '6',
                    12: '18',
                    18: '18',
                    24: '24'
                },
                value = 1
            ),  
            dcc.Slider(
                id = 'end-hour-slider',
                min = 1,
                max = 24,
                step = None,
                marks = {
                    1: '1',
                    6: '6',
                    12: '18',
                    18: '18',
                    24: '24'
                },
                value = 24
            ) 
        ]
    )