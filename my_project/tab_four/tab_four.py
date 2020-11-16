import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

from .tab_four_graphs import polar_solar, lat_long_solar, daily_solar
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
                id = 'solar-dropdown-output'
            ), 
            dcc.Graph(
                id = 'daily-solar'
            )
        ]
    )

# @app.callback(
#     Output('solar-dropdown-output', 'figure'),
#     [Input("solar-dropdown", 'value')]
# )
# def update_tab_four_solar(value):
#     """ Updating the button in tab four to change the solar graph. 
#     """
#     if value == 'polar':
#         return polar_solar()
#     elif value == 'lat/long':
#         return lat_long_solar()
#     else:
#         return daily_solar()

@app.callback(
    Output('solar-dropdown-output', 'figure'),
    Output('daily-solar', 'figure'),
    [Input("solar-dropdown", 'value')],
    [Input('df-store', 'modified_timestamp')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_four(value, ts, df, meta):
    df = pd.read_json(df, orient = 'split')
    if value == 'polar':
        return polar_solar(df, meta), daily_solar(df, meta)
    else:
        return lat_long_solar(df, meta), daily_solar(df, meta)
