import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output

from app import app
from pages.lib.layout import banner, footer, store #, build_tabs

server = app.server

app.title = "CBE Clima Tool"
app.layout = dbc.Container(
    fluid=True,
    style={"padding": "0"},
    children=[
        dcc.Location(id="url", refresh=False), # connected to callback below
        banner(),
        dbc.Nav(
            [
                dbc.NavLink(
                    html.Div(page["name"], className="ms-2"),
                    href=page["path"],
                    active="exact",
                    style={'color':'white'}
                )
                for page in dash.page_registry.values() if page["name"] not in ["404", "changelog"]
            ],
            pills=True,
            justified=True,
            style={'background-color': '#003262',
                   'padding': '0.25rem 0.5rem',
                } 
        ),
        html.Div(id="store-container", children=[store()]),
        dash.page_container,
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
