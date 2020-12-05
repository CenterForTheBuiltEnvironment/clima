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
        id = 'tab-five-container',
        children = [
            sliders(),
            dcc.Graph(
                id = 'wind-rose'
            ), 
            dcc.Graph(
                id = 'wind-heatmap',
                config = config
            )
        ]
    )

def sliders():
    """ Returns 2 sliders for the hour
    """
    return html.Div(
        className = 'container-col',
        id = 'slider-container',
        children = [
            html.Div(
                className = 'container-row',
                children = [
                    html.P("Month Range"),
                    dcc.RangeSlider(
                        id = 'month-slider',
                        min = 1,
                        max = 12,
                        step = 1,
                        value = [1, 12], 
                        marks = {
                            1: '1',
                            12: '12'
                        },
                        tooltip = {
                            'always_visible': False,
                            'placement' : 'top'
                        },
                        allowCross = False
                    ),
                ]
            ),
            html.Div(
                className = 'container-row',
                children = [
                    html.P("Hour Range"),
                    dcc.RangeSlider(
                        id = 'hour-slider',
                        min = 1,
                        max = 24,
                        step = 1,
                        value = [1, 24],
                        marks = {
                            1: '1',
                            24: '24'
                        },
                        tooltip = {
                            'always_visible': False,
                            'placement' : 'topLeft'
                        },
                        allowCross = False
                    )
                ]
            ),
        ]
    )