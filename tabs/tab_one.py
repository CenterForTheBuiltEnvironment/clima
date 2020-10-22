import dash
import dash_core_components as dcc
import dash_html_components as html

def tab_one():
    """ Contents in the first tab 'Select Weather File'
    """
    return html.Div(
        id = "tab-one-container",
        className = "container-col",
        children = [
            html.Label('Copy paste a link from the map below'),
            dcc.Input(
                id = "input-url",
                value = 'https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw', 
                type = 'text'
            ),
            html.Embed(
                id = "tab-one-map",
                src = "https://www.ladybug.tools/epwmap/"
            )
        ]
    )