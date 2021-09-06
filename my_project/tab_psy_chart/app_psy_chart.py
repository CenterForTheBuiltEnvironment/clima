import numpy as np
import plotly.graph_objects as go
from pythermalcomfort import psychrometrics as psy
from math import ceil, floor
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from my_project.global_scheme import (
    container_row_center_full,
    container_col_center_one_of_three,
)
from my_project.utils import generate_chart_name

from my_project.global_scheme import (
    dropdown_names,
    sun_cloud_tab_dropdown_names,
    more_variables_dropdown,
    sun_cloud_tab_explore_dropdown_names,
)
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app

from my_project.global_scheme import (
    template,
    unit_dict,
    range_dict,
    name_dict,
    color_dict,
    tight_margins,
)

psy_dropdown_names = {
    "None": "None",
    "Frequency": "Frequency",
}
psy_dropdown_names.update(dropdown_names.copy())
psy_dropdown_names.update(sun_cloud_tab_dropdown_names.copy())
psy_dropdown_names.update(more_variables_dropdown.copy())
psy_dropdown_names.update(sun_cloud_tab_explore_dropdown_names.copy())


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
                            html.H6("Month Range", style={"flex": "20%"}),
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
                                style={"flex": "50%"},
                            ),
                            dcc.Checklist(
                                options=[
                                    {"label": "Invert", "value": "invert"},
                                ],
                                value=[],
                                id="invert-month-psy",
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
                                style={"flex": "50%"},
                            ),
                            dcc.Checklist(
                                options=[
                                    {"label": "Invert", "value": "invert"},
                                ],
                                value=[],
                                id="invert-hour-psy",
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


# psychrometric chart
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
        State("invert-month-psy", "value"),
        State("invert-hour-psy", "value"),
    ],
)
# @cache.memoize(timeout=TIMEOUT)
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
    invert_month,
    invert_hour,
):
    df = pd.read_json(df, orient="split")
    start_month, end_month = month
    if invert_month == ["invert"] and (start_month != 1 or end_month != 12):
        month = month[::-1]
    start_hour, end_hour = hour
    if invert_hour == ["invert"] and (start_hour != 1 or end_hour != 24):
        hour = hour[::-1]
    time_filter_info = [time_filter, month, hour]
    data_filter_info = [data_filter, data_filter_var, min_val, max_val]

    time_filter = time_filter_info[0]
    start_month = time_filter_info[1][0]
    end_month = time_filter_info[1][1]
    start_hour = time_filter_info[2][0]
    end_hour = time_filter_info[2][1]

    data_filter = data_filter_info[0]
    data_filter_var = data_filter_info[1]
    min_val = data_filter_info[2]
    max_val = data_filter_info[3]

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

    if data_filter:
        if min_val <= max_val:
            mask = (df[data_filter_var] < min_val) | (df[data_filter_var] > max_val)
            df[mask] = None
        else:
            mask = (df[data_filter_var] >= max_val) & (df[data_filter_var] <= min_val)
            df[mask] = None

    if df.dropna().shape[0] == 0:
        return (
            dbc.Alert(
                "No data is available in this location under these conditions. Please "
                "either change the month and hour filters, or select a wider range for "
                "the filter variable",
                color="danger",
                style={"text-align": "center", "marginTop": "2rem"},
            ),
        )

    var = colorby_var
    if var == "None":
        var_color = "darkorange"
    elif var == "Frequency":
        var_color = ["rgba(255,255,255,0)", "rgb(0,150,255)", "rgb(0,0,150)"]
    else:
        var_unit = unit_dict[var]

        var_name = name_dict[var]

        var_color = color_dict[var]

    if global_local == "global":
        # Set Global values for Max and minimum
        var_range_x = range_dict["DBT"]
        hr_range = [0, 0.03]
        var_range_y = hr_range

    else:
        # Set maximum and minimum according to data
        data_max = 5 * ceil(df["DBT"].max() / 5)
        data_min = 5 * floor(df["DBT"].min() / 5)
        var_range_x = [data_min, data_max]

        data_max = (5 * ceil(df["hr"].max() * 1000 / 5)) / 1000
        data_min = (5 * floor(df["hr"].min() * 1000 / 5)) / 1000
        var_range_y = [data_min, data_max]

    title = "Psychrometric Chart"

    if colorby_var != "None" and colorby_var != "Frequency":
        title = title + " colored by " + var_name + " (" + var_unit + ")"

    dbt_list = list(range(-60, 60, 1))
    rh_list = list(range(10, 110, 10))

    rh_df = pd.DataFrame()
    for i, rh in enumerate(rh_list):
        hr_list = np.vectorize(psy.psy_ta_rh)(dbt_list, rh)
        hr_df = pd.DataFrame.from_records(hr_list)
        name = "rh" + str(rh)
        rh_df[name] = hr_df["hr"]

    fig = go.Figure()

    # Add traces
    for i, rh in enumerate(rh_list):
        name = "rh" + str(rh)
        fig.add_trace(
            go.Scatter(
                x=dbt_list,
                y=rh_df[name],
                showlegend=False,
                mode="lines",
                name="",
                hovertemplate="RH " + str(rh) + "%",
                line=dict(width=1, color="lightgrey"),
            )
        )
    if var == "None":
        fig.add_trace(
            go.Scatter(
                x=df["DBT"],
                y=df["hr"],
                showlegend=False,
                mode="markers",
                marker=dict(
                    size=6,
                    color=var_color,
                    showscale=False,
                    opacity=0.2,
                ),
                hovertemplate=name_dict["DBT"] + ": %{x:.2f}" + unit_dict["DBT"],
                name="",
            )
        )
    elif var == "Frequency":
        fig.add_trace(
            go.Histogram2d(
                x=df["DBT"],
                y=df["hr"],
                name="",
                colorscale=var_color,
                hovertemplate="",
                autobinx=False,
                xbins=dict(start=-50, end=60, size=1),
            )
        )
        # fig.add_trace(
        #     go.Scatter(
        #         x=dbt_list,
        #         y=rh_df["rh100"],
        #         showlegend=False,
        #         mode="none",
        #         name="",
        #         fill="toself",
        #         fillcolor="#fff",
        #     )
        # )

    else:
        fig.add_trace(
            go.Scatter(
                x=df["DBT"],
                y=df["hr"],
                showlegend=False,
                mode="markers",
                marker=dict(
                    size=5,
                    color=df[var],
                    showscale=True,
                    opacity=0.3,
                    colorscale=var_color,
                    colorbar=dict(thickness=30, title=var_unit + "<br>  "),
                ),
                customdata=np.stack((df["RH"], df["h"], df[var], df["t_dp"]), axis=-1),
                hovertemplate=name_dict["DBT"]
                + ": %{x:.2f}"
                + unit_dict["DBT"]
                + "<br>"
                + name_dict["RH"]
                + ": %{customdata[0]:.2f}"
                + unit_dict["RH"]
                + "<br>"
                + name_dict["h"]
                + ": %{customdata[1]:.2f}"
                + unit_dict["h"]
                + "<br>"
                + name_dict["t_dp"]
                + ": %{customdata[3]:.2f}"
                + unit_dict["t_dp"]
                + "<br>"
                + "<br>"
                + var_name
                + ": %{customdata[2]:.2f}"
                + var_unit,
                name="",
            )
        )

    fig.update_layout(template=template, margin=tight_margins)
    fig.update_xaxes(
        title_text="Temperature, °C",
        range=var_range_x,
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )
    fig.update_yaxes(
        title_text="Humidity Ratio, kg_water/kg_dry air",
        range=var_range_y,
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )

    return dcc.Graph(config=generate_chart_name("psy", meta), figure=fig)
