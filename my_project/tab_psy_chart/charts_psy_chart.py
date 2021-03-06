from math import ceil, floor

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pythermalcomfort import psychrometrics as psy

from my_project.global_scheme import (
    template,
    month_lst,
    unit_dict,
    range_dict,
    name_dict,
    color_dict,
    tight_margins,
)


def psych_chart(df, global_local, colorby_var, time_filter_info, data_filter_info):
    """Return the graph for the psychrometric chart"""
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

    var = colorby_var
    if var == "None":
        var_color = "darkorange"
    elif var == "Frequency":
        var_color = ["rgba(255,255,255,0)", "rgb(0,150,255)", "rgb(0,0,150)"]
    else:
        var_unit = str(var) + "_unit"
        var_unit = unit_dict[var_unit]

        var_name = str(var) + "_name"
        var_name = name_dict[var_name]

        var_color = str(var) + "_color"
        var_color = color_dict[var_color]

    if global_local == "global":
        # Set Global values for Max and minimum
        var_range_x = range_dict["DBT_range"]
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
                hovertemplate=name_dict["DBT_name"]
                + ": %{x:.2f}"
                + unit_dict["DBT_unit"],
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
                hovertemplate=name_dict["DBT_name"]
                + ": %{x:.2f}"
                + unit_dict["DBT_unit"]
                + "<br>"
                + name_dict["RH_name"]
                + ": %{customdata[0]:.2f}"
                + unit_dict["RH_unit"]
                + "<br>"
                + name_dict["h_name"]
                + ": %{customdata[1]:.2f}"
                + unit_dict["h_unit"]
                + "<br>"
                + name_dict["t_dp_name"]
                + ": %{customdata[3]:.2f}"
                + unit_dict["t_dp_unit"]
                + "<br>"
                + "<br>"
                + var_name
                + ": %{customdata[2]:.2f}"
                + var_unit,
                name="",
            )
        )
    fig.update_xaxes(range=var_range_x)
    fig.update_yaxes(range=var_range_y)

    fig.update_layout(template=template, margin=tight_margins)
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    return fig
