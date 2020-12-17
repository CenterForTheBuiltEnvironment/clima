import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from my_project.global_scheme import config

def sliders():
    """ Returns 2 sliders for the hour
    """
    return html.Div(
        className = 'container-col container-center',
        id = 'slider-container',
        children = [
            html.H3("Customizable Wind Rose"),
            html.Div(
                className = 'container-row each-slider',
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
                        allowCross = True
                    ),
                ]
            ),
            html.Div(
                className = 'container-row each-slider',
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

def seasonal_wind_rose():
    """ Return the section with the 4 seasonal wind rose graphs.
    """
    return html.Div(
        className = "container-col full-width",
        children = [
            html.H5("Seasonal Wind Rose"),
            html.Div(
                className = "container-row container-center",
                children = [
                    dcc.Graph(
                        className = "seasonal-graph",
                        id = "winter-wind-rose",
                        config = config 
                    ),
                    dcc.Graph(
                        className = "seasonal-graph",
                        id = "spring-wind-rose",
                        config = config 
                    ),
                ]
            ),
            html.Div(
                className = "container-row container-center",
                children = [
                    dcc.Graph(
                        className = "seasonal-graph",
                        id = "summer-wind-rose",
                        config = config 
                    ),
                    dcc.Graph(
                        className = "seasonal-graph",
                        id = "fall-wind-rose",
                        config = config 
                    )
                ]
            )
        ]
    )

def daily_wind_rose():
    """ Return the section for the 3 daily wind rose graphs.
    """
    return html.Div(
        className = "container-col full-width",
        children = [
            html.H5("Daily Wind Rose"),
            html.Div(
                className = "container-row full-width container-center",
                children = [
                    dcc.Graph(
                        className = "daily-wind-graph",
                        id = "morning-wind-rose",
                        config = config
                    ),
                    dcc.Graph(
                        className = "daily-wind-graph",
                        id = "noon-wind-rose",
                        config = config
                    ),
                    dcc.Graph(
                        className = "daily-wind-graph",
                        id = "night-wind-rose",
                        config = config
                    ),
                ]
            ),
        ]
    )

def tab_five():
    """ Contents in the fifth tab 'Wind'.
    """
    return html.Div(
        className = 'container-col',
        id = 'tab-five-container',
        children = [
            html.H5("Annual Wind Rose"),
            dcc.Graph(
                id = 'wind-rose'
            ), 
            dcc.Graph(
                id = 'wind-speed',
                config = config
            ), 
            dcc.Graph(
                id = 'wind-direction',
                config = config
            ),
            seasonal_wind_rose(),
            daily_wind_rose(),
            sliders(),
            dcc.Graph(
                id = 'custom-wind-rose'
            ), 
        ]
    )