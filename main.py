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


# @app.callback(
#     dash.dependencies.Output("page-content", "children"),
#     [dash.dependencies.Input("url", "pathname")],
# )
# def display_page(pathname):
#     if pathname == "/":
#         return build_tabs()
#     elif pathname == "/changelog":
#         return html.Div(children=[changelog()])


# # Handle tab selection
# @app.callback(
#     Output("tabs-content", "children"),
#     [
#         Input("tabs", "value"),
#         Input("si-ip-radio-input", "value"),
#     ],
# )
# def render_content(tab, si_ip):
#     """Update the contents of the page depending on what tab the user selects."""
#     if tab == "tab-select":
#         return layout_select()
#     elif tab == "tab-summary":
#         return layout_summary(si_ip)
#     elif tab == "tab-t-rh":
#         return layout_t_rh()
#     elif tab == "tab-sun":
#         return layout_sun(si_ip)
#     elif tab == "tab-wind":
#         return layout_wind()
#     elif tab == "tab-data-explorer":
#         return layout_data_explorer()
#     elif tab == "tab-outdoor-comfort":
#         return layout_outdoor_comfort()
#     elif tab == "tab-natural-ventilation":
#         return layout_natural_ventilation(si_ip)
#     elif tab == "tab-psy-chart":
#         return layout_psy_chart()
#     else:
#         return "404"


if __name__ == "__main__":
    app.run_server(
        debug=False,
        host="0.0.0.0",
        port=8080,
        processes=1,
        threaded=True,
    )
