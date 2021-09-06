import math
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import plotly.graph_objects as go
from my_project.global_scheme import (
    template,
    unit_dict,
    range_dict,
    name_dict,
    color_dict,
    tight_margins,
    month_lst,
    container_row_center_full,
    container_col_center_one_of_three,
)
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from my_project.utils import title_with_tooltip, generate_chart_name

from app import app


def layout_natural_ventilation():
    return html.Div(
        className="container-col",
        children=[
            inputs_tab(),
            dcc.Loading(
                html.Div(
                    id="nv-heatmap-chart",
                    style={"marginTop": "1rem"},
                ),
                type="circle",
            ),
            html.Div(
                className="container-row align-center justify-center",
                children=[
                    dbc.Checklist(
                        options=[
                            {"label": "", "value": 1},
                        ],
                        value=[1],
                        id="switches-input",
                        switch=True,
                        style={
                            "padding": "1rem",
                            "marginTop": "1rem",
                            "marginRight": "-2rem",
                        },
                    ),
                    html.Div(
                        children=title_with_tooltip(
                            text="Normalize data",
                            tooltip_text="If normalized is enabled it calculates the % "
                            "time otherwise it calculates the total number of hours",
                            id_button="nv_normalize",
                        ),
                    ),
                ],
            ),
            dcc.Loading(
                html.Div(
                    id="nv-bar-chart",
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
                            html.H6("Month Range", style={"flex": "20%"}),
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
                                    allowCross=False,
                                ),
                                style={"flex": "50%"},
                            ),
                            dcc.Checklist(
                                options=[
                                    {"label": "Invert", "value": "invert"},
                                ],
                                value=[],
                                id="invert-month-nv",
                                labelStyle={"flex": "30%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className="container-row align-center justify-center",
                        children=[
                            html.H6("Hour Range", style={"flex": "20%"}),
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
                                    allowCross=False,
                                ),
                                style={"flex": "50%"},
                            ),
                            dcc.Checklist(
                                options=[
                                    {"label": "Invert", "value": "invert"},
                                ],
                                value=[],
                                id="invert-hour-nv",
                                labelStyle={"flex": "30%"},
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
                        disabled=True,
                    ),
                    dbc.Checklist(
                        options=[
                            {
                                "label": "Include condensation risk by specifying below the dew-point temperature (to be used only if radiant systems are present).",
                                "value": 1,
                            },
                        ],
                        value=[],
                        id="enable-condensation",
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(
                                children=["Condensation risk:"],
                                style={"marginRight": "1rem"},
                            ),
                            dbc.Input(
                                id="nv-dpt-max-val",
                                placeholder="Enter a number for the max val",
                                type="number",
                                value=16,
                                step=1,
                                style={"flex": "1"},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


@app.callback(
    Output("nv-heatmap-chart", "children"),
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
        State("meta-store", "data"),
        State("invert-month-nv", "value"),
        State("invert-hour-nv", "value"),
        State("enable-condensation", "value"),
    ],
)
# @cache.memoize(timeout=TIMEOUT)
def nv_heatmap(
    time_filter,
    dbt_data_filter,
    click_dpt_filter,
    global_local,
    df,
    month,
    hour,
    min_dbt_val,
    max_dbt_val,
    max_dpt_val,
    meta,
    invert_month,
    invert_hour,
    condensation_enabled,
):

    # enable or disable button apply filter DPT
    if len(condensation_enabled) == 1:
        dpt_data_filter = True
    else:
        dpt_data_filter = False

    df = pd.read_json(df, orient="split")

    start_month, end_month = month
    if invert_month == ["invert"] and (start_month != 1 or end_month != 12):
        end_month, start_month = month
    start_hour, end_hour = hour
    if invert_hour == ["invert"] and (start_hour != 1 or end_hour != 24):
        end_hour, start_hour = hour

    var = "DBT"
    filter_var = "DPT"

    if dbt_data_filter and (min_dbt_val <= max_dbt_val):
        df.loc[(df[var] < min_dbt_val) | (df[var] > max_dbt_val), var] = None

    if dpt_data_filter:
        df.loc[(df[filter_var] < -200) | (df[filter_var] > max_dpt_val), var] = None

        if df.dropna().shape[0] == 0:
            return (
                dbc.Alert(
                    "Natural ventilation is not available in this location under these "
                    "conditions. Please either select a different outdoor dry-bulb air "
                    "temperature range, change the month and hour filter, or increase the"
                    "dew-point temperature.",
                    color="danger",
                    style={"text-align": "center", "marginTop": "2rem"},
                ),
            )

    if time_filter:
        if start_month <= end_month:
            df.loc[(df["month"] < start_month) | (df["month"] > end_month), var] = None
        else:
            df.loc[
                (df["month"] >= end_month) & (df["month"] <= start_month), var
            ] = None

        if start_hour <= end_hour:
            df.loc[(df["hour"] < start_hour) | (df["hour"] > end_hour), var] = None
        else:
            df.loc[(df["hour"] >= end_hour) & (df["hour"] <= start_hour), var] = None

    var_unit = unit_dict[var]

    filter_unit = unit_dict[filter_var]

    var_range = range_dict[var]

    var_name = str(var) + "_name"
    var_name = name_dict[var_name]

    filter_name = str(filter_var) + "_name"
    filter_name = name_dict[filter_name]

    var_color = color_dict[var]

    if global_local == "global":
        range_z = var_range
    else:
        data_max = 5 * math.ceil(df[var].max() / 5)
        data_min = 5 * math.floor(df[var].min() / 5)
        range_z = [data_min, data_max]

    title = f"Hours when the {var_name} is in the range {min_dbt_val} to {max_dbt_val} {var_unit}"

    if time_filter:
        title += (
            f" between the months of {month_lst[start_month - 1]} and "
            f"{month_lst[end_month - 1]}<br>and between the hours {start_hour}"
            f":00 and {end_hour}:00"
        )
    if dpt_data_filter:
        title += f" and when the {filter_name} is below {max_dpt_val} {filter_unit}."

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

    return dcc.Graph(
        config=generate_chart_name("heatmap_nv", meta),
        figure=fig,
    )


@app.callback(
    Output("nv-bar-chart", "children"),
    [
        Input("nv-month-hour-filter", "n_clicks"),
        Input("nv-dbt-filter", "n_clicks"),
        Input("nv-dpt-filter", "n_clicks"),
        Input("switches-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("nv-month-slider", "value"),
        State("nv-hour-slider", "value"),
        State("nv-tdb-min-val", "value"),
        State("nv-tdb-max-val", "value"),
        State("nv-dpt-max-val", "value"),
        State("meta-store", "data"),
        State("invert-month-nv", "value"),
        State("invert-hour-nv", "value"),
        State("enable-condensation", "value"),
    ],
)
# @cache.memoize(timeout=TIMEOUT)
def nv_bar_chart(
    time_filter,
    dbt_data_filter,
    click_dpt_filter,
    normalize,
    df,
    month,
    hour,
    min_dbt_val,
    max_dbt_val,
    max_dpt_val,
    meta,
    invert_month,
    invert_hour,
    condensation_enabled,
):
    # enable or disable button apply filter DPT
    if len(condensation_enabled) == 1:
        dpt_data_filter = True
    else:
        dpt_data_filter = False

    df = pd.read_json(df, orient="split")

    start_month, end_month = month
    if invert_month == ["invert"] and (start_month != 1 or end_month != 12):
        end_month, start_month = month
    start_hour, end_hour = hour
    if invert_hour == ["invert"] and (start_hour != 1 or end_hour != 24):
        end_hour, start_hour = hour

    var = "DBT"
    filter_var = "DPT"

    var_unit = unit_dict[var]
    filter_unit = unit_dict[filter_var]

    var_name = str(var) + "_name"
    var_name = name_dict[var_name]

    filter_name = str(filter_var) + "_name"
    filter_name = name_dict[filter_name]

    color_in = "dodgerblue"

    df["nv_allowed"] = 1

    if time_filter:
        if start_month <= end_month:
            df.loc[
                (df["month"] < start_month) | (df["month"] > end_month), "nv_allowed"
            ] = 0
        else:
            df.loc[
                (df["month"] >= end_month) & (df["month"] <= start_month), "nv_allowed"
            ] = 0

        if start_hour <= end_hour:
            df.loc[
                (df["hour"] < start_hour) | (df["hour"] > end_hour), "nv_allowed"
            ] = 0
        else:
            df.loc[
                (df["hour"] >= end_hour) & (df["hour"] <= start_hour), "nv_allowed"
            ] = 0

    # this should be the total after filtering by time
    tot_month_hours = df.groupby(df["UTC_time"].dt.month)["nv_allowed"].sum().values

    if dbt_data_filter and (min_dbt_val <= max_dbt_val):
        df.loc[(df[var] < min_dbt_val) | (df[var] > max_dbt_val), "nv_allowed"] = 0

    if dpt_data_filter:
        df.loc[(df[filter_var] > max_dpt_val), "nv_allowed"] = 0

    n_hours_nv_allowed = (
        df.dropna().groupby(df["UTC_time"].dt.month)["nv_allowed"].sum().values
    )

    per_time_nv_allowed = np.round(100 * (n_hours_nv_allowed / tot_month_hours))

    if len(normalize) == 0:
        fig = go.Figure(
            go.Bar(
                x=df["month_names"].unique(),
                y=n_hours_nv_allowed,
                name="",
                marker_color=color_in,
                customdata=np.stack((n_hours_nv_allowed, per_time_nv_allowed), axis=-1),
                hovertemplate=(
                    "natural ventilation possible for: <br>%{customdata[0]} hrs or <br>%{"
                    "customdata[1]}% of selected time<br>"
                ),
            )
        )

        title = (
            f"Number of hours the {var_name}"
            + f" is in the range {min_dbt_val}"
            + f" to "
            + f" {max_dbt_val} {var_unit}"
        )
        fig.update_yaxes(title_text="hours", range=[0, 744])

    else:
        trace1 = go.Bar(
            x=df["month_names"].unique(),
            y=per_time_nv_allowed,
            name="",
            marker_color=color_in,
            customdata=np.stack((n_hours_nv_allowed, per_time_nv_allowed), axis=-1),
            hovertemplate=(
                "natural ventilation possible for: <br>%{customdata[0]} hrs or <br>%{"
                "customdata[1]}% of selected time<br>"
            ),
        )

        fig = go.Figure(data=trace1)

        title = (
            f"Percentage of hours the {var_name}"
            + f" is in the range {min_dbt_val}"
            + f" to {max_dbt_val}"
            + f" {var_unit}"
        )
        fig.update_yaxes(title_text="% percent", range=[0, 100])

    if time_filter:
        title += (
            f" between the months of {month_lst[start_month - 1]} and "
            f"{month_lst[end_month - 1]} and between<br>the hours {start_hour}"
            f":00 and {end_hour}:00"
        )
    if dpt_data_filter:
        title += f" when the {filter_name} is below {max_dpt_val} {filter_unit}."

    fig.update_layout(
        template=template,
        title=title,
        barnorm="",
        dragmode=False,
        margin=tight_margins.copy().update({"t": 55}),
    )

    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)

    return dcc.Graph(
        config=generate_chart_name("bar_chart_nv", meta),
        figure=fig,
    )


@app.callback(
    Output("nv-dpt-filter", "disabled"), Input("enable-condensation", "value")
)
def enable_disable_button_data_filter(state_checklist):
    if len(state_checklist) == 1:
        return False
    else:
        return True
