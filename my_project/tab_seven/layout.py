import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from my_project.global_scheme import config, tab7_dropdown


def tab_seven():
    """Return the contents for tab 7."""
    return html.Div(
        className="container-col",
        children=[
            dcc.Dropdown(
                id="tab7-dropdown",
                options=[
                    {"label": i, "value": tab7_dropdown[i]} for i in tab7_dropdown
                ],
                value="utci_Sun_Wind",
            ),
            dcc.Loading(
                type="circle", children=[dcc.Graph(id="utci-heatmap", config=config)]
            ),
            dcc.Loading(
                type="circle",
                children=[dcc.Graph(id="utci-category-heatmap", config=config)],
            ),
        ],
    )
