import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, no_update
from dash_extensions.enrich import Output, Input, State, callback

from app import app
from pages.lib.layout import banner, footer, build_tabs

server = app.server

app.title = "CBE Clima Tool"
app.layout = dbc.Container(
    fluid=True,
    style={"padding": "0"},
    children=[
        dcc.Location(id="url", refresh=False), # connected to callback below
        banner(),
        html.Div(
            id="page-content",
            children=build_tabs()
        ),    
        footer(),
    ],
)


# callback for survey alert (dbc.Toast)
@callback(
    Output('alert-auto', 'is_open'),
    Input('interval-component', 'n_intervals')
)
def display_alert(n):
    return n == 1


if __name__ == "__main__":
    app.run_server(
        debug=False,
        host="0.0.0.0",
        port=8080,
        processes=1,
        threaded=True,
    )