import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from my_project.global_scheme import (
    fig_config,
    container_row_center_full,
    container_col_center_one_of_three,
)

from my_project.global_scheme import dropdown_names
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app, cache, TIMEOUT
from my_project.tab_psy_chart.charts_psy_chart import psych_chart


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
                                className="text-next-to-input", children=["Color By:"]
                            ),
                            dcc.Dropdown(
                                className="tab9-sec3-dropdown",
                                id="tab9-colorby-dropdown",
                                options=[
                                    {"label": i, "value": dropdown_names[i]}
                                    for i in dropdown_names
                                ],
                                value="None",
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className=container_col_center_one_of_three,
                children=[
                    dbc.Checklist(
                        options=[
                            {"label": "Apply Time Filters", "value": "time"},
                        ],
                        value=[],
                        id="tab9-sec3-time-filter-input",
                    ),
                    html.Div(
                        className="container-row full-width container-center",
                        children=[
                            html.H6("Month Range"),
                            dcc.RangeSlider(
                                id="tab9-sec3-query-month-slider",
                                min=1,
                                max=12,
                                step=1,
                                value=[1, 12],
                                marks={1: "1", 12: "12"},
                                tooltip={"always_visible": False, "placement": "top"},
                                allowCross=True,
                            ),
                        ],
                    ),
                    html.Div(
                        className="container-row full-width container-center",
                        children=[
                            html.H6("Hour Range"),
                            dcc.RangeSlider(
                                id="tab9-sec3-query-hour-slider",
                                min=1,
                                max=24,
                                step=1,
                                value=[1, 24],
                                marks={1: "1", 24: "24"},
                                tooltip={
                                    "always_visible": False,
                                    "placement": "topLeft",
                                },
                                allowCross=True,
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className=container_col_center_one_of_three,
                children=[
                    dbc.Checklist(
                        options=[
                            {"label": "Apply Data Filters", "value": "data"},
                        ],
                        value=[],
                        id="tab9-sec3-data-filter-input",
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(
                                className="text-next-to-input",
                                children=["Filter Variable:"],
                            ),
                            dcc.Dropdown(
                                className="tab9-sec3-dropdown",
                                id="tab9-sec3-filter-var-dropdown",
                                options=[
                                    {"label": i, "value": dropdown_names[i]}
                                    for i in dropdown_names
                                ],
                                value="RH",
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(
                                className="text-next-to-input", children=["Min Value:"]
                            ),
                            dbc.Input(
                                className="num-input",
                                id="tab9-sec3-min-val",
                                placeholder="Enter a number for the min val",
                                type="number",
                                min=0,
                                step=1,
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(
                                className="text-next-to-input", children=["Max Value:"]
                            ),
                            dbc.Input(
                                className="num-input",
                                id="tab9-sec3-max-val",
                                placeholder="Enter a number for the max val",
                                type="number",
                                min=0,
                                step=1,
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
                children=[inputs(), dcc.Graph(id="psych-chart", config=fig_config)],
            ),
        ),
    )


# TAB NINE: PYSCHROMETRIC CHART
@app.callback(
    Output("psych-chart", "figure"),
    # Sec1 Inputs
    [Input("tab9-colorby-dropdown", "value")],
    # Sec2 Inputs
    [Input("tab9-sec3-time-filter-input", "value")],
    [Input("tab9-sec3-query-month-slider", "value")],
    [Input("tab9-sec3-query-hour-slider", "value")],
    # Sec3 Inputs
    [Input("tab9-sec3-data-filter-input", "value")],
    [Input("tab9-sec3-filter-var-dropdown", "value")],
    [Input("tab9-sec3-min-val", "value")],
    [Input("tab9-sec3-max-val", "value")],
    # General
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_psych_chart(
    colorby_var,
    time_filter,
    month,
    hour,
    data_filter,
    data_filter_var,
    min_val,
    max_val,
    global_local,
    df,
):
    df = pd.read_json(df, orient="split")
    time_filter_info = [time_filter, month, hour]
    data_filter_info = [data_filter, data_filter_var, min_val, max_val]
    fig = psych_chart(df, global_local, colorby_var, time_filter_info, data_filter_info)
    return fig
