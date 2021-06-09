import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def construction():
    return html.Div(
        className="container-col",
        id="construction-container",
        children=[
            html.H4("This tab is under construction."),
            html.P("Come back soon to check it out!"),
        ],
    )
