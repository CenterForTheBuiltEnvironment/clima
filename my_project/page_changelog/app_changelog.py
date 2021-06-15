import dash_bootstrap_components as dbc
import dash_core_components as dcc


def changelog():
    """changelog page"""
    f = open("CHANGELOG.md", "r")

    return dbc.Container(
        className="container p-4",
        children=[dcc.Markdown(f.read())],
    )
