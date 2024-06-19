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


# callbrack for Alert solution
@callback(
    Output('alert-auto', 'is_open'),
    Input('interval-component', 'n_intervals')
)
def display_alert(n):
    return n == 1


# callback for Modal solution
# @callback(
#     Output('alert-auto', 'is_open'),
#     [Input('interval-component', 'n_intervals'), Input("close", "n_clicks")],
#     [State('alert-auto', 'is_open')]
# )
# def toggle_alert(n_intervals, n_clicks, is_open):
#     if n_intervals == 1 and not is_open:
#         return True
#     elif n_clicks:
#         return False
#     return is_open


if __name__ == "__main__":
    app.run_server(
        debug=False,
        host="0.0.0.0",
        port=8080,
        processes=1,
        threaded=True,
    )