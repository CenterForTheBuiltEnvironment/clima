import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output

from app import app
from pages.lib.layout import banner, footer, build_tabs #, build_tabs

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

if __name__ == "__main__":
    app.run_server(
        debug=False,
        host="0.0.0.0",
        port=8080,
        processes=1,
        threaded=True,
    )
