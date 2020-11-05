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
            dcc.Dropdown(
                id = "solar-dropdown", 
                options = [
                    {'label': 'Polar', 'value': 'polar'},
                    {'label': 'Latitude/Longitude', 'value': 'lat/long'},
                    {'label': 'Daily', 'value': 'daily'}
                ], 
                value = 'polar', 
                searchable = False
            ),
            dcc.Graph(
                id = 'solar-dropdown-output', 
                config = config.config()
            )
        ]
    )
