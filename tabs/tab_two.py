import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from graphs import tab_two_graphs

def tab_two():
    """ Contents in the second tab 'Climate Summary'.
    """
    return html.Div(
        className = "container-col", 
        children = [
            section_one(), 
            dcc.Graph(
                figure = tab_two_graphs.monthly_dbt(),
                config = config
            ), dcc.Graph(
                figure = tab_two_graphs.monthly_dbt_day_night(),
                config = config
            )
        ]
    )
    
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