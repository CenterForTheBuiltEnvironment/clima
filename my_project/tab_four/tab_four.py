import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from .tab_four_graphs import polar_solar, lat_long_solar, daily_solar, monthly_solar, horizontal_solar, diffuse_solar, direct_solar, cloud_cover
from my_project.server import app 

def tab_four():
    """ Contents of tab four.
    """
    return html.Div(
        className = "container-col tab-container",
        id = "tab-four-container",
        children = [
            dcc.Dropdown(
                id = "solar-dropdown", 
                options = [
                    {'label': 'Polar', 'value': 'polar'},
                    {'label': 'Latitude/Longitude', 'value': 'lat/long'}
                ], 
                value = 'polar'
            ),
            dcc.Graph(
                id = 'solar-dropdown-output',
                config = config
            ), 
            dcc.Graph(
                id = 'daily-solar',
                config = config
            ), 
            dcc.Graph(
                id = 'monthly-solar',
                config = config
            ), 
            dcc.Graph(
                id = 'horizontal-solar',
                config = config
            ), 
            dcc.Graph(
                id = 'diffuse-solar',
                config = config
            ), 
            dcc.Graph(
                id = 'direct-solar',
                config = config
            ), 
            dcc.Graph(
                id = 'cloud-cover',
                config = config
            )
        ]
    )

@app.callback(
    Output('solar-dropdown-output', 'figure'),
    Output('daily-solar', 'figure'),
    Output('monthly-solar', 'figure'),
    Output('horizontal-solar', 'figure'),
    Output('diffuse-solar', 'figure'),
    Output('direct-solar', 'figure'),
    Output('cloud-cover', 'figure'),
    [Input("solar-dropdown", 'value')],
    [Input('df-store', 'modified_timestamp')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_four(value, ts, df, meta):
    df = pd.read_json(df, orient = 'split')
    if value == 'polar':
        return polar_solar(df, meta), daily_solar(df, meta), monthly_solar(df, meta), horizontal_solar(df, meta), diffuse_solar(df, meta), direct_solar(df, meta), cloud_cover(df, meta)
    else:
        return lat_long_solar(df, meta), daily_solar(df, meta), monthly_solar(df, meta), horizontal_solar(df, meta), diffuse_solar(df, meta), direct_solar(df, meta), cloud_cover(df, meta)


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