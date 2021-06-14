import dash_core_components as dcc
import dash_html_components as html
from my_project.global_scheme import config, tab7_dropdown
from dash.dependencies import Input, Output, State
from my_project.template_graphs import heatmap
import pandas as pd

from app import app, cache, TIMEOUT


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


# TAB SEVEN: OUTDOOR COMFORT
@app.callback(
    Output("utci-heatmap", "figure"),
    Output("utci-category-heatmap", "figure"),
    [Input("tab7-dropdown", "value")],
    # General
    [Input("df-store", "modified_timestamp")],
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_seven(var, ts, global_local, df, meta):
    df = pd.read_json(df, orient="split")
    utci_heatmap = heatmap(df, var, global_local)
    utci_stress_cat = heatmap(df, var + "_categories", global_local)
    return utci_heatmap, utci_stress_cat
