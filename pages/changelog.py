import dash
import dash_bootstrap_components as dbc
from dash import dcc

dash.register_page(__name__, path='/changelog', name='changelog')

def layout():
    """changelog page"""
    f = open("CHANGELOG.md", "r")

    return dbc.Container(
        className="container p-4",
        children=[dcc.Markdown(f.read())],
    )
