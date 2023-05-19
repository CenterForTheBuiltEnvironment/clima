from math import ceil, floor

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from my_project.global_scheme import mapping_dictionary
import dash_bootstrap_components as dbc
from .global_scheme import month_lst, template, tight_margins


from .utils import code_timer, determine_month_and_hour_filter


def violin(df, var, global_local, si_ip):
    """Return day night violin based on the 'var' col"""
    mask_day = (df["hour"] >= 8) & (df["hour"] < 20)
    mask_night = (df["hour"] < 8) | (df["hour"] >= 20)
    var_unit = mapping_dictionary[var][si_ip]["unit"]
    var_range = mapping_dictionary[var][si_ip]["range"]
    var_name = mapping_dictionary[var]["name"]

    data_day = df.loc[mask_day, var]
    data_night = df.loc[mask_night, var]

    if global_local != "global":
        data_max = 5 * ceil(df[var].max() / 5)
        data_min = 5 * floor(df[var].min() / 5)
        var_range = [data_min, data_max]

    fig = go.Figure()
    fig.add_trace(
        go.Violin(
            x=df["fake_year"],
            y=data_day,
            line_color="#ffaa00",
            name="Day",
            side="negative",
            hoverinfo="y",
            hoveron="violins",
        )
    )

    fig.add_trace(
        go.Violin(
            x=df["fake_year"],
            y=data_night,
            line_color="#00264d",
            name="Night",
            side="positive",
            hoverinfo="y",
            hoveron="violins",
        )
    )

    fig.update_traces(
        meanline_visible=True,
        orientation="v",
        width=0.8,
        points=False,
    )
    title = var_name + " (" + var_unit + ")"
    fig.update_layout(
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        violingap=0,
        violingroupgap=0,
        violinmode="overlay",
        margin=tight_margins,
        legend=dict(orientation="h", yanchor="bottom", y=0.9, xanchor="right", x=1),
        template=template,
        title=title,
        title_x=0.5,
        dragmode=False,
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.update_yaxes(
        showline=True, linewidth=1, linecolor="black", mirror=True, range=var_range
    )

    return fig


@code_timer
def yearly_profile(df, var, global_local, si_ip):
    """Return yearly profile figure based on the 'var' col."""
    var_unit = mapping_dictionary[var][si_ip]["unit"]
    var_range = mapping_dictionary[var][si_ip]["range"]
    var_name = mapping_dictionary[var]["name"]
    var_color = mapping_dictionary[var]["color"]

    if global_local == "global":
        # Set Global values for Max and minimum
        range_y = var_range
    else:
        # Set maximum and minimum according to data
        data_max = 5 * ceil(df[var].max() / 5)
        data_min = 5 * floor(df[var].min() / 5)
        range_y = [data_min, data_max]

    var_single_color = var_color[len(var_color) // 2]
    custom_ylim = range_y
    # Get min, max, and mean of each day
    dbt_day = df.groupby(np.arange(len(df.index)) // 24)[var].agg(
        ["min", "max", "mean"]
    )

    trace1 = go.Bar(
        x=df["UTC_time"].dt.date.unique(),
        y=dbt_day["max"] - dbt_day["min"],
        base=dbt_day["min"],
        marker_color=var_single_color,
        marker_opacity=0.3,
        name=var_name + " Range",
        customdata=np.stack(
            (dbt_day["mean"], df.iloc[::24, :]["month_names"], df.iloc[::24, :]["day"]),
            axis=-1,
        ),
        hovertemplate=(
            "Max: %{y:.2f} "
            + var_unit
            + "<br>Min: %{base:.2f} "
            + var_unit
            + "<br><b>Ave : %{customdata[0]:.2f} "
            + var_unit
            + "</b><br>Month: %{customdata[1]}<br>Day: %{customdata[2]}<br>"
        ),
    )

    trace2 = go.Scatter(
        x=df["UTC_time"].dt.date.unique(),
        y=dbt_day["mean"],
        name="Average " + var_name,
        mode="lines",
        marker_color=var_single_color,
        marker_opacity=1,
        customdata=np.stack(
            (dbt_day["mean"], df.iloc[::24, :]["month_names"], df.iloc[::24, :]["day"]),
            axis=-1,
        ),
        hovertemplate=(
            "<b>Ave : %{customdata[0]:.2f} "
            + var_unit
            + "</b><br>Month: %{customdata[1]}<br>Day: %{customdata[2]}<br>"
        ),
    )

    if var == "DBT":
        # plot ashrae adaptive comfort limits (80%)
        lo80 = df.groupby("DOY")["adaptive_cmf_80_low"].mean().values
        hi80 = df.groupby("DOY")["adaptive_cmf_80_up"].mean().values
        rmt = df.groupby("DOY")["adaptive_cmf_rmt"].mean().values
        # set color https://github.com/CenterForTheBuiltEnvironment/clima/issues/113 implementation
        var_bar_colors = np.where((rmt > 40) | (rmt < 10), "lightgray", "darkgray")

        trace3 = go.Bar(
            x=df["UTC_time"].dt.date.unique(),
            y=hi80 - lo80,
            base=lo80,
            name="ASHRAE adaptive comfort (80%)",
            marker_color=var_bar_colors,
            marker_opacity=0.5,
            hovertemplate=(
                "Max: %{y:.2f} " + var_unit + "Min: %{base:.2f} " + var_unit
            ),
        )

        # plot ashrae adaptive comfort limits (90%)
        lo90 = df.groupby("DOY")["adaptive_cmf_90_low"].mean().values
        hi90 = df.groupby("DOY")["adaptive_cmf_90_up"].mean().values

        trace4 = go.Bar(
            x=df["UTC_time"].dt.date.unique(),
            y=hi90 - lo90,
            base=lo90,
            name="ASHRAE adaptive comfort (90%)",
            marker_color=var_bar_colors,
            marker_opacity=0.5,
            hovertemplate=(
                "Max: %{y:.2f} " + var_unit + "Min: %{base:.2f} " + var_unit
            ),
        )
        data = [trace3, trace4, trace1, trace2]

    elif var == "RH":
        # plot relative Humidity limits (30-70%)
        lo_rh = [30] * 365
        hi_rh = [70] * 365
        lo_rh_df = pd.DataFrame({"loRH": lo_rh})
        hi_rh_df = pd.DataFrame({"hiRH": hi_rh})

        trace3 = go.Bar(
            x=df["UTC_time"].dt.date.unique(),
            y=hi_rh_df["hiRH"] - lo_rh_df["loRH"],
            base=lo_rh_df["loRH"],
            name="humidity comfort band",
            marker_opacity=0.3,
            marker_color="silver",
        )

        data = [trace3, trace1, trace2]

    else:
        data = [trace1, trace2]

    fig = go.Figure(
        data=data, layout=go.Layout(barmode="overlay", bargap=0, margin=tight_margins)
    )

    fig.update_xaxes(
        dtick="M1",
        tickformat="%b",
        ticklabelmode="period",
        title_text="Day",
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )
    fig.update_yaxes(
        range=custom_ylim,
        title_text=f"{var_name} ({var_unit})",
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template=template,
    )

    return fig


# @code_timer
def daily_profile(df, var, global_local, si_ip):
    """Return the daily profile based on the 'var' col."""
    var_name = mapping_dictionary[var]["name"]
    var_unit = mapping_dictionary[var][si_ip]["unit"]
    var_range = mapping_dictionary[var][si_ip]["range"]
    var_color = mapping_dictionary[var]["color"]
    if global_local == "global":
        # Set Global values for Max and minimum
        range_y = var_range
    else:
        # Set maximum and minimum according to data
        data_max = 5 * ceil(df[var].max() / 5)
        data_min = 5 * floor(df[var].min() / 5)
        range_y = [data_min, data_max]

    var_single_color = var_color[len(var_color) // 2]
    var_month_ave = df.groupby(["month", "hour"])[var].median().reset_index()
    fig = make_subplots(
        rows=1,
        cols=12,
        subplot_titles=month_lst,
    )

    for i in range(12):
        fig.add_trace(
            go.Scatter(
                x=df.loc[df["month"] == i + 1, "hour"],
                y=df.loc[df["month"] == i + 1, var],
                mode="markers",
                marker_color=var_single_color,
                opacity=0.5,
                marker_size=3,
                name=month_lst[i],
                showlegend=False,
                customdata=df.loc[df["month"] == i + 1, "month_names"],
                hovertemplate=(
                    "<b>"
                    + var
                    + ": %{y:.2f} "
                    + var_unit
                    + "</b><br>Month: %{customdata}<br>Hour: %{x}:00<br>"
                ),
            ),
            row=1,
            col=i + 1,
        )

        fig.add_trace(
            go.Scatter(
                x=var_month_ave.loc[var_month_ave["month"] == i + 1, "hour"],
                y=var_month_ave.loc[var_month_ave["month"] == i + 1, var],
                mode="lines",
                line_color=var_single_color,
                line_width=3,
                name=None,
                showlegend=False,
                hovertemplate=(
                    "<b>" + var + ": %{y:.2f} " + var_unit + "</b><br>Hour: %{x}:00<br>"
                ),
            ),
            row=1,
            col=i + 1,
        )

        fig.update_xaxes(range=[0, 25], row=1, col=i + 1)
        fig.update_yaxes(range=range_y, row=1, col=i + 1)

    fig.update_xaxes(
        ticktext=["6", "12", "18"], tickvals=["6", "12", "18"], tickangle=0
    )

    fig.update_layout(
        template=template,
        dragmode=False,
        margin=dict(l=20, r=20, t=55, b=20),
        title=f"{var_name} ({var_unit})",
    )
    return fig


# @code_timer
def heatmap_with_filter(
    df,
    var,
    global_local,
    si_ip,
    time_filter,
    month,
    hour,
    invert_month,
    invert_hour,
    title,
):
    """General function that returns a heatmap."""
    var_unit = mapping_dictionary[var][si_ip]["unit"]
    var_range = mapping_dictionary[var][si_ip]["range"]
    var_color = mapping_dictionary[var]["color"]

    df = filter_df_by_month_and_hour(
        df, time_filter, month, hour, invert_month, invert_hour, var
    )

    start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
        month, hour, invert_month, invert_hour
    )

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

    if global_local == "global":
        # Set Global values for Max and minimum
        range_z = var_range
    else:
        # Set maximum and minimum according to data
        data_max = 5 * ceil(df[var].max() / 5)
        data_min = 5 * floor(df[var].min() / 5)
        range_z = [data_min, data_max]
    fig = go.Figure(
        data=go.Heatmap(
            y=df["hour"],
            x=df["UTC_time"].dt.date,
            z=df[var],
            colorscale=var_color,
            zmin=range_z[0],
            zmax=range_z[1],
            customdata=np.stack((df["month_names"], df["day"]), axis=-1),
            hovertemplate=(
                "<b>"
                + var
                + ": %{z:.2f} "
                + var_unit
                + "</b><br>Month: %{customdata[0]}<br>Day: %{customdata[1]}<br>Hour:"
                " %{y}:00<br>"
            ),
            name="",
            colorbar=dict(title=var_unit),
        )
    )

    fig.update_xaxes(dtick="M1", tickformat="%b", ticklabelmode="period")

    fig.update_yaxes(title_text="Hour")
    fig.update_xaxes(title_text="Day")

    if time_filter:
        title += (
            f" between the months of {month_lst[start_month - 1]} and "
            f"{month_lst[end_month - 1]}<br>and between the hours {start_hour}"
            f":00 and {end_hour}:00"
        )
    fig.update_layout(
        template=template,
        title=title,
        margin=tight_margins.copy().update({"t": 55}),
        yaxis_nticks=13,
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)

    return fig


def heatmap(df, var, global_local, si_ip):
    """General function that returns a heatmap."""
    var_unit = mapping_dictionary[var][si_ip]["unit"]
    var_range = mapping_dictionary[var][si_ip]["range"]
    var_color = mapping_dictionary[var]["color"]

    if global_local == "global":
        # Set Global values for Max and minimum
        range_z = var_range
    else:
        # Set maximum and minimum according to data
        data_max = 5 * ceil(df[var].max() / 5)
        data_min = 5 * floor(df[var].min() / 5)
        range_z = [data_min, data_max]
    fig = go.Figure(
        data=go.Heatmap(
            y=df["hour"],
            x=df["UTC_time"].dt.date,
            z=df[var],
            colorscale=var_color,
            zmin=range_z[0],
            zmax=range_z[1],
            customdata=np.stack((df["month_names"], df["day"]), axis=-1),
            hovertemplate=(
                "<b>"
                + var
                + ": %{z:.2f} "
                + var_unit
                + "</b><br>Month: %{customdata[0]}<br>Day: %{customdata[1]}<br>Hour:"
                " %{y}:00<br>"
            ),
            name="",
            colorbar=dict(title=var_unit),
        )
    )

    fig.update_xaxes(dtick="M1", tickformat="%b", ticklabelmode="period")

    fig.update_yaxes(title_text="Hour")
    fig.update_xaxes(title_text="Day")

    fig.update_layout(template=template, margin=tight_margins, yaxis_nticks=13)
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)

    return fig


### WIND ROSE TEMPLATE
def speed_labels(bins, units):
    """Return nice labels for a wind speed range."""
    labels = []
    for left, right in zip(bins[:-1], bins[1:]):
        if left == bins[0]:
            labels.append("calm")
        elif np.isinf(right):
            labels.append(">{} {}".format(left, units))
        else:
            labels.append("{} - {} {}".format(left, right, units))
    return labels


def wind_rose(df, title, month, hour, labels, si_ip):
    """Return the wind rose figure.

    Based on:  https://gist.github.com/phobson/41b41bdd157a2bcf6e14
    """
    start_month = month[0]
    end_month = month[1]
    start_hour = hour[0]
    end_hour = hour[1]
    if start_month <= end_month:
        df = df.loc[(df["month"] >= start_month) & (df["month"] <= end_month)]
    else:
        df = df.loc[(df["month"] <= end_month) | (df["month"] >= start_month)]
    if start_hour <= end_hour:
        df = df.loc[(df["hour"] >= start_hour) & (df["hour"] <= end_hour)]
    else:
        df = df.loc[(df["hour"] <= end_hour) | (df["hour"] >= start_hour)]

    spd_colors = mapping_dictionary["wind_speed"]["color"]
    spd_unit = mapping_dictionary["wind_speed"][si_ip]["unit"]
    spd_bins = [-1, 0.5, 1.5, 3.3, 5.5, 7.9, 10.7, 13.8, 17.1, 20.7, np.inf]
    if si_ip == "ip":
        spd_bins = convert_bins(spd_bins)

    spd_labels = speed_labels(spd_bins, spd_unit)
    dir_bins = np.arange(-22.5 / 2, 360 + 22.5, 22.5)
    dir_labels = (dir_bins[:-1] + dir_bins[1:]) / 2
    total_count = df.shape[0]
    calm_count = df.query("wind_speed == 0").shape[0]
    rose = (
        df.assign(
            WindSpd_bins=lambda df: pd.cut(
                df["wind_speed"], bins=spd_bins, labels=spd_labels, right=True
            )
        )
        .assign(
            WindDir_bins=lambda df: pd.cut(
                df["wind_dir"], bins=dir_bins, labels=dir_labels, right=False
            )
        )
        .replace({"WindDir_bins": {360: 0}})
        .groupby(by=["WindSpd_bins", "WindDir_bins"])
        .size()
        .unstack(level="WindSpd_bins")
        .fillna(0)
        .assign(calm=lambda df: calm_count / df.shape[0])
        .sort_index(axis=1)
        .applymap(lambda x: x / total_count * 100)
    )
    fig = go.Figure()
    for i, col in enumerate(rose.columns):
        fig.add_trace(
            go.Barpolar(
                r=rose[col],
                theta=rose.index.categories,
                name=col,
                marker_color=spd_colors[i],
                hovertemplate="frequency: %{r:.2f}%"
                + "<br>"
                + "direction: %{theta:.2f}"
                + "\u00B0 deg"
                + "<br>",
            )
        )

    fig.update_traces(
        text=[
            "North",
            "N-N-E",
            "N-E",
            "E-N-E",
            "East",
            "E-S-E",
            "S-E",
            "S-S-E",
            "South",
            "S-S-W",
            "S-W",
            "W-S-W",
            "West",
            "W-N-W",
            "N-W",
            "N-N-W",
        ]
    )
    if title != "":
        fig.update_layout(title=title, title_x=0.5)
    fig.update_layout(
        autosize=True,
        polar_angularaxis_rotation=90,
        polar_angularaxis_direction="clockwise",
        showlegend=labels,
        dragmode=False,
        margin=tight_margins,
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)

    return fig


def convert_bins(sbins):
    i = 0
    for x in sbins:
        x = x * 196.85039370078738
        sbins[i] = round(x, 1)
        i = i + 1
    return sbins


def thermal_stress_stacked_barchart(
    df, var, time_filter, month, hour, invert_month, invert_hour, normalize, title
):
    """Return the summary bar chart."""
    categories = [
        "extreme cold stress",
        "very strong cold stress",
        "strong cold stress",
        "moderate cold stress",
        "slight cold stress",
        "no thermal stress",
        "moderate heat stress",
        "strong heat stress",
        "very strong heat stress",
        "extreme heat stress",
    ]
    colors = [
        "#2A2B72",
        "#394396",
        "#44549F",
        "#4F63A8",
        "#7AB7E2",
        "#6EB557",
        "#E0893D",
        "#D84032",
        "#A3302B",
        "#6B1F18",
    ]
    df = filter_df_by_month_and_hour(
        df, time_filter, month, hour, invert_month, invert_hour, var
    )
    start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
        month, hour, invert_month, invert_hour
    )

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
    isNormalized = True if len(normalize) != 0 else False
    if isNormalized:
        new_df = (
            df.groupby("month")[var].value_counts(normalize=True).unstack(var).fillna(0)
        )
        new_df.set_axis(categories, axis=1, inplace=True)
        new_df.reset_index(inplace=True)
    else:
        new_df = df.groupby("month")[var].value_counts().unstack(var).fillna(0)
        new_df.set_axis(categories, axis=1, inplace=True)
        new_df.reset_index(inplace=True)

    go.Figure()
    data = []
    for i in range(len(categories)):
        x_data = list(range(0, 12))
        y_data = [
            catch(lambda: new_df.iloc[mth][categories[i]]) for mth in range(0, 12)
        ]
        data.append(
            go.Bar(
                x=x_data,
                y=y_data,
                name=categories[i],
                marker_color=colors[i],
                hovertemplate=(
                    "</b><br>Month: %{x}<br>Category: "
                    + categories[i]
                    + "<br>Count: %{y}<br><extra></extra>"
                    if len(normalize) == 0
                    else "</b><br>Month: %{x}<br>Category: "
                    + categories[i]
                    + "<br>Proportion: %{y:.1f}%<br><extra></extra>"
                ),
            )
        )

    fig = go.Figure(data=data)

    if time_filter:
        title += (
            f" between the months of {month_lst[start_month - 1]} and "
            f"{month_lst[end_month - 1]} and between the hours {start_hour}"
            f":00 and {end_hour}:00"
        )

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        barmode="stack",
        dragmode=False,
        title=title,
        margin=tight_margins.copy().update({"t": 55}),
    )
    if isNormalized:
        fig.update_layout(barnorm="percent")
    fig.update_yaxes(
        title_text="Percentage (%)" if isNormalized else "Count",
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )
    fig.update_xaxes(
        dict(tickmode="array", tickvals=np.arange(0, 12, 1), ticktext=month_lst),
        title_text="Day",
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )
    return fig


