import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from .tab_three_graphs import daily_dbt, daily_humidity, monthly_dbt, monthly_humidity, heatmap_dbt, heatmap_humidity


def tab_three():
    return html.Div(
        className = "container-col", 
        children = [
            dcc.Graph(
                figure = daily_dbt(),
                config = config
            ), 
            dcc.Graph(
                figure = daily_humidity(),
                config = config
            ), 
            dcc.Graph(
                figure = monthly_dbt(),
                config = config
            ), 
            dcc.Graph(
                figure = monthly_humidity(), 
                config = config
            ), 
            dcc.Graph(
                figure = heatmap_dbt(),
                config = config
            ), 
            dcc.Graph(
                figure = heatmap_humidity(),
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