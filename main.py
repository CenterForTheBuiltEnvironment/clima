import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_extensions.enrich import Output, Input, callback

from app import app
from pages.lib.layout import banner, footer, build_tabs
from config import AppConfig

server = app.server

app.title = AppConfig.TITLE
app.layout = dbc.Container(
    fluid=True,
    style={"padding": "0"},
    children=[
        dcc.Location(id="url", refresh=False),  # connected to callback below
        banner(),
        html.Div(id="page-content", children=build_tabs()),
        footer(),
    ],
)


# callback for survey alert (dbc.Toast)
@callback(Output("alert-auto", "is_open"), Input("interval-component", "n_intervals"))
def display_alert(n):
    return n == 1


if __name__ == "__main__":
    app.run_server(
        debug=AppConfig.DEBUG,
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        processes=AppConfig.PROCESSES,
        threaded=AppConfig.THREADED,
    )
