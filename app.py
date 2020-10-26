import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from extract_df import create_df

from tabs import tab_one
from tabs import tab_two

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "EPW Viz"

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
                    html.H3(
                        id = "banner-title",
                        children = ["EPW Viz Tool"]),
                    html.H6(
                        id = "banner-subtitle",
                        children = ["Subtitle"]),
                ]
            ),
            html.Div(
                id = "banner-text-right",
                className = "container-col",
                children = [
                    html.H6("Some text"),
                    html.H6("More text"),
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
                parent_className = 'custom-tabs',
                value = 'tab-1', 
                children = [
                    dcc.Tab(
                        label = 'Select Weather File', 
                        value = 'tab-1',
                        className = 'custom-tab',
                        selected_className = 'custom-tab--selected'),
                    dcc.Tab(
                        label = 'Climate Summary', 
                        value = 'tab-2',
                        className = 'custom-tab',
                        selected_className = 'custom-tab--selected'),
                    dcc.Tab(
                        label = 'Temperature/Humidity', 
                        value = 'tab-3',
                        className = 'custom-tab',
                        selected_className = 'custom-tab--selected'),
                    dcc.Tab(
                        label = 'Sun and Rain', 
                        value = 'tab-4',
                        className = 'custom-tab',
                        selected_className = 'custom-tab--selected'),
                    dcc.Tab(
                        label = 'Wind', 
                        value = 'tab-5',
                        className = 'custom-tab',
                        selected_className = 'custom-tab--selected'),
                    dcc.Tab(
                        label = 'Outdoor Comfort', 
                        value = 'tab-6',
                        className='custom-tab',
                        selected_className='custom-tab--selected'),
                    dcc.Tab(
                        label = 'Natural Ventilation', 
                        value = 'tab-7',
                        className = 'custom-tab',
                        selected_className = 'custom-tab--selected'),
                ]
            ),
            html.Div(id = 'tabs-content')
        ]
    )

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return tab_one.tab_one()
    elif tab == 'tab-2':
        return tab_two.tab_two()
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
    app.run_server(debug = True)
    