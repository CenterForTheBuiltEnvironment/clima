import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from graphs import tab_four_graphs
from graphs import config

def tab_four():
    """
    """
    return html.Div(
        className = "container-col",
        children = [
            dcc.Graph(
                figure = tab_four_graphs.lat_long_solar(), 
                config = config.config()
            ), 
            dcc.Graph(
                figure = tab_four_graphs.polar_solar(), 
                config = config.config()
            ), 
            dcc.Graph(
                figure = tab_four_graphs.daily_solar(),
                config = config.config()
            )
        ]
    )
