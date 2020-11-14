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

@app.callback(Output('df-store', 'data'),
                Output('meta-store', 'data'),
                [Input('submit-button', 'n_clicks')],
                [State('input-url', 'value')])
def submit_button(n_clicks, value):
    if n_clicks is None:
        raise PreventUpdate
    df, meta = create_df(value)
    df = df.to_json(date_format = 'iso', orient = 'split')
    return df, meta

# @app.callback(Output('hidden-div', 'children'),
#                 [Input('df-store', 'modified_timestamp')],
#                 [State('df-store', 'data')])
# def update_url(ts, data):
#     if ts is None:
#         raise PreventUpdate
#     return data