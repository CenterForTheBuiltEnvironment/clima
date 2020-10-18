import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from extract_df import create_df
import graphs

app = dash.Dash(__name__)

def build_banner():
    """ Build the banner at the top of the page.
    """
    return html.Div(
        id = "banner",
        className = "container-row",
        children = [
            html.Div(
                id = "banner-text-left",
                className = "container-col",
                children = [
                    html.H1("EPW Viz Tool"),
                    html.H4("Subtitle"),
                ]
            ),
            html.Div(
                id = "banner-text-right",
                className = "container-col",
                children = [
                    html.H4("Some text"),
                    html.H4("More text"),
                ]
            )
        ]
    )

def build_tabs():
    """ Build the seven different tabs. 
    """
    return html.Div(
        id = "tabs-container",
        children = [
            dcc.Tabs(
                id = 'tabs', 
                value = 'tab-1', 
                children = [
                    dcc.Tab(label = 'Select Weather File', value = 'tab-1'),
                    dcc.Tab(label = 'Climate Summary', value = 'tab-2'),
                    dcc.Tab(label = 'Temperature and Humidity', value = 'tab-3'),
                    dcc.Tab(label = 'Sun and Rain', value = 'tab-4'),
                    dcc.Tab(label = 'Wind', value = 'tab-5'),
                    dcc.Tab(label = 'Outdoor Comfort', value = 'tab-6'),
                    dcc.Tab(label = 'Natural Ventilation', value = 'tab-7'),
                ]
            ),
            html.Div(id = 'tabs-content')
        ]
    )

def tab_one():
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

def tab_two():
    return html.Div(
            children = [
                html.Div(
                    className = "container-col",
                    children = [
                        html.H3('Climate Profiles'),
                        html.Div(
                            className = "container-row",
                            children = [
                                dcc.Graph(
                                    id = 'temp-profile-graph',
                                    figure = graphs.create_violin_temperature()
                                ), 
                                dcc.Graph(
                                    id = 'humidity-profile-graph',
                                    figure = graphs.create_violin_humidity()
                                ), 
                                dcc.Graph(
                                    id = 'solar-radiation-graph',
                                    figure = graphs.create_violin_solar()
                                ), 
                                dcc.Graph(
                                    id = 'wind-speed-graph',
                                    figure = graphs.create_violin_wind()
                                )
                            ]
                        )
                    ]
                )
            ]
        )

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return tab_one()
    elif tab == 'tab-2':
        return tab_two()
    elif tab == 'tab-3':
        return html.Div(
            children = [
                html.H3('Tab content 3')
            ]
        )
    elif tab == 'tab-4':
        return html.Div(
            children = [
                html.H3('Tab content 4')
            ]
        )
    elif tab == 'tab-5':
        return html.Div(
            children = [
                html.H3('Tab content 5')
            ]
        )
    elif tab == 'tab-6':
        return html.Div(
            children = [
            html.H3('Tab content 6')
            ]
        )
    elif tab == 'tab-7':
        return html.Div(
            children = [
            html.H3('Tab content 7')
            ]
        )

app.layout = html.Div(
    id = 'big-container',
    children = [
        build_banner(),
        build_tabs()
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)