def barchart(df, var, time_filter_info, data_filter_info, normalize, si_ip):
    """Return the custom summary bar chart."""
    time_filter = time_filter_info[0]
    data_filter = data_filter_info[0]
    min_val = data_filter_info[2]
    max_val = data_filter_info[3]
    if len(time_filter_info) == 3:
        start_month = time_filter_info[1][0]
        end_month = time_filter_info[1][1]
        start_hour = time_filter_info[2][0]
        end_hour = time_filter_info[2][1]

        filter_var = str(data_filter_info[1])
        filter_name = mapping_dictionary[filter_var]["name"]
        filter_unit = mapping_dictionary[filter_var][si_ip]["unit"]

    var_unit = mapping_dictionary[var][si_ip]["unit"]
    var_name = mapping_dictionary[var]["name"]
    var_color = mapping_dictionary[var]["color"]

    color_below = var_color[0]
    color_above = var_color[-1]
    color_in = var_color[len(var_color) // 2]

    new_df = df.copy()
    month_in = []
    month_below = []
    month_above = []

    min_val = str(min_val)
    max_val = str(max_val)

    if len(time_filter_info) == 1:
        filter_var = str(var)

    for i in range(1, 13):
        query = (
            f"month=={str(i)} and ({filter_var}>={min_val} and {filter_var}<={max_val})"
        )
        a = new_df.query(query)["DOY"].count()
        month_in.append(a)
        query = f"month=={str(i)} and ({filter_var}<{min_val})"
        b = new_df.query(query)["DOY"].count()
        month_below.append(b)
        query = f"month=={str(i)} and {filter_var}>{max_val}"
        c = new_df.query(query)["DOY"].count()
        month_above.append(c)

    go.Figure()
    trace1 = go.Bar(
        x=list(range(0, 13)), y=month_in, name="IN range", marker_color=color_in
    )
    trace2 = go.Bar(
        x=list(range(0, 13)),
        y=month_below,
        name="BELOW range",
        marker_color=color_below,
    )
    trace3 = go.Bar(
        x=list(range(0, 13)),
        y=month_above,
        name="ABOVE range",
        marker_color=color_above,
    )
    data = [trace2, trace1, trace3]

    fig = go.Figure(data=data)
    fig.update_layout(barmode="stack", dragmode=False)

    if normalize:
        title = (
            "Percentage of time the "
            + var_name
            + " is in the range "
            + min_val
            + " to "
            + max_val
            + " "
            + var_unit
        )
        fig.update_yaxes(title_text="Percentage (%)")
        fig.update_layout(title=title, barnorm="percent")
    else:
        title = (
            "Number of hours the "
            + var_name
            + " is in the range "
            + min_val
            + " to "
            + max_val
            + " "
            + var_unit
        )
        fig.update_yaxes(title_text="hours")
        fig.update_layout(title=title, barnorm="")
    if time_filter:
        title += (
            "<br>between the months of "
            + month_lst[start_month - 1]
            + " to "
            + month_lst[end_month - 1]
            + " and between "
            + str(start_hour)
            + ":00-"
            + str(end_hour)
            + ":00 hours"
        )
    if data_filter:
        title += (
            ",<br>when the "
            + filter_name
            + " is between "
            + str(min_val)
            + " and "
            + str(min_val)
            + filter_unit
        )
    return fig


def filter_df_by_month_and_hour(
    df, time_filter, month, hour, invert_month, invert_hour, var
):
    start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
        month, hour, invert_month, invert_hour
    )

    if time_filter:
        if start_month <= end_month:
            mask = (df["month"] < start_month) | (df["month"] > end_month)
            df.loc[mask, var] = None
        else:
            mask = (df["month"] >= end_month) & (df["month"] <= start_month)
            df.loc[mask, var] = None

        if start_hour <= end_hour:
            mask = (df["hour"] < start_hour) | (df["hour"] > end_hour)
            df.loc[mask, var] = None
        else:
            mask = (df["hour"] >= end_hour) & (df["hour"] <= start_hour)
            df.loc[mask, var] = None

    return df


def catch(func, handle=lambda e: e, *args, **kwargs):
    # Handle category not in dictionary
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return 0
