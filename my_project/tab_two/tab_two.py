import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from my_project.server import app 
from .tab_two_graphs import world_map, dbt_violin, humidity_violin, solar_violin, wind_violin

def tab_two():
    """ Contents in the second tab 'Climate Summary'.
    """
    return html.Div(
        className = "container-col", 
        children = [
            dcc.Graph(
                id = "world-map"
            ),
            section_one()
        ]        
    )

# @app.callback(
#     Output('world-map', 'figure'),
#     Output('temp-profile-graph', 'figure'),
#     Output('humidity-profile-graph', 'figure'),
#     Output('solar-radiation-graph', 'figure'),
#     Output('wind-speed-graph', 'figure'),
#     [Input('df-store', 'modified_timestamp')],
#     [State('df-store', 'data')],
#     [State('meta-store', 'data')]
# )
# def update_tab_two(ts, df, meta):
#     df = pd.read_json(df, orient = 'split')
#     return world_map(df, meta), dbt_violin(df, meta), humidity_violin(df, meta), solar_violin(df, meta), wind_violin(df, meta)
    
def section_one():
    """
    """
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

def climate_profiles_title():
    """
    """
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

def climate_profiles_graphs():
    """
    """
    return html.Div(
            id = "tab-two-4-container",
            className = "container-row",
            children = [
                dcc.Graph(
                    id = 'temp-profile-graph',
                    config = config
                ), 
                dcc.Graph(
                    id = 'humidity-profile-graph',
                    config = config
                ), 
                dcc.Graph(
                    id = 'solar-radiation-graph',
                    config = config
                ), 
                dcc.Graph(
                    id = 'wind-speed-graph',
                    config = config
                )
            ]
        )


# Configurations for the graph
config = dict({
    'toImageButtonOptions' : {
        'format': 'svg', 
        'scale': 2 # Multiply title/legend/axis/canvas sizes by this factor
    },
    'displaylogo' : False,
    'modeBarButtonsToRemove' : [
        "zoom2d", 
        "pan2d", 
        "select2d", 
        "lasso2d", 
        "zoomIn2d", 
        "zoomOut2d",
        "hoverClosestCartesian", 
        "hoverCompareCartesian", 
        "zoom3d", 
        "pan3d", 
        "orbitRotation", 
        "tableRotation", 
        "handleDrag3d", 
        "resetCameraDefault3d", 
        "resetCameraLastSave3d", 
        "hoverClosest3d",
        "zoomInGeo", 
        "zoomOutGeo", 
        "resetGeo", 
        "hoverClosestGeo", 
        "hoverClosestGl2d", 
        "hoverClosestPie", 
        "toggleHover", 
        "resetViews"
    ]
  }  
)