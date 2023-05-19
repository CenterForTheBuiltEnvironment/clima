import numpy as np
import plotly.graph_objects as go
import json
from pythermalcomfort import psychrometrics as psy
from math import ceil, floor
import dash_bootstrap_components as dbc
from copy import deepcopy
from dash import dcc
from dash import html
from my_project.global_scheme import (
    container_row_center_full,
    container_col_center_one_of_three,
)
from my_project.template_graphs import filter_df_by_month_and_hour
from my_project.utils import (
    generate_chart_name,
    generate_units,
    generate_custom_inputs_psy,
    determine_month_and_hour_filter,
    title_with_link,
)
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
    mapping_dictionary,
    tight_margins,
)

psy_dropdown_names = {
    "None": "None",
    "Frequency": "Frequency",
}
psy_dropdown_names.update(deepcopy(dropdown_names))
psy_dropdown_names.update(deepcopy(sun_cloud_tab_dropdown_names))
psy_dropdown_names.update(deepcopy(more_variables_dropdown))
psy_dropdown_names.update(deepcopy(sun_cloud_tab_explore_dropdown_names))
psy_dropdown_names.pop("Elevation", None)
psy_dropdown_names.pop("Azimuth", None)
psy_dropdown_names.pop("Saturation pressure", None)


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
                                persistence_type="session",
                                persistence=True,
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
                                    min=0,
                                    max=24,
                                    step=1,
                                    value=[0, 24],
                                    marks={0: "0", 24: "24"},
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
        html.Div(
            children=title_with_link(
                text="Psychrometric Chart",
                id_button="Psychrometric-Chart-chart",
                doc_link="https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/psychrometric-chart",
            ),
        ),
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
        Input("df-store", "modified_timestamp"),
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
        State("si-ip-unit-store", "data"),
    ],
)
def update_psych_chart(
    ts,
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
    si_ip,
):

    start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
        month, hour, invert_month, invert_hour
    )

    df = filter_df_by_month_and_hour(
        df, time_filter, month, hour, invert_month, invert_hour, df.columns
    )

    if data_filter:
        if min_val <= max_val:
            mask = (df[data_filter_var] < min_val) | (df[data_filter_var] > max_val)
            df[mask] = None
        else:
            mask = (df[data_filter_var] >= max_val) & (df[data_filter_var] <= min_val)
            df[mask] = None

    if df.dropna(subset=["month"]).shape[0] == 0:
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
        var_unit = mapping_dictionary[var][si_ip]["unit"]

        var_name = mapping_dictionary[var]["name"]

        var_color = mapping_dictionary[var]["color"]

    if global_local == "global":
        # Set Global values for Max and minimum
        var_range_x = mapping_dictionary["DBT"][si_ip]["range"]
        var_range_y = mapping_dictionary["hr"][si_ip]["range"]

    else:
        # Set maximum and minimum according to data
        data_max = 5 * ceil(df["DBT"].max() / 5)
        data_min = 5 * floor(df["DBT"].min() / 5)
        var_range_x = [data_min, data_max]

        data_max = round(df["hr"].max(), 4)
        data_min = round(df["hr"].min(), 4)
        var_range_y = [data_min * 1000, data_max * 1000]

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

        dbt_list_convert = list(dbt_list)
        rh_multiply = list(rh_df[name])

        for k in range(len(rh_df[name])):
            rh_multiply[k] = rh_multiply[k] * 1000

        if si_ip == "ip":
            for j in range(len(dbt_list)):
                dbt_list_convert[j] = dbt_list_convert[j] * 1.8 + 32

        fig.add_trace(
            go.Scatter(
                x=dbt_list_convert,
                y=rh_multiply,
                showlegend=False,
                mode="lines",
                name="",
                hovertemplate="RH " + str(rh) + "%",
                line=dict(width=1, color="lightgrey"),
            )
        )

    df_hr_multiply = list(df["hr"])
    for k in range(len(df_hr_multiply)):
        df_hr_multiply[k] = df_hr_multiply[k] * 1000
    if var == "None":
        fig.add_trace(
            go.Scatter(
                x=df["DBT"],
                y=df_hr_multiply,
                showlegend=False,
                mode="markers",
                marker=dict(
                    size=6,
                    color=var_color,
                    showscale=False,
                    opacity=0.2,
                ),
                hovertemplate=mapping_dictionary["DBT"]["name"]
                + ": %{x:.2f}"
                + mapping_dictionary["DBT"]["name"],
                name="",
            )
        )
    elif var == "Frequency":
        fig.add_trace(
            go.Histogram2d(
                x=df["DBT"],
                y=df_hr_multiply,
                name="",
                colorscale=var_color,
                hovertemplate="",
                autobinx=False,
                xbins=dict(start=-50, end=100, size=1),
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
        var_colorbar = dict(
            thickness=30,
            title=var_unit + "<br>  ",
        )

        if var_unit == "Thermal stress":
            var_colorbar["tickvals"] = [4, 3, 2, 1, 0, -1, -2, -3, -4, -5]
            var_colorbar["ticktext"] = [
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
            ]

        fig.add_trace(
            go.Scatter(
                x=df["DBT"],
                y=df_hr_multiply,
                showlegend=False,
                mode="markers",
                marker=dict(
                    size=5,
                    color=df[var],
                    showscale=True,
                    opacity=0.3,
                    colorscale=var_color,
                    colorbar=var_colorbar,
                ),
                customdata=np.stack((df["RH"], df["h"], df[var], df["t_dp"]), axis=-1),
                hovertemplate=mapping_dictionary["DBT"]["name"]
                + ": %{x:.2f}"
                + mapping_dictionary["DBT"][si_ip]["unit"]
                + "<br>"
                + mapping_dictionary["RH"]["name"]
                + ": %{customdata[0]:.2f}"
                + mapping_dictionary["RH"][si_ip]["unit"]
                + "<br>"
                + mapping_dictionary["h"]["name"]
                + ": %{customdata[1]:.2f}"
                + mapping_dictionary["h"][si_ip]["unit"]
                + "<br>"
                + mapping_dictionary["t_dp"]["name"]
                + ": %{customdata[3]:.2f}"
                + mapping_dictionary["t_dp"][si_ip]["unit"]
                + "<br>"
                + "<br>"
                + var_name
                + ": %{customdata[2]:.2f}"
                + var_unit,
                name="",
            )
        )

    xtitle_name = "Temperature" + "  " + mapping_dictionary["DBT"][si_ip]["unit"]
    ytitle_name = "Humidity Ratio" + "  " + mapping_dictionary["hr"][si_ip]["unit"]
    fig.update_layout(template=template, margin=tight_margins)
    fig.update_xaxes(
        title_text=xtitle_name,
        range=var_range_x,
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )
    fig.update_yaxes(
        title_text=ytitle_name,
        range=var_range_y,
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )
    custom_inputs = generate_custom_inputs_psy(
        start_month,
        end_month,
        start_hour,
        end_hour,
        colorby_var,
        data_filter_var,
        min_val,
        max_val,
    )
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name("psy", meta, custom_inputs, units), figure=fig
    )
