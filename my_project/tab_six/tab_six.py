import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from my_project.global_scheme import config, var_name_lst

def section_one():
    """ Return the graphs for section one
    """
    return html.Div(
        className = "container-col container-center full-width",
        children = [
            dcc.Dropdown(
                id = "first-var-dropdown", 
                options = [
                    {'label': i, 'value': i} for i in var_name_lst
                ], 
                value = 'RH'
            ),
            dcc.Graph(
                className = "full-width",
                id = 'query-yearly',
                config = config
            ),
            dcc.Graph(
                className = "full-width",
                id = 'query-daily',
                config = config
            ), 
            dcc.Graph(
                className = "full-width",
                id = 'query-heatmap',
                config = config
            )
        ]
    )

def section_two():
    """ Return the two graphs in section two.
    """
    return html.Div(
        className = "container-col container-center full-width",
        children = [
            dcc.Dropdown(
                id = "second-var-dropdown", 
                options = [
                    {'label': i, 'value': i} for i in var_name_lst
                ], 
                value = 'RH'
            ),
            dbc.Checklist(
                options = [
                    {"label": "Apply Time Filters", "value": "time"},
                ],
                value = [],
                id = "time-filter-input",
            ),
            html.Div(
                className = 'container-row each-slider',
                children = [
                    html.P("Month Range"),
                    dcc.RangeSlider(
                        id = 'query-month-slider',
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
                        id = 'query-hour-slider',
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
            dbc.Checklist(
                options = [
                    {"label": "Apply Data Filters", "value": "data"},
                ],
                value = [],
                id = "data-filter-input",
            ),
            dcc.Dropdown(
                id = "second-filter-var-dropdown", 
                options = [
                    {'label': i, 'value': i} for i in var_name_lst
                ], 
                value = 'RH'
            ),
            dbc.Input(
                id = "min-val",
                placeholder = "Enter a number for the min val",
                type = "number", 
                min = 0, 
                step = 1
            ),
            dbc.Input(
                id = "max-val",
                placeholder = "Enter a number for the max val",
                type = "number", 
                min = 0, 
                step = 1
            ),
            dcc.Graph(
                className = "full-width",
                id = 'custom-heatmap',
                config = config
            ),
            dcc.Graph(
                className = "full-width",
                id = 'custom-summary',
                config = config
            ),  
        ]
    )

def section_three():
    """ Return the two graphs in section three.
    """
    return html.Div(
        className = "container-col container-center full-width",
        children = [

        ]
    )

def tab_six():
    """ Return the contents of tab six."
    """
    return html.Div(
        className = 'continer-col container-center',
        children = [
            section_one(),
            section_two(),
            section_three()
        ]
    )