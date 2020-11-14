import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from my_project.server import app 
from my_project.extract_df import create_df

def tab_one():
    """ Contents in the first tab 'Select Weather File'
    """
    return html.Div(
        className = "container-col tab-container",
        children = [
            html.Label('Copy paste a link from the map below'),
            html.Div(
                id = "tab-one-form-container",
                className = "container-row",
                children = [
                    dcc.Input(
                        id = "input-url",
                        value = 'https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw', 
                        type = 'text'
                    ),
                    html.Button("Submit", id = 'submit-button'),
                ]
            ),
            html.Embed(
                id = "tab-one-map",
                src = "https://www.ladybug.tools/epwmap/"
            ), 
            
        ]
    )

@app.callback(Output('session', 'data'),
                [Input('submit-button', 'n_clicks')],
                [State('input-url', 'value')])
def submit_button(n_clicks, value):
    if n_clicks is None:
        raise PreventUpdate
    return value

@app.callback(Output('session-clicks', 'children'),
                [Input('session', 'modified_timestamp')],
                [State('session', 'data')])
def update_url(ts, data):
    if ts is None:
        raise PreventUpdate
    return data


# # add a click to the appropriate store.
# @app.callback(Output('session', 'data'),
#                 [Input('session-button', 'n_clicks')],
#                 [State('session', 'data')])
# def on_click(n_clicks, data):
#     if n_clicks is None:
#         # prevent the None callbacks is important with the store component.
#         # you don't want to update the store for nothing.
#         raise PreventUpdate
#     # Give a default data dict with 0 clicks if there's no data.
#     data = data or {'clicks': 0}
#     data['clicks'] = data['clicks'] + 1
#     return data

# # output the stored clicks in the table cell.
# @app.callback(Output('session-clicks', 'children'),
#                 [Input('session', 'modified_timestamp')],
#                 [State('session', 'data')])
# def on_data(ts, data):
#     if ts is None:
#         raise PreventUpdate
#     data = data or {}
#     return data.get('clicks', 0)