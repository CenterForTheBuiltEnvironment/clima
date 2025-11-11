import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import UnitSystem
from pages.lib.utils import (
    get_max_min_value,
    has_filtered_data,
    get_variable_info,
    get_variable_range,
    get_original_column_values,
    calculate_daily_statistics,
    unpack_variable_info,
)
import dash_bootstrap_components as dbc
from .global_scheme import month_lst, template, tight_margins, WIND_ROSE_BINS
from pages.lib.global_variables import Variables, VariableInfo
from .utils import code_timer, determine_month_and_hour_filter, separate_filtered_data


def violin(df, var, global_local, si_ip):
    """Return day night violin based on the 'var' col"""
    mask_day = (df[Variables.HOUR.col_name] >= 8) & (df[Variables.HOUR.col_name] < 20)
    mask_night = (df[Variables.HOUR.col_name] < 8) | (df[Variables.HOUR.col_name] >= 20)
    var_info = get_variable_info(var, si_ip)
    var_unit, var_range, var_name = unpack_variable_info(
        var_info, ["var_unit", "var_range", "var_name"]
    )

    data_day = df.loc[mask_day, var]
    data_night = df.loc[mask_night, var]

    if global_local != "global":
        data_max, data_min = get_max_min_value(df[var])
        var_range = [data_min, data_max]

    fig = go.Figure()
    fig.add_trace(
        go.Violin(
            x=df[Variables.FAKE_YEAR.col_name],
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
            x=df[Variables.FAKE_YEAR.col_name],
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
        height=400,
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.update_yaxes(
        showline=True, linewidth=1, linecolor="black", mirror=True, range=var_range
    )

    return fig


@code_timer
def yearly_profile(df, var, global_local, si_ip):
    """Return yearly profile figure based on the 'var' col."""
    var_info = get_variable_info(var, si_ip)
    var_unit, var_range, var_name, var_color = unpack_variable_info(var_info)

    # Separate filtered and unfiltered data using utility function
    filter_info = separate_filtered_data(df, var)
    has_filter_marker = filter_info["has_filter_marker"]
    filtered_mask = filter_info["filtered_mask"]
    original_var_col = filter_info["original_var_col"]
    use_original_for_filtered = filter_info["use_original_for_filtered"]

    # Calculate y-axis range - use original values if available to keep range consistent
    if global_local == "global":
        # Set Global values for Max and minimum
        range_y = var_range
    else:
        # Set maximum and minimum according to data
        # If filtering is active, use original values to maintain consistent y-axis range
        if (
            has_filter_marker
            and use_original_for_filtered
            and filtered_mask is not None
            and filtered_mask.any()
        ):
            # Combine unfiltered values and original filtered values for range calculation
            values_for_range = pd.concat(
                [
                    df[~filtered_mask][var],
                    df[filtered_mask][original_var_col],
                ]
            ).dropna()
            # Use combined values if available, otherwise fallback to current values
            range_y = get_variable_range(
                var,
                df,
                "local",
                si_ip,
                use_original_for_range=len(values_for_range) > 0,
                original_values=values_for_range if len(values_for_range) > 0 else None,
            )
        else:
            range_y = get_variable_range(var, df, "local", si_ip)

    var_single_color = var_color[len(var_color) // 2]
    custom_ylim = range_y

    # Get all unique dates from the full dataframe for consistent x-axis alignment
    all_dates = sorted(df[Variables.UTC_TIME.col_name].dt.date.unique())

    # Get min, max, and mean of each day for unfiltered and filtered data
    if has_filter_marker and filtered_mask is not None:
        # Use already separated data from filter_info
        df_unfiltered = filter_info["df_unfiltered"]
        df_filtered = filter_info["df_filtered"]

        # Calculate statistics for unfiltered data
        dbt_day_unfiltered = calculate_daily_statistics(df_unfiltered, var)

        # Calculate statistics for filtered data (using original values)
        if has_filtered_data(df_filtered) and use_original_for_filtered:
            dbt_day_filtered = calculate_daily_statistics(df_filtered, original_var_col)
        else:
            dbt_day_filtered = None
    else:
        # No filtering, use full dataframe
        df_unfiltered = df
        df_filtered = None
        dbt_day_unfiltered = calculate_daily_statistics(df, var)
        dbt_day_filtered = None

    traces = []

    # Add filtered data traces (gray) if any filtered data exists
    if (
        has_filter_marker
        and filtered_mask is not None
        and filtered_mask.any()
        and dbt_day_filtered is not None
        and len(dbt_day_filtered) > 0
    ):
        # Reindex to all_dates to ensure consistent x-axis alignment
        dbt_day_filtered_reindexed = dbt_day_filtered.reindex(all_dates)

        # Create a mapping from date to month/day names for customdata
        df_filtered_date_map = df_filtered.copy()
        df_filtered_date_map["_date"] = df_filtered_date_map[
            Variables.UTC_TIME.col_name
        ].dt.date
        # Get first occurrence of each date for month/day names
        date_to_metadata_filtered = df_filtered_date_map.groupby("_date").first()

        # Build customdata arrays aligned with all_dates
        filtered_month_names = [
            date_to_metadata_filtered.loc[date, Variables.MONTH_NAMES.col_name]
            if date in date_to_metadata_filtered.index
            else ""
            for date in all_dates
        ]
        filtered_day_names = [
            date_to_metadata_filtered.loc[date, Variables.DAY.col_name]
            if date in date_to_metadata_filtered.index
            else ""
            for date in all_dates
        ]

        trace1_filtered = go.Bar(
            x=all_dates,
            y=dbt_day_filtered_reindexed["max"] - dbt_day_filtered_reindexed["min"],
            base=dbt_day_filtered_reindexed["min"],
            marker_color="gray",
            marker_opacity=0.3,
            name=var_name + " Range (Filtered)",
            customdata=np.stack(
                (
                    dbt_day_filtered_reindexed["mean"].values,
                    filtered_month_names,
                    filtered_day_names,
                ),
                axis=-1,
            ),
            hovertemplate=(
                "<b>Filtered Data</b><br>Max: %{y:.2f} "
                + var_unit
                + "<br>Min: %{base:.2f} "
                + var_unit
                + "<br><b>Ave : %{customdata[0]:.2f} "
                + var_unit
                + "</b><br>Month: %{customdata[1]}<br>Day: %{customdata[2]}<br>"
            ),
        )
        traces.append(trace1_filtered)

        trace2_filtered = go.Scatter(
            x=all_dates,
            y=dbt_day_filtered_reindexed["mean"],
            name="Average " + var_name + " (Filtered)",
            mode="lines",
            marker_color="lightgray",
            marker_opacity=1,
            line=dict(color="lightgray", width=2),
            customdata=np.stack(
                (
                    dbt_day_filtered_reindexed["mean"].values,
                    filtered_month_names,
                    filtered_day_names,
                ),
                axis=-1,
            ),
            hovertemplate=(
                "<b>Filtered Data</b><br><b>Ave : %{customdata[0]:.2f} "
                + var_unit
                + "</b><br>Month: %{customdata[1]}<br>Day: %{customdata[2]}<br>"
            ),
        )
        traces.append(trace2_filtered)

    # Add unfiltered data traces (normal colors)
    if len(dbt_day_unfiltered) > 0:
        # Reindex to all_dates to ensure consistent x-axis alignment
        dbt_day_unfiltered_reindexed = dbt_day_unfiltered.reindex(all_dates)

        # Create a mapping from date to month/day names for customdata
        df_unfiltered_date_map = df_unfiltered.copy()
        df_unfiltered_date_map["_date"] = df_unfiltered_date_map[
            Variables.UTC_TIME.col_name
        ].dt.date
        # Get first occurrence of each date for month/day names
        date_to_metadata = df_unfiltered_date_map.groupby("_date").first()

        # Build customdata arrays aligned with all_dates
        unfiltered_month_names = [
            date_to_metadata.loc[date, Variables.MONTH_NAMES.col_name]
            if date in date_to_metadata.index
            else ""
            for date in all_dates
        ]
        unfiltered_day_names = [
            date_to_metadata.loc[date, Variables.DAY.col_name]
            if date in date_to_metadata.index
            else ""
            for date in all_dates
        ]

        trace1 = go.Bar(
            x=all_dates,
            y=dbt_day_unfiltered_reindexed["max"] - dbt_day_unfiltered_reindexed["min"],
            base=dbt_day_unfiltered_reindexed["min"],
            marker_color=var_single_color,
            marker_opacity=0.3,
            name=var_name + " Range",
            customdata=np.stack(
                (
                    dbt_day_unfiltered_reindexed["mean"].values,
                    unfiltered_month_names,
                    unfiltered_day_names,
                ),
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
        traces.append(trace1)

        trace2 = go.Scatter(
            x=all_dates,
            y=dbt_day_unfiltered_reindexed["mean"],
            name="Average " + var_name,
            mode="lines",
            marker_color=var_single_color,
            marker_opacity=1,
            customdata=np.stack(
                (
                    dbt_day_unfiltered_reindexed["mean"].values,
                    unfiltered_month_names,
                    unfiltered_day_names,
                ),
                axis=-1,
            ),
            hovertemplate=(
                "<b>Ave : %{customdata[0]:.2f} "
                + var_unit
                + "</b><br>Month: %{customdata[1]}<br>Day: %{customdata[2]}<br>"
            ),
        )
        traces.append(trace2)

    if var == Variables.DBT.col_name:
        # plot ashrae adaptive comfort limits (80%)
        # Group by DOY and get mean values
        doy_grouped = df.groupby(Variables.DOY.col_name)
        lo80_by_doy = doy_grouped[Variables.ADAPTIVE_CMF_80_LOW.col_name].mean()
        hi80_by_doy = doy_grouped[Variables.ADAPTIVE_CMF_80_UP.col_name].mean()
        rmt_by_doy = doy_grouped[Variables.ADAPTIVE_CMF_RMT.col_name].mean()

        # Map DOY values to dates
        df_with_date_doy = df.copy()
        df_with_date_doy["_date"] = df_with_date_doy[
            Variables.UTC_TIME.col_name
        ].dt.date
        date_to_doy = df_with_date_doy.groupby("_date")[Variables.DOY.col_name].first()

        # Align ASHRAE values to all_dates
        lo80_aligned = [
            lo80_by_doy.get(
                date_to_doy.get(date, 1),
                lo80_by_doy.iloc[0] if len(lo80_by_doy) > 0 else 0,
            )
            for date in all_dates
        ]
        hi80_aligned = [
            hi80_by_doy.get(
                date_to_doy.get(date, 1),
                hi80_by_doy.iloc[0] if len(hi80_by_doy) > 0 else 0,
            )
            for date in all_dates
        ]
        rmt_aligned = [
            rmt_by_doy.get(
                date_to_doy.get(date, 1),
                rmt_by_doy.iloc[0] if len(rmt_by_doy) > 0 else 0,
            )
            for date in all_dates
        ]

        # set color https://github.com/CenterForTheBuiltEnvironment/clima/issues/113 implementation
        var_bar_colors = np.where(
            (np.array(rmt_aligned) > 40) | (np.array(rmt_aligned) < 10),
            "lightgray",
            "darkgray",
        )

        trace3 = go.Bar(
            x=all_dates,
            y=np.array(hi80_aligned) - np.array(lo80_aligned),
            base=lo80_aligned,
            name="ASHRAE adaptive comfort (80%)",
            marker_color=var_bar_colors,
            marker_opacity=0.5,
            hovertemplate=(
                "Max: %{y:.2f} " + var_unit + "Min: %{base:.2f} " + var_unit
            ),
        )

        # plot ashrae adaptive comfort limits (90%)
        lo90_by_doy = doy_grouped[Variables.ADAPTIVE_CMF_90_LOW.col_name].mean()
        hi90_by_doy = doy_grouped[Variables.ADAPTIVE_CMF_90_UP.col_name].mean()

        # Align ASHRAE values to all_dates
        lo90_aligned = [
            lo90_by_doy.get(
                date_to_doy.get(date, 1),
                lo90_by_doy.iloc[0] if len(lo90_by_doy) > 0 else 0,
            )
            for date in all_dates
        ]
        hi90_aligned = [
            hi90_by_doy.get(
                date_to_doy.get(date, 1),
                hi90_by_doy.iloc[0] if len(hi90_by_doy) > 0 else 0,
            )
            for date in all_dates
        ]

        trace4 = go.Bar(
            x=all_dates,
            y=np.array(hi90_aligned) - np.array(lo90_aligned),
            base=lo90_aligned,
            name="ASHRAE adaptive comfort (90%)",
            marker_color=var_bar_colors,
            marker_opacity=0.5,
            hovertemplate=(
                "Max: %{y:.2f} " + var_unit + "Min: %{base:.2f} " + var_unit
            ),
        )
        # Insert ASHRAE traces before the main traces
        traces = [trace3, trace4] + traces

    elif var == Variables.RH.col_name:
        # plot relative Humidity limits (30-70%)
        # Align to all_dates length
        lo_rh = [30] * len(all_dates)
        hi_rh = [70] * len(all_dates)

        trace3 = go.Bar(
            x=all_dates,
            y=np.array(hi_rh) - np.array(lo_rh),
            base=lo_rh,
            name="humidity comfort band",
            marker_opacity=0.3,
            marker_color="silver",
        )

        # Insert humidity comfort band before the main traces
        traces = [trace3] + traces

    # traces already contains the main traces (trace1, trace2, and filtered versions if any)

    fig = go.Figure(
        data=traces, layout=go.Layout(barmode="overlay", bargap=0, margin=tight_margins)
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
    var_info = get_variable_info(var, si_ip)
    var_name, var_unit, var_color = unpack_variable_info(
        var_info, ["var_name", "var_unit", "var_color"]
    )
    range_y = get_variable_range(var, df, global_local, si_ip)

    var_single_color = var_color[len(var_color) // 2]

    # Separate filtered and unfiltered data using utility function
    filter_info = separate_filtered_data(df, var)
    df_unfiltered = filter_info["df_unfiltered"]
    df_filtered = filter_info["df_filtered"]
    original_var_col = filter_info["original_var_col"]
    use_original_for_filtered = filter_info["use_original_for_filtered"]

    # Calculate monthly averages for unfiltered data
    var_month_ave = (
        df_unfiltered.groupby([Variables.MONTH.col_name, Variables.HOUR.col_name])[var]
        .median()
        .reset_index()
    )

    # Calculate monthly averages for filtered data (using original values)
    var_month_ave_filtered = None
    if has_filtered_data(df_filtered) and use_original_for_filtered:
        var_month_ave_filtered = (
            df_filtered.groupby([Variables.MONTH.col_name, Variables.HOUR.col_name])[
                original_var_col
            ]
            .median()
            .reset_index()
        )

    fig = make_subplots(
        rows=1,
        cols=12,
        subplot_titles=month_lst,
        shared_yaxes=True,
    )

    for i in range(12):
        month_data_unfiltered = df_unfiltered.loc[
            df_unfiltered[Variables.MONTH.col_name] == i + 1
        ]
        month_data_filtered = None
        if has_filtered_data(df_filtered):
            month_data_filtered = df_filtered.loc[
                df_filtered[Variables.MONTH.col_name] == i + 1
            ]

        # Add filtered data scatter (gray) if any
        if month_data_filtered is not None and len(month_data_filtered) > 0:
            filtered_var_values = (
                month_data_filtered[original_var_col]
                if use_original_for_filtered
                else month_data_filtered[var]
            )
            fig.add_trace(
                go.Scatter(
                    x=month_data_filtered[Variables.HOUR.col_name],
                    y=filtered_var_values,
                    mode="markers",
                    marker_color="gray",
                    opacity=0.3,
                    marker_size=2,
                    name=month_lst[i] + " (Filtered)",
                    showlegend=False,
                    customdata=month_data_filtered[Variables.MONTH_NAMES.col_name],
                    hovertemplate=(
                        "<b>Filtered Data</b><br>"
                        + var
                        + ": %{y:.2f} "
                        + var_unit
                        + "</b><br>Month: %{customdata}<br>Hour: %{x}:00<br>"
                    ),
                ),
                row=1,
                col=i + 1,
            )

            # Add filtered data median line (lightgray) if available
            if var_month_ave_filtered is not None and len(var_month_ave_filtered) > 0:
                month_ave_filtered = var_month_ave_filtered.loc[
                    var_month_ave_filtered[Variables.MONTH.col_name] == i + 1
                ]
                if len(month_ave_filtered) > 0:
                    fig.add_trace(
                        go.Scatter(
                            x=month_ave_filtered[Variables.HOUR.col_name],
                            y=month_ave_filtered[original_var_col],
                            mode="lines",
                            line_color="lightgray",
                            line_width=2,
                            name=None,
                            showlegend=False,
                            hovertemplate=(
                                "<b>Filtered Data</b><br>"
                                + var
                                + ": %{y:.2f} "
                                + var_unit
                                + "</b><br>Hour: %{x}:00<br>"
                            ),
                        ),
                        row=1,
                        col=i + 1,
                    )

        # Add unfiltered data scatter (normal color)
        if len(month_data_unfiltered) > 0:
            fig.add_trace(
                go.Scatter(
                    x=month_data_unfiltered[Variables.HOUR.col_name],
                    y=month_data_unfiltered[var],
                    mode="markers",
                    marker_color=var_single_color,
                    opacity=0.5,
                    marker_size=3,
                    name=month_lst[i],
                    showlegend=False,
                    customdata=month_data_unfiltered[Variables.MONTH_NAMES.col_name],
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

        # Add unfiltered data median line (normal color)
        month_ave_unfiltered = var_month_ave.loc[
            var_month_ave[Variables.MONTH.col_name] == i + 1
        ]
        if len(month_ave_unfiltered) > 0:
            fig.add_trace(
                go.Scatter(
                    x=month_ave_unfiltered[Variables.HOUR.col_name],
                    y=month_ave_unfiltered[var],
                    mode="lines",
                    line_color=var_single_color,
                    line_width=3,
                    name=None,
                    showlegend=False,
                    hovertemplate=(
                        "<b>"
                        + var
                        + ": %{y:.2f} "
                        + var_unit
                        + "</b><br>Hour: %{x}:00<br>"
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
    z_range=None,
):
    """General function that returns a heatmap."""
    var_info = get_variable_info(var, si_ip)
    var_unit, var_range, var_color = unpack_variable_info(
        var_info, ["var_unit", "var_range", "var_color"]
    )

    has_global_filter_marker = "_is_filtered" in df.columns
    global_filter_mask = None
    if has_global_filter_marker:
        global_filter_mask = df["_is_filtered"].copy()

    df = filter_df_by_month_and_hour(
        df, time_filter, month, hour, invert_month, invert_hour, var
    )

    if has_global_filter_marker and global_filter_mask is not None:
        df["_is_filtered"] = global_filter_mask

    start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
        month, hour, invert_month, invert_hour
    )

    if df.dropna(subset=[Variables.MONTH.col_name]).shape[0] == 0:
        return (
            dbc.Alert(
                "No data is available in this location under these conditions. Please "
                "either change the month and hour filters, or select a wider range for "
                "the filter variable",
                color="danger",
                style={"text-align": "center", "marginTop": "2rem"},
            ),
        )

    # For category variables (e.g., UTCI categories), always use global range
    # to ensure consistent color mapping regardless of data range
    if "_categories" in var:
        range_z = var_range
    else:
        range_z = get_variable_range(var, df, global_local, si_ip)
    fig = go.Figure()

    has_filter_marker = "_is_filtered" in df.columns

    if has_filter_marker and df["_is_filtered"].any():
        filtered_mask = df["_is_filtered"]
        if filtered_mask.any():
            filtered_values = get_original_column_values(df, var)

            filtered_values[~filtered_mask] = None

            fig.add_trace(
                go.Heatmap(
                    y=df[Variables.HOUR.col_name] - 0.5,
                    x=df[Variables.UTC_TIME.col_name].dt.date,
                    z=filtered_values,
                    colorscale=[[0, "lightgray"], [1, "gray"]],
                    zmin=range_z[0],
                    zmax=range_z[1],
                    showscale=False,
                    customdata=np.stack(
                        (
                            df[Variables.MONTH_NAMES.col_name],
                            df[Variables.DAY.col_name],
                        ),
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

        base_values = df[var].copy()
        base_values[filtered_mask] = None

        fig.add_trace(
            go.Heatmap(
                y=df[Variables.HOUR.col_name] - 0.5,
                x=df[Variables.UTC_TIME.col_name].dt.date,
                z=base_values,
                colorscale=var_color,
                zmin=range_z[0],
                zmax=range_z[1],
                customdata=np.stack(
                    (df[Variables.MONTH_NAMES.col_name], df[Variables.DAY.col_name]),
                    axis=-1,
                ),
                hovertemplate=(
                    "<b>"
                    + var
                    + ": %{z:.2f} "
                    + var_unit
                    + "</b><br>Month: %{customdata[0]}<br>Day: %{customdata[1]}<br>Hour:"
                    " %{y}:00<br>"
                ),
                name="",
                colorbar=(
                    dict(title="") if "_categories" in var else dict(title=var_unit)
                ),
            )
        )
    else:
        fig.add_trace(
            go.Heatmap(
                y=df[Variables.HOUR.col_name]
                - 0.5,  # Offset by 0.5 to center the hour labels
                x=df[Variables.UTC_TIME.col_name].dt.date,
                z=df[var],
                colorscale=var_color,
                zmin=range_z[0],
                zmax=range_z[1],
                customdata=np.stack(
                    (df[Variables.MONTH_NAMES.col_name], df[Variables.DAY.col_name]),
                    axis=-1,
                ),
                hovertemplate=(
                    "<b>"
                    + var
                    + ": %{z:.2f} "
                    + var_unit
                    + "</b><br>Month: %{customdata[0]}<br>Day: %{customdata[1]}<br>Hour:"
                    " %{y}:00<br>"
                ),
                name="",
                colorbar=(
                    dict(title="") if "_categories" in var else dict(title=var_unit)
                ),
            )
        )

    if var == Variables.WIND_SPEED.col_name:
        spd_bins = list(WIND_ROSE_BINS)
        if si_ip == UnitSystem.IP:
            spd_bins = convert_bins(spd_bins)
        fig.update_traces(zmin=0, zmax=spd_bins[-2])

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
    var_info = get_variable_info(var, si_ip)
    var_unit, var_range, var_color = unpack_variable_info(
        var_info, ["var_unit", "var_range", "var_color"]
    )
    range_z = get_variable_range(var, df, global_local, si_ip)
    fig = go.Figure()

    has_filter_marker = "_is_filtered" in df.columns

    if has_filter_marker and df["_is_filtered"].any():
        filtered_mask = df["_is_filtered"]
        if filtered_mask.any():
            filtered_values = get_original_column_values(df, var)

            filtered_values[~filtered_mask] = None

            fig.add_trace(
                go.Heatmap(
                    y=df[Variables.HOUR.col_name],
                    x=df[Variables.UTC_TIME.col_name].dt.date,
                    z=filtered_values,
                    colorscale=[[0, "lightgray"], [1, "gray"]],
                    zmin=range_z[0],
                    zmax=range_z[1],
                    showscale=False,
                    customdata=np.stack(
                        (
                            df[Variables.MONTH_NAMES.col_name],
                            df[Variables.DAY.col_name],
                        ),
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

        base_values = df[var].copy()
        base_values[filtered_mask] = None

        fig.add_trace(
            go.Heatmap(
                y=df[Variables.HOUR.col_name],
                x=df[Variables.UTC_TIME.col_name].dt.date,
                z=base_values,
                colorscale=var_color,
                zmin=range_z[0],
                zmax=range_z[1],
                customdata=np.stack(
                    (df[Variables.MONTH_NAMES.col_name], df[Variables.DAY.col_name]),
                    axis=-1,
                ),
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
    else:
        fig.add_trace(
            go.Heatmap(
                y=df[Variables.HOUR.col_name],
                x=df[Variables.UTC_TIME.col_name].dt.date,
                z=df[var],
                colorscale=var_color,
                zmin=range_z[0],
                zmax=range_z[1],
                customdata=np.stack(
                    (df[Variables.MONTH_NAMES.col_name], df[Variables.DAY.col_name]),
                    axis=-1,
                ),
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

    if var == Variables.WIND_SPEED.col_name:
        spd_bins = list(WIND_ROSE_BINS)
        if si_ip == UnitSystem.IP:
            spd_bins = convert_bins(spd_bins)
        fig.update_traces(zmin=0, zmax=spd_bins[-2])

    fig.update_xaxes(dtick="M1", tickformat="%b", ticklabelmode="period")

    fig.update_yaxes(title_text="Hour")
    fig.update_xaxes(title_text="Day")

    fig.update_layout(template=template, margin=tight_margins, yaxis_nticks=13)
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)

    return fig


def speed_labels(bins, units):
    """Return nice labels for a wind speed range."""
    labels = []
    for left, right in zip(bins[:-1], bins[1:]):
        if left == bins[0]:
            labels.append("calm")
        elif np.isinf(right):
            labels.append(f">{left} {units}")
        else:
            labels.append(f"{left} - {right} {units}")
    return labels


def wind_rose(df, title, month, hour, labels, si_ip, skip_time_filter=False):
    """Return the wind rose figure.

    Based on:  https://gist.github.com/phobson/41b41bdd157a2bcf6e14
    """
    if not skip_time_filter:
        start_month = month[0]
        end_month = month[1]
        start_hour = hour[0]
        end_hour = hour[1]
        if start_month <= end_month:
            df = df.loc[
                (df[Variables.MONTH.col_name] >= start_month)
                & (df[Variables.MONTH.col_name] <= end_month)
            ]
        else:
            df = df.loc[
                (df[Variables.MONTH.col_name] <= end_month)
                | (df[Variables.MONTH.col_name] >= start_month)
            ]
        if start_hour <= end_hour:
            df = df.loc[
                (df[Variables.HOUR.col_name] > start_hour)
                & (df[Variables.HOUR.col_name] <= end_hour)
            ]
        else:
            df = df.loc[
                (df[Variables.HOUR.col_name] <= end_hour)
                | (df[Variables.HOUR.col_name] >= start_hour)
            ]

    wind_speed_variable = VariableInfo.from_col_name(Variables.WIND_SPEED.col_name)

    spd_colors = wind_speed_variable.get_color()
    spd_unit = wind_speed_variable.get_unit(si_ip)
    spd_bins = list(
        WIND_ROSE_BINS
    )  # Create a copy to avoid modifying the global constant
    if si_ip == UnitSystem.IP:
        spd_bins = convert_bins(spd_bins)

    spd_labels = speed_labels(spd_bins, spd_unit)
    dir_bins = np.arange(-22.5 / 2, 360 + 22.5, 22.5)
    dir_labels = (dir_bins[:-1] + dir_bins[1:]) / 2
    total_count = df.shape[0]
    calm_count = df.query(f"{Variables.WIND_SPEED.col_name} == 0").shape[0]

    # Create a temporary DataFrame with binned data
    df_binned = df.assign(
        WindSpd_bins=lambda d: pd.cut(
            d[Variables.WIND_SPEED.col_name],
            bins=spd_bins,
            labels=spd_labels,
            right=True,
        ),
        WindDir_bins=lambda d: pd.cut(
            d[Variables.WIND_DIR.col_name],
            bins=dir_bins,
            labels=dir_labels,
            right=False,
        ),
    )

    # Rename the category in the 'WindDir_bins' column
    df_binned[Variables.WIND_DIR_BINS.col_name] = df_binned[
        Variables.WIND_DIR_BINS.col_name
    ].rename({360.0: 0.0})

    rose = (
        df_binned.groupby(
            by=[Variables.WIND_SPD_BINS.col_name, Variables.WIND_DIR_BINS.col_name],
            observed=False,
        )
        .size()
        .unstack(level=Variables.WIND_SPD_BINS.col_name)
        .fillna(0)
        .assign(calm=lambda d: calm_count / d.shape[0])
        .sort_index(axis=1)
        .map(lambda x: x / total_count * 100)
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
                + "\u00b0 deg"
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
        legend_title_text=f"Wind Speed ({spd_unit})",
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)

    return fig


def convert_bins(sbins):
    """Convert wind speed bins from m/s to fpm (feet per minute).

    Returns a new list without modifying the input list.
    """
    result = []
    for x in sbins:
        if np.isfinite(x):
            converted = round(x * 196.85039370078738, 1)
            result.append(converted)
        else:
            result.append(x)  # Preserve np.inf
    return result


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

    # Check if there's a filter marker before applying time filter
    has_filter_marker = "_is_filtered" in df.columns
    global_filter_mask = None
    if has_filter_marker:
        global_filter_mask = df["_is_filtered"].copy()

    df = filter_df_by_month_and_hour(
        df, time_filter, month, hour, invert_month, invert_hour, var
    )

    # Restore filter marker after time filtering
    if has_filter_marker and global_filter_mask is not None:
        df["_is_filtered"] = global_filter_mask

    start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
        month, hour, invert_month, invert_hour
    )

    if df.dropna(subset=[Variables.MONTH.col_name]).shape[0] == 0:
        return (
            dbc.Alert(
                "No data is available in this location under these conditions. Please "
                "either change the month and hour filters, or select a wider range for "
                "the filter variable",
                color="danger",
                style={"text-align": "center", "marginTop": "2rem"},
            ),
        )

    # Separate filtered and unfiltered data using utility function
    filter_info = separate_filtered_data(df, var)
    df_unfiltered = filter_info["df_unfiltered"]
    df_filtered = filter_info["df_filtered"]
    has_filtered_data_flag = has_filtered_data(df_filtered)

    isNormalized = True if normalize else False

    # Calculate data for unfiltered
    if isNormalized:
        new_df_unfiltered = (
            df_unfiltered.groupby(Variables.MONTH.col_name)[var]
            .value_counts(normalize=True)
            .unstack(var)
            .fillna(0)
        )
        new_df_unfiltered = new_df_unfiltered.set_axis(categories, axis=1)
        new_df_unfiltered.reset_index(inplace=True)
    else:
        new_df_unfiltered = (
            df_unfiltered.groupby(Variables.MONTH.col_name)[var]
            .value_counts()
            .unstack(var)
            .fillna(0)
        )
        new_df_unfiltered = new_df_unfiltered.set_axis(categories, axis=1)
        new_df_unfiltered.reset_index(inplace=True)

    # Calculate data for filtered (if any)
    new_df_filtered = None
    if has_filtered_data_flag:
        # Use original values for filtered data if available
        original_var_col = f"_{var}_original"
        use_original = original_var_col in df_filtered.columns

        if use_original:
            # Create a temporary column with original values for calculation
            df_filtered_temp = df_filtered.copy()
            df_filtered_temp[var] = df_filtered_temp[original_var_col]
        else:
            df_filtered_temp = df_filtered

        if isNormalized:
            new_df_filtered = (
                df_filtered_temp.groupby(Variables.MONTH.col_name)[var]
                .value_counts(normalize=True)
                .unstack(var)
                .fillna(0)
            )
            new_df_filtered = new_df_filtered.set_axis(categories, axis=1)
            new_df_filtered.reset_index(inplace=True)
        else:
            new_df_filtered = (
                df_filtered_temp.groupby(Variables.MONTH.col_name)[var]
                .value_counts()
                .unstack(var)
                .fillna(0)
            )
            new_df_filtered = new_df_filtered.set_axis(categories, axis=1)
            new_df_filtered.reset_index(inplace=True)

    go.Figure()
    data = []

    # Filtered data traces removed - no gray filtering effect for thermal stress chart

    # Add unfiltered data traces (normal colors)
    for i in range(len(categories)):
        x_data = list(range(0, 12))
        y_data = []
        for mth in range(0, 12):
            month_idx = mth + 1  # month index (1-12)
            # Check if this month exists in unfiltered data
            month_rows = new_df_unfiltered[
                new_df_unfiltered[Variables.MONTH.col_name] == month_idx
            ]
            if len(month_rows) > 0:
                try:
                    val = month_rows.iloc[0][categories[i]]
                    y_data.append(val if not pd.isna(val) else 0)
                except (KeyError, IndexError, TypeError):
                    y_data.append(0)
            else:
                y_data.append(0)
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
                    if not normalize
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
    # Get available months from unfiltered data (or combined if no filter)
    available_months = sorted(new_df_unfiltered[Variables.MONTH.col_name].unique())
    if has_filtered_data_flag and new_df_filtered is not None:
        filtered_months = sorted(new_df_filtered[Variables.MONTH.col_name].unique())
        available_months = sorted(set(available_months + filtered_months))

    fig.update_xaxes(
        dict(
            tickmode="array",
            tickvals=np.arange(0, len(available_months), 1),
            ticktext=month_lst,
        ),
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

        filter_variable = VariableInfo.from_col_name(str(data_filter_info[1]))
        filter_name = filter_variable.get_name()
        filter_unit = filter_variable.get_unit(si_ip)

    var_info = get_variable_info(var, si_ip)
    var_unit, var_name, var_color = unpack_variable_info(
        var_info, ["var_unit", "var_name", "var_color"]
    )

    color_below = var_color[0]
    color_above = var_color[-1]
    color_in = var_color[len(var_color) // 2]

    new_df = df.copy()

    # Separate filtered and unfiltered data using utility function
    filter_info = separate_filtered_data(new_df, var)
    has_filter_marker = filter_info["has_filter_marker"]
    filtered_mask = filter_info["filtered_mask"]
    df_unfiltered = filter_info["df_unfiltered"]
    df_filtered = filter_info["df_filtered"]
    original_var_col = filter_info["original_var_col"]
    use_original_for_filtered = filter_info["use_original_for_filtered"]

    month_in = []
    month_below = []
    month_above = []
    month_in_filtered = []
    month_below_filtered = []
    month_above_filtered = []

    min_val = str(min_val)
    max_val = str(max_val)

    if len(time_filter_info) == 1:
        filter_var = str(var)

    # Always process all 12 months
    available_months_set = set(new_df[Variables.MONTH.col_name].unique())

    for month_num in range(1, 13):
        if month_num in available_months_set:
            # Calculate for unfiltered data
            month_unfiltered = df_unfiltered[
                df_unfiltered[Variables.MONTH.col_name] == month_num
            ]
            if len(month_unfiltered) > 0:
                query = f"month=={str(month_num)} and ({filter_var}>={min_val} and {filter_var}<={max_val})"
                a = month_unfiltered.query(query)[Variables.DOY.col_name].count()
                month_in.append(a)
                query = f"month=={str(month_num)} and ({filter_var}<{min_val})"
                b = month_unfiltered.query(query)[Variables.DOY.col_name].count()
                month_below.append(b)
                query = f"month=={str(month_num)} and {filter_var}>{max_val}"
                c = month_unfiltered.query(query)[Variables.DOY.col_name].count()
                month_above.append(c)
            else:
                month_in.append(0)
                month_below.append(0)
                month_above.append(0)

            # Calculate for filtered data (using original values)
            if has_filtered_data(df_filtered) and use_original_for_filtered:
                month_filtered = df_filtered[
                    df_filtered[Variables.MONTH.col_name] == month_num
                ]
                if len(month_filtered) > 0:
                    filtered_var_col = original_var_col
                    query = f"month=={str(month_num)} and ({filtered_var_col}>={min_val} and {filtered_var_col}<={max_val})"
                    a = month_filtered.query(query)[Variables.DOY.col_name].count()
                    month_in_filtered.append(a)
                    query = (
                        f"month=={str(month_num)} and ({filtered_var_col}<{min_val})"
                    )
                    b = month_filtered.query(query)[Variables.DOY.col_name].count()
                    month_below_filtered.append(b)
                    query = f"month=={str(month_num)} and {filtered_var_col}>{max_val}"
                    c = month_filtered.query(query)[Variables.DOY.col_name].count()
                    month_above_filtered.append(c)
                else:
                    month_in_filtered.append(0)
                    month_below_filtered.append(0)
                    month_above_filtered.append(0)
            else:
                month_in_filtered.append(0)
                month_below_filtered.append(0)
                month_above_filtered.append(0)
        else:
            # No data for this month, append zeros
            month_in.append(0)
            month_below.append(0)
            month_above.append(0)
            month_in_filtered.append(0)
            month_below_filtered.append(0)
            month_above_filtered.append(0)

    go.Figure()

    month_names = month_lst

    data = []

    # Add filtered data traces (gray) if any filtered data exists
    if (
        has_filter_marker
        and filtered_mask is not None
        and filtered_mask.any()
        and any(month_in_filtered + month_below_filtered + month_above_filtered)
    ):
        trace1_filtered = go.Bar(
            x=month_names,
            y=month_in_filtered,
            name="IN range (Filtered)",
            marker_color="gray",
        )
        trace2_filtered = go.Bar(
            x=month_names,
            y=month_below_filtered,
            name="BELOW range (Filtered)",
            marker_color="lightgray",
        )
        trace3_filtered = go.Bar(
            x=month_names,
            y=month_above_filtered,
            name="ABOVE range (Filtered)",
            marker_color="silver",
        )
        data = [trace2_filtered, trace1_filtered, trace3_filtered]

    # Add unfiltered data traces (normal colors)
    trace1 = go.Bar(x=month_names, y=month_in, name="IN range", marker_color=color_in)
    trace2 = go.Bar(
        x=month_names,
        y=month_below,
        name="BELOW range",
        marker_color=color_below,
    )
    trace3 = go.Bar(
        x=month_names,
        y=month_above,
        name="ABOVE range",
        marker_color=color_above,
    )
    data = data + [trace2, trace1, trace3]

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


def time_filtering(
    df: pd.DataFrame, start_time: int, end_time: int, time_col: str, target_col: str
) -> pd.DataFrame:
    """Mask values in the target column based on the given time range.

    Args:
        df: Input dataframe.
        start_time: Start of the time range.
        end_time: End of the time range.
        time_col: Column name representing time (e.g., hour or month).
        target_col: Column name to apply the mask on.

    Returns:
        A modified DataFrame with masked values outside the given time range.
    """
    if start_time <= end_time:
        mask = (df[time_col] < start_time) | (df[time_col] > end_time)
    else:
        mask = (df[time_col] >= end_time) & (df[time_col] <= start_time)
    df.loc[mask, target_col] = None
    return df


def filter_df_by_month_and_hour(
    df, time_filter, month, hour, invert_month, invert_hour, var
):
    """Apply month and hour filtering to the DataFrame based on user selections.

    Args:
        df: Input DataFrame.
        time_filter: Whether to apply the time filter.
        month: Selected month range.
        hour: Selected hour range.
        invert_month: Whether to invert the month range.
        invert_hour: Whether to invert the hour range.
        var: Target variable column name.

    Returns:
        Filtered DataFrame with appropriate masking applied.
    """
    start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
        month, hour, invert_month, invert_hour
    )

    if time_filter:
        # Month filter
        time_filtering(df, start_month, end_month, Variables.MONTH.col_name, var)
        # Hour filter
        time_filtering(df, start_hour, end_hour, Variables.HOUR.col_name, var)

    return df


def catch(func, handle=lambda e: e, *args, **kwargs):
    # Handle category not in dictionary
    try:
        return func(*args, **kwargs)
    except (KeyError, IndexError, TypeError):
        return 0
