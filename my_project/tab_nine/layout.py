import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from my_project.global_scheme import config

from my_project.global_scheme import dropdown_names

def inputs():
    """
    """
    return html.Div(
        className = "container-row full-width three-inputs-container",
        children = [
            html.Div(
                className = "container-col container-center one-of-three-container",
                children = [
                    html.Div(
                        className = "container-row row-center full-width",
                        children = [
                            html.H6(
                                className = "text-next-to-input", 
                                children = ["X Variable:"]
                            ),
                            dcc.Dropdown(
                                className = "tab9-sec3-dropdown",
                                id = "tab9-var-x-dropdown", 
                                options = [
                                    {'label': i, 'value': dropdown_names[i]} for i in dropdown_names
                                ], 
                                value = 'DBT'
                            ),
                        ]
                    ),
                    html.Div(
                        className = "container-row row-center full-width",
                        children = [
                            html.H6(
                                className = "text-next-to-input", 
                                children = ["Y Variable:"]
                            ),
                            dcc.Dropdown(
                                className = "tab9-sec3-dropdown",
                                id = "tab9-var-y-dropdown", 
                                options = [
                                    {'label': i, 'value': dropdown_names[i]} for i in dropdown_names
                                ], 
                                value = 'RH'
                            ),
                        ]
                    ),
                    html.Div(
                        className = "container-row row-center full-width",
                        children = [
                            html.H6(
                                className = "text-next-to-input", 
                                children = ["Color By:"]
                            ),
                            dcc.Dropdown(
                                className = "tab9-sec3-dropdown",
                                id = "tab9-colorby-dropdown", 
                                options = [
                                    {'label': i, 'value': dropdown_names[i]} for i in dropdown_names
                                ], 
                                value = 'GHrad'
                            ),
                        ]
                    ),
                ]
            ),
            html.Div(
                className = "container-col container-center one-of-three-container",
                children = [
                    dbc.Checklist(
                        options = [
                            {"label": "Apply Time Filters", "value": "time"},
                        ],
                        value = ["time"],
                        id = "tab9-sec3-time-filter-input",
                    ),
                    html.Div(
                        className = 'container-row full-width container-center',
                        children = [
                            html.H6("Month Range"),
                            dcc.RangeSlider(
                                id = "tab9-sec3-query-month-slider",
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
                        className = 'container-row full-width container-center',
                        children = [
                            html.H6("Hour Range"),
                            dcc.RangeSlider(
                                id = "tab9-sec3-query-hour-slider",
                                min = 1,
                                max = 24,
                                step = 1,
                                value = [6, 20],
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
            ),
            html.Div(
                className = "container-col container-center one-of-three-container",
                children = [
                    dbc.Checklist(
                        options = [
                            {"label": "Apply Data Filters", "value": "data"},
                        ],
                        value = [],
                        id = "tab9-sec3-data-filter-input",
                    ),
                    html.Div(
                        className = "container-row row-center full-width",
                        children = [
                            html.H6(
                                className = "text-next-to-input", 
                                children = ["Filter Variable:"]
                            ),
                            dcc.Dropdown(
                                className = "tab9-sec3-dropdown",
                                id = "tab9-sec3-filter-var-dropdown", 
                                options = [
                                    {'label': i, 'value': dropdown_names[i]} for i in dropdown_names
                                ], 
                                value = 'RH'
                            ),
                        ]
                    ),
                    html.Div(
                        className = "container-row row-center full-width",
                        children = [
                            html.H6(
                                className = "text-next-to-input",
                                children = ["Min Value:"]
                            ),
                            dbc.Input(
                                className = "num-input",
                                id = "tab9-sec3-min-val",
                                placeholder = "Enter a number for the min val",
                                type = "number", 
                                min = 0, 
                                step = 1
                            ),
                        ]
                    ),
                    html.Div(
                        className = "container-row row-center full-width",
                        children = [
                            html.H6(
                                className = "text-next-to-input",
                                children = ["Max Value:"]
                            ),
                            dbc.Input(
                                className = "num-input",
                                id = "tab9-sec3-max-val",
                                placeholder = "Enter a number for the max val",
                                type = "number", 
                                min = 0, 
                                step = 1
                            ),
                        ]
                    ),
                ]
            )
        ]
    )

def tab_nine():
    return html.Div(
        className = "container-col",
        children = [
            inputs(), 
            dcc.Graph(
                id = "psych-chart",
                config = config
            )
        ]
    )