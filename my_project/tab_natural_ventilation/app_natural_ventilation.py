import math
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
from my_project.global_scheme import (
    template,
    unit_dict,
    range_dict,
    name_dict,
    color_dict,
    fig_config,
    tight_margins,
    month_lst,
    container_row_center_full,
    container_col_center_one_of_three,
)
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from my_project.utils import title_with_tooltip

from app import app, cache, TIMEOUT


def layout_natural_ventilation():
    return html.Div(
        className="container-col",
        children=[
            inputs_tab(),
            dcc.Loading(
                dcc.Graph(
                    id="nv-heatmap-chart",
                    config=fig_config,
                    style={"marginTop": "1rem"},
                ),
                type="circle",
            ),
        ],
    )


def inputs_tab():
    return html.Div(
        className="container-row full-width three-inputs-container",
        children=[
            html.Div(
                className=container_col_center_one_of_three,
                children=[
                    dbc.Button(
                        "Apply filter",
                        color="primary",
                        id="nv-dbt-filter",
                        className="mb-2",
                        n_clicks=1,
                    ),
                    html.H6("Outdoor dry-bulb air temperature range"),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(children=["Min Value:"], style={"flex": "30%"}),
                            dbc.Input(
                                id="nv-tdb-min-val",
                                placeholder="Enter a number for the min val",
                                type="number",
                                step=1,
                                value=10,
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(children=["Max Value:"], style={"flex": "30%"}),
                            dbc.Input(
                                id="nv-tdb-max-val",
                                placeholder="Enter a number for the max val",
                                type="number",
                                value=24,
                                step=1,
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
                        id="nv-month-hour-filter",
                        className="mb-2",
                        n_clicks=0,
                    ),
                    html.Div(
                        className="container-row full-width justify-center mt-2",
                        children=[
                            html.H6("Month Range", style={"flex": "30%"}),
                            html.Div(
                                dcc.RangeSlider(
                                    id="nv-month-slider",
                                    min=1,
                                    max=12,
                                    step=1,
                                    value=[1, 12],
                                    marks={1: "1", 12: "12"},
                                    tooltip={
                                        "always_visible": False,
                                        "placement": "top",
                                    },
                                    allowCross=True,
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
                                    id="nv-hour-slider",
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
                        id="nv-dpt-filter",
                        className="mb-2",
                        n_clicks=0,
                    ),
                    html.H6(
                        "Include condensation risk by specifying below the dew-point temperature (to be used only if radiant systems are present)."
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(children=["Max Value:"], style={"flex": "30%"}),
                            dbc.Input(
                                id="nv-dpt-max-val",
                                placeholder="Enter a number for the max val",
                                type="number",
                                value=16,
                                step=1,
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


@app.callback(
    Output("nv-heatmap-chart", "figure"),
    [
        Input("nv-month-hour-filter", "n_clicks"),
        Input("nv-dbt-filter", "n_clicks"),
        Input("nv-dpt-filter", "n_clicks"),
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("nv-month-slider", "value"),
        State("nv-hour-slider", "value"),
        State("nv-tdb-min-val", "value"),
        State("nv-tdb-max-val", "value"),
        State("nv-dpt-max-val", "value"),
    ],
)
# @cache.memoize(timeout=TIMEOUT)
def nv_heatmap(
    time_filter,
    dbt_data_filter,
    dpt_data_filter,
    global_local,
    df,
    month,
    hour,
    min_dbt_val,
    max_dbt_val,
    max_dpt_val,
):
    df = pd.read_json(df, orient="split")

    start_month, end_month = month
    start_hour, end_hour = hour

    var = "DBT"
    filter_var = "DPT"

    if dbt_data_filter and (min_dbt_val <= max_dbt_val):
        df[(df[var] < min_dbt_val) | (df[var] > max_dbt_val)] = None

    if dpt_data_filter:
        df[(df[filter_var] < -200) | (df[filter_var] > max_dpt_val)] = None

    if time_filter:
        if start_month <= end_month:
            mask = (df["month"] < start_month) | (df["month"] > end_month)
            df[mask] = None
        else:
            mask = (df["month"] >= end_month) & (df["month"] <= start_month)
            df[mask] = None

        if start_hour <= end_hour:
            mask = (df["hour"] < start_hour) | (df["hour"] > end_hour)
            df[mask] = None
        else:
            mask = (df["hour"] >= end_hour) & (df["hour"] <= start_hour)
            df[mask] = None

    var_unit = str(var) + "_unit"
    var_unit = unit_dict[var_unit]

    filter_unit = str(filter_var) + "_unit"
    filter_unit = unit_dict[filter_unit]

    var_range = str(var) + "_range"
    var_range = range_dict[var_range]

    var_name = str(var) + "_name"
    var_name = name_dict[var_name]

    filter_name = str(filter_var) + "_name"
    filter_name = name_dict[filter_name]

    var_color = str(var) + "_color"
    var_color = color_dict[var_color]

    if global_local == "global":
        range_z = var_range
    else:
        data_max = 5 * math.ceil(df[var].max() / 5)
        data_min = 5 * math.floor(df[var].min() / 5)
        range_z = [data_min, data_max]

    title = f"{var_name} ({var_unit})"

    if time_filter:
        title += (
            f" between the months of {month_lst[start_month - 1]} and "
            f"{month_lst[end_month - 1]} and between<br>the hours {start_hour}"
            f":00 and {end_hour}:00"
        )
    if dpt_data_filter:
        title += f" when the {filter_name} is below {max_dpt_val} {filter_unit}."

    fig = go.Figure(
        data=go.Heatmap(
            y=df["hour"],
            x=df["UTC_time"].dt.date,
            z=df[var],
            colorscale=var_color,
            zmin=range_z[0],
            zmax=range_z[1],
            connectgaps=False,
            hoverongaps=False,
            customdata=np.stack((df["month_names"], df["day"]), axis=-1),
            hovertemplate=(
                "<b>"
                + var
                + ": %{z:.2f} "
                + var_unit
                + "</b><br>"
                + "Month: %{customdata[0]}<br>"
                + "Day: %{customdata[1]}<br>"
                + "Hour: %{y}:00<br>"
            ),
            colorbar=dict(title=var_unit),
            name="",
        )
    )

    fig.update_layout(
        template=template,
        title=title,
        yaxis_nticks=13,
        yaxis=dict(range=(1, 24)),
        margin=tight_margins.copy().update({"t": 55}),
    )

    fig.update_xaxes(
        dtick="M1",
        tickformat="%b",
        ticklabelmode="period",
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
        title_text="days of the year",
    )
    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
        title_text="hours of the day",
    )

    return fig
