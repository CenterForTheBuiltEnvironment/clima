from math import ceil, floor

import json
import numpy as np
import math
import plotly.express as px
import plotly.graph_objects as go
from my_project.global_scheme import template, mapping_dictionary, month_lst


def custom_heatmap(df, global_local, var, time_filter_info, data_filter_info, si_ip):
    """Return the customizable heatmap."""
    time_filter = time_filter_info[0]
    start_month = time_filter_info[1][0]
    end_month = time_filter_info[1][1]
    start_hour = time_filter_info[2][0]
    end_hour = time_filter_info[2][1]
    data_filter = data_filter_info[0]
    filter_var = data_filter_info[1]
    min_val = data_filter_info[2]
    max_val = data_filter_info[3]

    if data_filter:
        if min_val <= max_val:
            mask = (df[filter_var] < min_val) | (df[filter_var] > max_val)
            df[var][mask] = None
        else:
            mask = (df[filter_var] >= max_val) & (df[filter_var] <= min_val)
            df[var][mask] = None

    if df.dropna(subset=[var]).shape[0] == 0:
        return None

    var_unit = mapping_dictionary[var][si_ip]["unit"]
    var_range = mapping_dictionary[var][si_ip]["range"]
    var_name = mapping_dictionary[var]["name"]
    var_color = mapping_dictionary[var]["color"]
    filter_name = mapping_dictionary[filter_var]["name"]
    filter_unit = mapping_dictionary[filter_var][si_ip]["unit"]

    if global_local == "global":
        # Set Global values for Max and minimum
        range_z = var_range
    else:
        # Set maximum and minimum according to data
        data_max = 5 * ceil(df[var].max() / 5)
        data_min = 5 * floor(df[var].min() / 5)
        range_z = [data_min, data_max]

    title = var_name + " (" + var_unit + ")"
    if time_filter:
        title += (
            f" between the months of {month_lst[start_month - 1]} and "
            f"{month_lst[end_month - 1]} and between the hours {start_hour}"
            f":00 and {end_hour}:00"
        )
    if data_filter:
        title += (
            f" when the {filter_name} is between {min_val} and {max_val} {filter_unit}"
        )

    fig = go.Figure(
        data=go.Heatmap(
            y=df["hour"],
            x=df["DOY"],
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
            name="",
            colorbar=dict(title=var_unit),
        )
    )
    fig.update_layout(
        template=template,
        title=title,
        xaxis_nticks=53,
        yaxis_nticks=13,
        yaxis=dict(range=(1, 24)),
        xaxis=dict(range=(1, 365)),
    )
    fig.update_yaxes(title_text="Hour")
    fig.update_xaxes(title_text="Day")
    return fig


def three_var_graph(
    df,
    global_local,
    var_x,
    var_y,
    color_by,
    data_filter_info3,
    si_ip,
):

    """Return the custom graph plotting three variables."""
    data_filter = data_filter_info3[0]
    filter_var = data_filter_info3[1]
    min_val = data_filter_info3[2]
    max_val = data_filter_info3[3]

    var_unit_x = mapping_dictionary[var_x][si_ip]["unit"]
    var_unit_y = mapping_dictionary[var_y][si_ip]["unit"]

    var = color_by
    var_range = mapping_dictionary[var][si_ip]["range"]
    var_color = mapping_dictionary[var]["color"]

    if global_local != "global":
        # Set maximum and minimum according to data
        data_max = 5 * math.ceil(df[var].max() / 5)
        data_min = 5 * math.floor(df[var].min() / 5)
        var_range = [data_min, data_max]

    color_scale = var_color

    if data_filter:
        if min_val <= max_val:
            df.loc[(df[filter_var] < min_val) | (df[filter_var] > max_val)] = None
        else:
            df.loc[(df[filter_var] >= max_val) & (df[filter_var] <= min_val)] = None

    if df.dropna(subset=["month"]).shape[0] == 0:
        return None

    title = (
        mapping_dictionary[var_x]["name"]
        + " vs "
        + mapping_dictionary[var_y]["name"]
        + " colored by "
        + mapping_dictionary[color_by]["name"]
    )

    fig = px.scatter(
        df,
        x=var_x,
        y=var_y,
        color=color_by,
        color_continuous_scale=color_scale,
        opacity=0.4,
        range_color=var_range,
        marginal_x="histogram",
        marginal_y="histogram",
        title=title,
        labels={var_x: f"{var_x} ({var_unit_x})", var_y: f"{var_y} ({var_unit_y})"},
    )

    fig.update_layout(template=template, title=title)
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=False)

    return fig


def two_var_graph(df, var_x, var_y, si_ip):

    title = (
        "Simultaneous frequency of "
        + mapping_dictionary[var_x]["name"]
        + " and  "
        + mapping_dictionary[var_y]["name"]
    )

    var_unit_x = mapping_dictionary[var_x][si_ip]["unit"]
    var_unit_y = mapping_dictionary[var_y][si_ip]["unit"]

    fig = px.density_heatmap(
        df,
        x=var_x,
        y=var_y,
        title=title,
        marginal_x="histogram",
        marginal_y="histogram",
        labels={var_x: f"{var_x} ({var_unit_x})", var_y: f"{var_y} ({var_unit_y})"},
    )
    fig.update_layout(dragmode=False)
    return fig
