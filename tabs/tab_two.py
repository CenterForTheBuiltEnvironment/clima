import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from graphs import tab_two_graphs
from graphs import config

def tab_two():
    """ Contents in the second tab 'Climate Summary'.
    """
    print("fail tabs 2")
    return html.Div(
        className = "container-col", 
        children = [
            section_one(), 
            dcc.Graph(
                figure = tab_two_graphs.monthly_dbt(),
                config = config.config()
            ), 
            dcc.Graph(
                figure = tab_two_graphs.monthly_dbt_day_night(),
                config = config.config()
            )
        ]
    )
    
def section_one():
    """
    """
    try:
        return html.Div(
                className = "tab-container",
                children = [
                    html.Div(
                        className = "container-col",
                        children = [
                            climate_profiles_title(), 
                            climate_profiles_graphs()
                        ]
                    )
                ]
            )
    except:
        print("fail section one")

def climate_profiles_title():
    """
    """
    try:
        return html.Div(
                id = "tooltip-title-container",
                className = "container-row",
                children = [
                    html.H5('Climate Profiles'),
                    html.Div([
                        html.Span(
                            "?",
                            id = "tooltip-target",
                            style = {
                                    "textAlign": "center", 
                                    "color": "white"
                            },
                            className = "dot"),
                        dbc.Tooltip(
                            "Some information text",
                            target = "tooltip-target",
                            placement = "right"
                        )
                    ])
                ]
            )
    except:
        print("fail title")

def climate_profiles_graphs():
    """
    """
    try:
        return html.Div(
                className = "container-row",
                children = [
                    dcc.Graph(
                        id = 'temp-profile-graph',
                        figure = tab_two_graphs.temperature(),
                        config = config
                    ), 
                    dcc.Graph(
                        id = 'humidity-profile-graph',
                        figure = tab_two_graphs.humidity(),
                        config = config
                    ), 
                    dcc.Graph(
                        id = 'solar-radiation-graph',
                        figure = tab_two_graphs.solar(),
                        config = config
                    ), 
                    dcc.Graph(
                        id = 'wind-speed-graph',
                        figure = tab_two_graphs.wind(),
                        config = config
                    )
                ]
            )
    except:
        print("fail graphs")