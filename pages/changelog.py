import dash
import dash_bootstrap_components as dbc
from dash import dcc

from pages.lib.page_urls import PageUrls


dash.register_page(__name__,
                   name='changelog',
                   path=PageUrls.CHANGELOG.value
                   )


def layout():
    """changelog page"""
    f = open("CHANGELOG.md", "r")

    return dbc.Container(
        className="container p-4",
        children=[dcc.Markdown(f.read())],
    )
