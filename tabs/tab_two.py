import dash
import dash_core_components as dcc
import dash_html_components as html
import graphs 

def tab_two():
    """ Contents in the second tab 'Climate Summary'.
    """
    return html.Div(
        children = [
            html.Div(
                className = "container-col",
                children = [
                    html.H3('Climate Profiles'),
                    html.Div(
                        className = "container-row",
                        children = [
                            dcc.Graph(
                                id = 'temp-profile-graph',
                                figure = graphs.create_violin_temperature(),
                                config = config
                            ), 
                            dcc.Graph(
                                id = 'humidity-profile-graph',
                                figure = graphs.create_violin_humidity(),
                                config = config
                            ), 
                            dcc.Graph(
                                id = 'solar-radiation-graph',
                                figure = graphs.create_violin_solar(),
                                config = config
                            ), 
                            dcc.Graph(
                                id = 'wind-speed-graph',
                                figure = graphs.create_violin_wind(),
                                config = config
                            )
                        ]
                    )
                ]
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