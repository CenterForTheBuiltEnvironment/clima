import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from extract_df import create_df

app = dash.Dash(__name__)

url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw"
epw_df, location_name = create_df(url)

# Color scheme and templates
DBT_color='Reds'
RH_color='GnBu'
GHrad_color='YlOrRd_r'
Wspeed_color='Blues_r'
template="ggplot2"

# First violin plot 
def create_violin():
    custom_ylim = (-40, 50)
    Title = "Temperature" + " profile<br>" + location_name
    fig = px.violin(data_frame = epw_df, x = None, y = "DBT", template = template, 
        range_y = custom_ylim, height = 1000, width = 350, points = False, box = False, 
        title = Title, labels = dict(DBT = "Temperature (degC)"))
    return fig

def build_banner():
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
    return html.Div([
        dcc.Tabs(
            id = 'tabs-example', 
            value = 'tab-1', 
            children = [
                dcc.Tab(label = 'Select Weather File', value = 'tab-1'),
                dcc.Tab(label = 'Climate Summary', value = 'tab-2'),
                dcc.Tab(label = 'Temperature and Humidity', value = 'tab-3'),
                dcc.Tab(label = 'Sun and Rain', value = 'tab-4'),
                dcc.Tab(label = 'Wind', value = 'tab-5'),
                dcc.Tab(label = 'Outdoor Comfort', value = 'tab-6'),
                dcc.Tab(label = 'Natural Ventilation', value = 'tab-7'),
            ]),
        html.Div(id = 'tabs-example-content')
    ])

@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return html.Div(
            children = [
                html.H3('Tab content 1')
            ]
        )
    elif tab == 'tab-2':
        return html.Div(
            children = [
                html.H3('Tab content 2'),
                dcc.Graph(
                    id = 'example-graph',
                    figure = create_violin()
                )
            ]
        )
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