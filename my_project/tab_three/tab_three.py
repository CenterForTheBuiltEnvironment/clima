import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from my_project.server import app
from .tab_three_graphs import daily_dbt, daily_humidity, monthly_dbt3, monthly_humidity, heatmap_dbt, heatmap_humidity

def tab_three():
    return html.Div(
        className = "container-col", 
        children = [
            dcc.Graph(
                id = 'daily-dbt',
                config = config
            ), 
            dcc.Graph(
                id = 'daily-humidity',
                config = config
            ), 
            dcc.Graph(
                id = 'monthly-dbt-3',
                config = config
            ), 
            dcc.Graph(
                id = 'monthly-humidity',
                config = config
            ), 
            dcc.Graph(
                id = 'heatmap-dbt',
                config = config
            ), 
            dcc.Graph(
                id = 'heatmap-humidity',
                config = config
            )
        ]
    )

@app.callback(
    Output('daily-dbt', 'figure'),
    Output('daily-humidity', 'figure'),
    Output('monthly-dbt-3', 'figure'),
    Output('monthly-humidity', 'figure'),
    Output('heatmap-dbt', 'figure'),
    Output('heatmap-humidity', 'figure'),
    [Input('df-store', 'modified_timestamp')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_three(ts, df, meta):
    df = pd.read_json(df, orient = 'split')
    return daily_dbt(df, meta), daily_humidity(df, meta), monthly_dbt3(df, meta), monthly_humidity(df, meta), heatmap_dbt(df, meta), heatmap_humidity(df, meta)

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