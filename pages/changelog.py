import dash
import dash_bootstrap_components as dbc
from dash import dcc

from config import PageUrls, FilePaths


dash.register_page(__name__, name="changelog", path=PageUrls.CHANGELOG.value)


def layout():
    """changelog page"""
    with open(FilePaths.CHANGELOG, "r") as f:
        changelog_content = f.read()

    return dbc.Container(
        className="container p-4",
        children=[dcc.Markdown(changelog_content)],
    )
