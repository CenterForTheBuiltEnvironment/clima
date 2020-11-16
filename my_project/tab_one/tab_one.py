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
            alert(),
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
      
def alert():
    return html.Div(
        [
            dbc.Alert(
                id = "alert",
                dismissable = True,
                is_open = False,
            )
        ]
    )

@app.callback(Output('df-store', 'data'),
                Output('meta-store', 'data'),
                [Input('submit-button', 'n_clicks')],
                [State('input-url', 'value')])
def submit_button(n_clicks, value):
    try:
        if n_clicks is None:
            raise PreventUpdate
        df, meta = create_df(value)
        df = df.to_json(date_format = 'iso', orient = 'split')
        return df, meta
    except:
        return None, None

@app.callback(Output("alert", 'is_open'),
                Output("alert", 'children'),
                Output("alert", "color"),
                [Input('df-store', 'data')],
                [Input('submit-button', 'n_clicks')])
def alert_display(data, n_clicks):
    if n_clicks is  None:
        raise PreventUpdate
    if data is None and n_clicks > 0:
        return True, "This link is not available. Please choose another one.", "warning"
    else:
        return True, "Successfully loaded data. Check out the other tabs!", "success"

