import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from my_project.global_scheme import config, tab4_dropdown_names, tab4_explore_dropdown_names

def custom():
    """ Return the layout for the custom sunpath and its dropdowns.
    """
    return html.Div(
        className = 'container-col full-width',
        id = "tab-four-custom-sun-container",
        children = [
            html.Div(
                className = "container-row container-center full-width",
                children = [
                    html.H6(
                        className = "text-next-to-input",
                        children = ["Variable: "]
                    ),
                    dcc.Dropdown(
                        id = "custom-sun-var-dropdown", 
                        options = [
                            {'label': i, 'value': tab4_dropdown_names[i]} for i in tab4_dropdown_names
                        ], 
                        value = 'DBT'
                    ),
                ]
            ),
            html.Div(
                className = "container-row container-center full-width",
                children = [
                    html.H6(
                        className = "text-next-to-input",
                        children = ["View: "]
                    ),
                    dcc.Dropdown(
                        id = "custom-sun-view-dropdown", 
                        options = [
                            {'label': 'Polar', 'value': 'polar'},
                            {'label': 'Cartesian', 'value': 'cartesian'}
                        ], 
                        value = 'polar'
                    ),
                ]
            ),
            html.Div(
                className = "container-row full-width container-center container-stretch",
                children = [
                    dcc.Loading(
                        type = "circle",
                        children = [
                            dcc.Graph(
                                id = 'custom-sunpath',
                                config = config
                            ), 
                        ]
                    ),
                ]
            ),
        ]
    )

def explore_daily_heatmap():
    """ Contents of the bottom part of the tab"""
    return html.Div(
        className = "container-col full-width",
        children = [
            dcc.Dropdown(
                id = "tab4-explore-dropdown",
                options = [
                    {'label': i, 'value': tab4_explore_dropdown_names[i]} for i in tab4_explore_dropdown_names
                ], 
                value = 'GHrad'
            ),
            dcc.Loading(
                type = "circle",
                children = [
                    dcc.Graph(
                        id = 'tab4-daily',
                        config = config
                    ), 
                ]
            ),
            dcc.Loading(
                type = "circle",
                children = [
                    dcc.Graph(
                        id = 'tab4-heatmap',
                        config = config
                    ), 
                ]
            )
        ]
    )

def static_section():
    return html.Div(
        className = "container-col full-width", 
        children = [
            dcc.Loading(
                type = "circle",
                children = [
                    dcc.Graph(
                        id = 'monthly-solar',
                        config = config
                    ), 
                ]
            ),
            dcc.Loading(
                type = "circle",
                children = [
                    dcc.Graph(
                        id = 'cloud-cover',
                        config = config
                    ), 
                ]
            ),
        ]
    )


def tab_four():
    """ Contents of tab four.
    """
    return html.Div(
        className = "container-col",
        id = "tab-four-container",
        children = [
            custom(),
            static_section(),
            explore_daily_heatmap()
        ]
    )
