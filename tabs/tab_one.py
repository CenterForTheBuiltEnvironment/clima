import dash
import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc

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
                    dbc.Button("Submit", color = "primary", className = "mr-1"),
                ]
            ),
            html.Embed(
                id = "tab-one-map",
                src = "https://www.ladybug.tools/epwmap/"
            )
        ]
    )