import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from my_project.extract_df import create_df

def tab_one():
    """ Contents in the first tab 'Select Weather File'
    """
    return html.Div(
        className = "container-col tab-container",
        children = [
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
                    dbc.Button("Submit", color = "primary", className = "mr-1", id = 'submit-button'),
                ]
            ),
            html.Embed(
                id = "tab-one-map",
                src = "https://www.ladybug.tools/epwmap/"
            ), 
        ]
    )
      
def alert():
    """ Alert layout for the submit button.
    """
    return html.Div(
        [
            dbc.Alert(
                id = "alert",
                dismissable = True,
                is_open = False,
            )
        ]
    )
