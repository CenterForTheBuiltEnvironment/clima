import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pages.lib.utils import get_max_min_value
from pages.lib.global_scheme import template, month_lst
from pages.lib.global_variables import Variables, VariableInfo


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

    variable = VariableInfo.from_col_name(var)
    filter_variable = VariableInfo.from_col_name(filter_var)

    var_name = variable.get_name()
    var_unit = variable.get_unit(si_ip)
    var_range = variable.get_range(si_ip)
    var_color = variable.get_color()

    filter_name = filter_variable.get_name()
    filter_unit = filter_variable.get_unit(si_ip)

    if global_local == "global":
        # Set Global values for Max and minimum
        range_z = var_range
    else:
        # Set maximum and minimum according to data
        data_max, data_min = get_max_min_value(df[var])
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

    fig = go.Figure()

    has_filter_marker = "_is_filtered" in df.columns

    if has_filter_marker and df["_is_filtered"].any():
        filtered_mask = df["_is_filtered"]
        if filtered_mask.any():
            original_col = f"_{var}_original"
            if original_col in df.columns:
                filtered_z = df[original_col].copy()
            else:
                filtered_z = df[var].copy()

            filtered_z[~filtered_mask] = None

            fig.add_trace(
                go.Heatmap(
                    y=df[Variables.HOUR.col_name],
                    x=df[Variables.DOY.col_name],
                    z=filtered_z,
                    colorscale=[[0, "lightgray"], [1, "gray"]],
                    zmin=range_z[0],
                    zmax=range_z[1],
                    showscale=False,
                    connectgaps=False,
                    hoverongaps=False,
                    customdata=np.stack(
                        (df[Variables.MONTH.col_name], df[Variables.DAY.col_name]),
                        axis=-1,
                    ),
                    hovertemplate=(
                        "<b>Filtered Data</b><br>"
                        + "Month: %{customdata[0]}<br>Day: %{customdata[1]}<br>Hour:"
                        " %{y}:00<br>"
                    ),
                    name="filtered",
                )
            )

        normal_mask = ~filtered_mask
        normal_z = df[var].copy()
        normal_z[filtered_mask] = None

        fig.add_trace(
            go.Heatmap(
                y=df[Variables.HOUR.col_name],
                x=df[Variables.DOY.col_name],
                z=normal_z,
                colorscale=var_color,
                zmin=range_z[0],
                zmax=range_z[1],
                connectgaps=False,
                hoverongaps=False,
                customdata=np.stack(
                    (df[Variables.MONTH.col_name], df[Variables.DAY.col_name]), axis=-1
                ),
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
    else:
        fig.add_trace(
            go.Heatmap(
                y=df[Variables.HOUR.col_name],
                x=df[Variables.DOY.col_name],
                z=df[var],
                colorscale=var_color,
                zmin=range_z[0],
                zmax=range_z[1],
                connectgaps=False,
                hoverongaps=False,
                customdata=np.stack(
                    (df[Variables.MONTH_NAMES.col_name], df[Variables.DAY.col_name]),
                    axis=-1,
                ),
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

    variable_x = VariableInfo.from_col_name(var_x)
    variable_y = VariableInfo.from_col_name(var_y)
    variable_color = VariableInfo.from_col_name(color_by)

    var_unit_x = variable_x.get_unit(si_ip)
    var_unit_y = variable_y.get_unit(si_ip)
    var_range = variable_color.get_range(si_ip)
    var_color = variable_color.get_color()

    var = color_by

    if global_local != "global":
        # Set maximum and minimum according to data
        data_max, data_min = get_max_min_value(df[var])
        var_range = [data_min, data_max]

    color_scale = var_color

    if data_filter:
        if min_val <= max_val:
            df.loc[(df[filter_var] < min_val) | (df[filter_var] > max_val)] = None
        else:
            df.loc[(df[filter_var] >= max_val) & (df[filter_var] <= min_val)] = None

    if df.dropna(subset=[Variables.MONTH.col_name]).shape[0] == 0:
        return None

    title = (
        variable_x.get_name()
        + " vs "
        + variable_y.get_name()
        + " colored by "
        + variable_color.get_name()
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
    variable_x = VariableInfo.from_col_name(var_x)
    variable_y = VariableInfo.from_col_name(var_y)

    title = (
        "Simultaneous frequency of "
        + variable_x.get_name()
        + " and  "
        + variable_y.get_name()
    )

    var_unit_x = variable_x.get_unit(si_ip)
    var_unit_y = variable_y.get_unit(si_ip)

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
