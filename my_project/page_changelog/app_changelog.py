import dash_bootstrap_components as dbc
from dash import dcc


def changelog():
    """changelog page"""
    f = open("CHANGELOG.md", "r")

    return dbc.Container(
        className="container p-4",
        children=[dcc.Markdown(f.read())],
    )
