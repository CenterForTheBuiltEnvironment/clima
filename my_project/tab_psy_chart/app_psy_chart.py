import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from my_project.global_scheme import (
    container_row_center_full,
    container_col_center_one_of_three,
)
from my_project.utils import generate_chart_name

from my_project.global_scheme import dropdown_names
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app, cache, TIMEOUT
from my_project.tab_psy_chart.charts_psy_chart import psych_chart

psy_dropdown_names = {
    "None": "None",
    "Frequency": "Frequency",
}
psy_dropdown_names.update(dropdown_names.copy())


def inputs():
    """"""
    return html.Div(
        className="container-row full-width three-inputs-container",
        children=[
            html.Div(
                className=container_col_center_one_of_three,
                children=[
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(
                                children=["Color By:"],
                                style={"flex": "30%"},
                            ),
                            dcc.Dropdown(
                                id="psy-color-by-dropdown",
                                options=[
                                    {"label": i, "value": psy_dropdown_names[i]}
                                    for i in psy_dropdown_names
                                ],
                                value="Frequency",
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className=container_col_center_one_of_three,
                children=[
                    dbc.Button(
                        "Apply month and hour filter",
                        color="primary",
                        id="month-hour-filter",
                        className="mb-2",
                        n_clicks=0,
                    ),
                    html.Div(
                        className="container-row full-width justify-center mt-2",
                        children=[
                            html.H6("Month Range", style={"flex": "30%"}),
                            html.Div(
                                dcc.RangeSlider(
                                    id="psy-month-slider",
                                    min=1,
                                    max=12,
                                    step=1,
                                    value=[1, 12],
                                    marks={1: "1", 12: "12"},
                                    tooltip={
                                        "always_visible": False,
                                        "placement": "top",
                                    },
                                    allowCross=False,
                                ),
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className="container-row align-center justify-center",
                        children=[
                            html.H6("Hour Range", style={"flex": "30%"}),
                            html.Div(
                                dcc.RangeSlider(
                                    id="psy-hour-slider",
                                    min=1,
                                    max=24,
                                    step=1,
                                    value=[1, 24],
                                    marks={1: "1", 24: "24"},
                                    tooltip={
                                        "always_visible": False,
                                        "placement": "topLeft",
                                    },
                                    allowCross=False,
                                ),
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className=container_col_center_one_of_three,
                children=[
                    dbc.Button(
                        "Apply filter",
                        color="primary",
                        id="data-filter",
                        className="mb-2",
                        n_clicks=0,
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(
                                children=["Filter Variable:"], style={"flex": "30%"}
                            ),
                            dcc.Dropdown(
                                id="psy-var-dropdown",
                                options=[
                                    {"label": i, "value": dropdown_names[i]}
                                    for i in dropdown_names
                                ],
                                value="RH",
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(children=["Min Value:"], style={"flex": "30%"}),
                            dbc.Input(
                                id="psy-min-val",
                                placeholder="Enter a number for the min val",
                                type="number",
                                step=1,
                                value=0,
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(children=["Max Value:"], style={"flex": "30%"}),
                            dbc.Input(
                                id="psy-max-val",
                                placeholder="Enter a number for the max val",
                                type="number",
                                value=100,
                                step=1,
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def layout_psy_chart():
    return (
        dcc.Loading(
            type="circle",
            children=html.Div(
                className="container-col",
                children=[inputs(), html.Div(id="psych-chart")],
            ),
        ),
    )


# TAB NINE: PYSCHROMETRIC CHART
@app.callback(
    Output("psych-chart", "children"),
    [
        Input("psy-color-by-dropdown", "value"),
        Input("month-hour-filter", "n_clicks"),
        Input("data-filter", "n_clicks"),
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("psy-month-slider", "value"),
        State("psy-hour-slider", "value"),
        State("psy-min-val", "value"),
        State("psy-max-val", "value"),
        State("psy-var-dropdown", "value"),
        State("meta-store", "data"),
    ],
)
@cache.memoize(timeout=TIMEOUT)
def update_psych_chart(
    colorby_var,
    time_filter,
    data_filter,
    global_local,
    df,
    month,
    hour,
    min_val,
    max_val,
    data_filter_var,
    meta,
):
    df = pd.read_json(df, orient="split")
    time_filter_info = [time_filter, month, hour]
    data_filter_info = [data_filter, data_filter_var, min_val, max_val]
    return dcc.Graph(
        config=generate_chart_name("psy", meta),
        figure=psych_chart(
            df, global_local, colorby_var, time_filter_info, data_filter_info
        ),
    )
