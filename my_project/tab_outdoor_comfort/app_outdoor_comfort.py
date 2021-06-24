import dash_core_components as dcc
import dash_html_components as html
from my_project.global_scheme import fig_config, tab7_dropdown
from dash.dependencies import Input, Output, State
from my_project.template_graphs import heatmap
import pandas as pd
from my_project.utils import title_with_tooltip

from app import app, cache, TIMEOUT


def layout_outdoor_comfort():
    return html.Div(
        className="container-col",
        children=[
            html.Div(
                className="container-row full-width align-center justify-center",
                children=[
                    html.H3(
                        className="text-next-to-input", children=["Select a variable: "]
                    ),
                    dcc.Dropdown(
                        id="tab7-dropdown",
                        className="dropdown-t-rh",
                        options=[
                            {"label": i, "value": tab7_dropdown[i]}
                            for i in tab7_dropdown
                        ],
                        value="utci_Sun_Wind",
                    ),
                ],
            ),
            html.Div(
                children=title_with_tooltip(
                    text="UTCI heatmap charts",
                    tooltip_text="Heatmap",
                    id_button="utci-charts-label",
                ),
            ),
            dcc.Loading(
                type="circle",
                children=[dcc.Graph(id="utci-heatmap", config=fig_config)],
            ),
            dcc.Loading(
                type="circle",
                children=[dcc.Graph(id="utci-category-heatmap", config=fig_config)],
            ),
        ],
    )


@app.callback(
    Output("utci-heatmap", "figure"),
    [
        Input("tab7-dropdown", "value"),
        Input("df-store", "modified_timestamp"),
        Input("global-local-radio-input", "value"),
    ],
    [State("df-store", "data"), State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_utci_value(var, ts, global_local, df, meta):
    df = pd.read_json(df, orient="split")
    utci_heatmap = heatmap(df, var, global_local)
    return utci_heatmap


@app.callback(
    Output("utci-category-heatmap", "figure"),
    [
        Input("tab7-dropdown", "value"),
        Input("df-store", "modified_timestamp"),
        Input("global-local-radio-input", "value"),
    ],
    [State("df-store", "data"), State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_utci_category(var, ts, global_local, df, meta):
    df = pd.read_json(df, orient="split")
    utci_stress_cat = heatmap(df, var + "_categories", global_local)
    utci_stress_cat["data"][0]["colorbar"] = dict(
        title="Thermal stress",
        titleside="top",
        tickmode="array",
        tickvals=[4, 3, 2, 1, 0, -1, -2, -3, -4, -5],
        ticktext=[
            "extreme heat stress",
            "very strong heat stress",
            "strong heat stress",
            "moderate heat stress",
            "no thermal stress",
            "slight cold stress",
            "moderate cold stress",
            "strong cold stress",
            "very strong cold stress",
            "extreme cold stress",
        ],
        ticks="outside",
    )
    return utci_stress_cat
