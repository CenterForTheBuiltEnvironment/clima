import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from graphs import tab_three_graphs

def tab_three():
    return html.Div(
        className = "container-col", 
        children = [
            dcc.Graph(
                figure = tab_three_graphs.daily_dbt(),
                config = config
            ), 
            dcc.Graph(
                figure = tab_three_graphs.daily_humidity(),
                config = config
            ), 
            dcc.Graph(
                figure = tab_three_graphs.monthly_dbt(),
                config = config
            ), 
            dcc.Graph(
                figure = tab_three_graphs.monthly_humidity(), 
                config = config
            ), 
            dcc.Graph(
                figure = tab_three_graphs.heatmap_dbt(),
                config = config
            ), 
            dcc.Graph(
                figure = tab_three_graphs.heatmap_humidity(),
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