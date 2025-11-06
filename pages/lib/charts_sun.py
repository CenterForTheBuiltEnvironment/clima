from datetime import timedelta
from math import cos, radians

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from config import UnitSystem
from pages.lib.utils import get_max_min_value
from pages.lib.global_scheme import (
    template,
    degrees_unit,
    tight_margins,
    month_lst,
)
from plotly.subplots import make_subplots
from pvlib import solarposition
from pages.lib.global_variables import Variables, VariableInfo
from pages.lib.utils import separate_filtered_data


def monthly_solar(epw_df, si_ip):
    # Check if there's a filter marker
    has_filter_marker = "_is_filtered" in epw_df.columns
    filtered_mask = None
    if has_filter_marker:
        filtered_mask = epw_df["_is_filtered"]

    # Get original values if available
    original_glob_col = f"_{Variables.GLOB_HOR_RAD.col_name}_original"
    original_dif_col = f"_{Variables.DIF_HOR_RAD.col_name}_original"
    use_original_for_filtered = (
        has_filter_marker
        and original_glob_col in epw_df.columns
        and original_dif_col in epw_df.columns
    )

    # Separate filtered and unfiltered data
    if has_filter_marker and filtered_mask is not None:
        df_unfiltered = epw_df[~filtered_mask].copy()
        df_filtered = epw_df[filtered_mask].copy() if filtered_mask.any() else None
    else:
        df_unfiltered = epw_df
        df_filtered = None

    # Calculate monthly averages for unfiltered data
    g_h_rad_month_ave = (
        df_unfiltered.groupby([Variables.MONTH.col_name, Variables.HOUR.col_name])[
            Variables.GLOB_HOR_RAD.col_name
        ]
        .median()
        .reset_index()
    )
    dif_h_rad_month_ave = (
        df_unfiltered.groupby([Variables.MONTH.col_name, Variables.HOUR.col_name])[
            Variables.DIF_HOR_RAD.col_name
        ]
        .median()
        .reset_index()
    )

    # Calculate monthly averages for filtered data (using original values)
    g_h_rad_month_ave_filtered = None
    dif_h_rad_month_ave_filtered = None
    if df_filtered is not None and len(df_filtered) > 0 and use_original_for_filtered:
        g_h_rad_month_ave_filtered = (
            df_filtered.groupby([Variables.MONTH.col_name, Variables.HOUR.col_name])[
                original_glob_col
            ]
            .median()
            .reset_index()
        )
        dif_h_rad_month_ave_filtered = (
            df_filtered.groupby([Variables.MONTH.col_name, Variables.HOUR.col_name])[
                original_dif_col
            ]
            .median()
            .reset_index()
        )

    # Always show 12 months in horizontal layout
    fig = make_subplots(
        rows=1,
        cols=12,
        subplot_titles=month_lst,
        shared_yaxes=True,
    )

    # Track which legend entries have been shown (only show once)
    legend_shown = {
        "Global": False,
        "Diffuse": False,
    }

    for month_num in range(1, 13):
        col_idx = month_num

        # Add filtered data traces (gray) if any
        if (
            df_filtered is not None
            and len(df_filtered) > 0
            and g_h_rad_month_ave_filtered is not None
        ):
            month_glob_filtered = g_h_rad_month_ave_filtered.loc[
                g_h_rad_month_ave_filtered[Variables.MONTH.col_name] == month_num
            ]
            if len(month_glob_filtered) > 0:
                # Get the column name from the groupby result (it should be the original column name)
                filtered_glob_col = (
                    original_glob_col
                    if original_glob_col in month_glob_filtered.columns
                    else Variables.GLOB_HOR_RAD.col_name
                )
                fig.add_trace(
                    go.Scatter(
                        x=month_glob_filtered[Variables.HOUR.col_name],
                        y=month_glob_filtered[filtered_glob_col],
                        fill="tozeroy",
                        mode="lines",
                        line_color="gray",
                        line_width=1,
                        name="Global (Filtered)",
                        showlegend=False,
                        customdata=[month_lst[month_num - 1]] * len(month_glob_filtered)
                        if len(month_glob_filtered) > 0
                        else [],
                        hovertemplate=(
                            "<b>Filtered Data</b><br>"
                            + "Global Horizontal Solar Radiation"
                            + ": %{y:.2f} "
                            + VariableInfo.from_col_name(
                                Variables.GLOB_HOR_RAD.col_name
                            ).get_unit(si_ip)
                            + "</b><br>"
                            + "Month: %{customdata}<br>"
                            + "Hour: %{x}:00<br>"
                            + "<extra></extra>"
                        ),
                    ),
                    row=1,
                    col=col_idx,
                )

            month_dif_filtered = dif_h_rad_month_ave_filtered.loc[
                dif_h_rad_month_ave_filtered[Variables.MONTH.col_name] == month_num
            ]
            if len(month_dif_filtered) > 0:
                # Get the column name from the groupby result (it should be the original column name)
                filtered_dif_col = (
                    original_dif_col
                    if original_dif_col in month_dif_filtered.columns
                    else Variables.DIF_HOR_RAD.col_name
                )
                fig.add_trace(
                    go.Scatter(
                        x=month_dif_filtered[Variables.HOUR.col_name],
                        y=month_dif_filtered[filtered_dif_col],
                        fill="tozeroy",
                        mode="lines",
                        line_color="lightgray",
                        line_width=1,
                        name="Diffuse (Filtered)",
                        showlegend=False,
                        customdata=[month_lst[month_num - 1]] * len(month_dif_filtered)
                        if len(month_dif_filtered) > 0
                        else [],
                        hovertemplate=(
                            "<b>Filtered Data</b><br>"
                            + "Diffuse Horizontal Solar Radiation"
                            + ": %{y:.2f} "
                            + VariableInfo.from_col_name(
                                Variables.DIF_HOR_RAD.col_name
                            ).get_unit(si_ip)
                            + "</b><br>"
                            + "Month: %{customdata}<br>"
                            + "Hour: %{x}:00<br>"
                            + "<extra></extra>"
                        ),
                    ),
                    row=1,
                    col=col_idx,
                )

        # Add unfiltered data traces (normal colors)
        month_glob_unfiltered = g_h_rad_month_ave.loc[
            g_h_rad_month_ave[Variables.MONTH.col_name] == month_num
        ]
        if len(month_glob_unfiltered) > 0:
            fig.add_trace(
                go.Scatter(
                    x=month_glob_unfiltered[Variables.HOUR.col_name],
                    y=month_glob_unfiltered[Variables.GLOB_HOR_RAD.col_name],
                    fill="tozeroy",
                    mode="lines",
                    line_color="orange",
                    line_width=2,
                    name="Global",
                    legendgroup="Global",
                    showlegend=not legend_shown["Global"],
                    customdata=[month_lst[month_num - 1]] * len(month_glob_unfiltered),
                    hovertemplate=(
                        "<b>"
                        + "Global Horizontal Solar Radiation"
                        + ": %{y:.2f} "
                        + VariableInfo.from_col_name(
                            Variables.GLOB_HOR_RAD.col_name
                        ).get_unit(si_ip)
                        + "</b><br>"
                        + "Month: %{customdata}<br>"
                        + "Hour: %{x}:00<br>"
                        + "<extra></extra>"  # Hides the "secondary box"
                    ),
                ),
                row=1,
                col=col_idx,
            )
            if not legend_shown["Global"]:
                legend_shown["Global"] = True

        month_dif_unfiltered = dif_h_rad_month_ave.loc[
            dif_h_rad_month_ave[Variables.MONTH.col_name] == month_num
        ]
        if len(month_dif_unfiltered) > 0:
            fig.add_trace(
                go.Scatter(
                    x=month_dif_unfiltered[Variables.HOUR.col_name],
                    y=month_dif_unfiltered[Variables.DIF_HOR_RAD.col_name],
                    fill="tozeroy",
                    mode="lines",
                    line_color="dodgerblue",
                    line_width=2,
                    name="Diffuse",
                    legendgroup="Diffuse",
                    showlegend=not legend_shown["Diffuse"],
                    customdata=[month_lst[month_num - 1]] * len(month_dif_unfiltered),
                    hovertemplate=(
                        "<b>"
                        + "Diffuse Horizontal Solar Radiation"
                        + ": %{y:.2f} "
                        + VariableInfo.from_col_name(
                            Variables.DIF_HOR_RAD.col_name
                        ).get_unit(si_ip)
                        + "</b><br>"
                        + "Month: %{customdata}<br>"
                        + "Hour: %{x}:00<br>"
                        + "<extra></extra>"  # Hides the "secondary box"
                    ),
                ),
                row=1,
                col=col_idx,
            )
            if not legend_shown["Diffuse"]:
                legend_shown["Diffuse"] = True

        fig.update_xaxes(range=[0, 25], row=1, col=col_idx)

    if si_ip == UnitSystem.SI:
        fig.update_yaxes(range=[0, 1000])
    if si_ip == UnitSystem.IP:
        fig.update_yaxes(range=[0, 400])

    fig.update_layout(
        template=template,
        dragmode=False,
    )
    return fig


def polar_graph(df, meta, global_local, var, si_ip):
    """Return the figure for the custom sun path."""
    latitude = float(meta[Variables.LAT.col_name])
    longitude = float(meta[Variables.LON.col_name])
    time_zone = float(meta[Variables.TIME_ZONE.col_name])

    # Separate filtered and unfiltered data using utility function
    # Note: For "None" variable, pass None to avoid checking for original column
    filter_var = None if var == "None" else var
    filter_info = separate_filtered_data(df, filter_var)
    df_unfiltered = filter_info["df_unfiltered"]
    df_filtered = filter_info["df_filtered"]
    original_var_col = filter_info["original_var_col"]
    use_original_for_filtered = filter_info["use_original_for_filtered"]
    # Adjust for "None" case
    if var == "None":
        original_var_col = None
        use_original_for_filtered = False

    solpos_unfiltered = df_unfiltered.loc[
        df_unfiltered[Variables.APPARENT_ELEVATION.col_name] > 0, :
    ]
    solpos_filtered = None
    if df_filtered is not None and len(df_filtered) > 0:
        solpos_filtered = df_filtered.loc[
            df_filtered[Variables.APPARENT_ELEVATION.col_name] > 0, :
        ]

    if var != "None":
        variable = VariableInfo.from_col_name(var)
        var_unit = variable.get_unit(si_ip)
        var_range = variable.get_range(si_ip)
        var_name = variable.get_name()
        var_color = variable.get_color()
        if global_local == "global":
            # Set Global values for Max and minimum
            range_z = var_range
        else:
            # Set maximum and minimum according to data
            if len(solpos_unfiltered) > 0:
                data_max, data_min = get_max_min_value(solpos_unfiltered[var])
            else:
                data_max, data_min = var_range
            range_z = [data_min, data_max]

    tz = "UTC"
    times = pd.date_range(
        "2019-01-01 00:00:00", "2020-01-01", inclusive="left", freq="h", tz=tz
    )
    delta = timedelta(days=0, hours=time_zone - 1, minutes=0)
    times = times - delta

    if var == "None":
        var_color = "orange"
        marker_size = 3
    else:
        if len(solpos_unfiltered) > 0:
            vals = solpos_unfiltered[var]
            marker_size = ((vals - vals.min()) / (vals.max() - vals.min()) + 1) * 4
        else:
            marker_size = 3

    fig = go.Figure()
    # draw altitude circles
    for i in range(10):
        pt = []
        for j in range(361):
            pt.append(j)

        fig.add_trace(
            go.Scatterpolar(
                r=[90 * cos(radians(i * 10))] * 361,
                theta=pt,
                mode="lines",
                line_color="silver",
                line_width=1,
                hovertemplate="Altitude circle<br>" + str(i * 10) + degrees_unit,
                name="",
            )
        )

    # Draw filtered data (gray) if any
    if solpos_filtered is not None and len(solpos_filtered) > 0:
        if var == "None":
            fig.add_trace(
                go.Scatterpolar(
                    r=90
                    * np.cos(
                        np.radians(
                            90 - solpos_filtered[Variables.APPARENT_ZENITH.col_name]
                        )
                    ),
                    theta=solpos_filtered[Variables.AZIMUTH.col_name],
                    mode="markers",
                    marker_color="gray",
                    marker_size=marker_size * 0.7,
                    marker_opacity=0.5,
                    marker_line_width=0,
                    customdata=np.stack(
                        (
                            solpos_filtered[Variables.DAY.col_name],
                            solpos_filtered[Variables.MONTH_NAMES.col_name],
                            solpos_filtered[Variables.HOUR.col_name],
                            solpos_filtered[Variables.ELEVATION.col_name],
                            solpos_filtered[Variables.AZIMUTH.col_name],
                        ),
                        axis=-1,
                    ),
                    hovertemplate="<b>Filtered Data</b><br>month: %{customdata[1]}"
                    + "<br>day: %{customdata[0]:.0f}"
                    + "<br>hour: %{customdata[2]:.0f}:00"
                    + "<br>sun altitude: %{customdata[3]:.2f}"
                    + degrees_unit
                    + "<br>sun azimuth: %{customdata[4]:.2f}"
                    + degrees_unit
                    + "<br>",
                    name="Filtered",
                )
            )
        else:
            # For filtered data with variable, use original values
            if use_original_for_filtered:
                filtered_var_vals = solpos_filtered[original_var_col]
            else:
                filtered_var_vals = solpos_filtered[var]

            fig.add_trace(
                go.Scatterpolar(
                    r=90
                    * np.cos(
                        np.radians(
                            90 - solpos_filtered[Variables.APPARENT_ZENITH.col_name]
                        )
                    ),
                    theta=solpos_filtered[Variables.AZIMUTH.col_name],
                    mode="markers",
                    marker=dict(
                        color="gray",
                        size=marker_size * 0.7,
                        opacity=0.5,
                        line_width=0,
                    ),
                    customdata=np.stack(
                        (
                            solpos_filtered[Variables.DAY.col_name],
                            solpos_filtered[Variables.MONTH_NAMES.col_name],
                            solpos_filtered[Variables.HOUR.col_name],
                            solpos_filtered[Variables.ELEVATION.col_name],
                            solpos_filtered[Variables.AZIMUTH.col_name],
                            filtered_var_vals,
                        ),
                        axis=-1,
                    ),
                    hovertemplate="<b>Filtered Data</b><br>month: %{customdata[1]}"
                    + "<br>day: %{customdata[0]:.0f}"
                    + "<br>hour: %{customdata[2]:.0f}:00"
                    + "<br>sun altitude: %{customdata[3]:.2f}"
                    + degrees_unit
                    + "<br>sun azimuth: %{customdata[4]:.2f}"
                    + degrees_unit
                    + "<br>"
                    + "<br><b>"
                    + var_name
                    + ": %{customdata[5]:.2f}"
                    + var_unit
                    + "</b>",
                    name="Filtered",
                )
            )

    # Draw unfiltered data (normal colors)
    if len(solpos_unfiltered) > 0:
        if var == "None":
            fig.add_trace(
                go.Scatterpolar(
                    r=90
                    * np.cos(
                        np.radians(
                            90 - solpos_unfiltered[Variables.APPARENT_ZENITH.col_name]
                        )
                    ),
                    theta=solpos_unfiltered[Variables.AZIMUTH.col_name],
                    mode="markers",
                    marker_color="orange",
                    marker_size=marker_size,
                    marker_line_width=0,
                    customdata=np.stack(
                        (
                            solpos_unfiltered[Variables.DAY.col_name],
                            solpos_unfiltered[Variables.MONTH_NAMES.col_name],
                            solpos_unfiltered[Variables.HOUR.col_name],
                            solpos_unfiltered[Variables.ELEVATION.col_name],
                            solpos_unfiltered[Variables.AZIMUTH.col_name],
                        ),
                        axis=-1,
                    ),
                    hovertemplate="month: %{customdata[1]}"
                    + "<br>day: %{customdata[0]:.0f}"
                    + "<br>hour: %{customdata[2]:.0f}:00"
                    + "<br>sun altitude: %{customdata[3]:.2f}"
                    + degrees_unit
                    + "<br>sun azimuth: %{customdata[4]:.2f}"
                    + degrees_unit
                    + "<br>",
                    name="",
                )
            )
        else:
            fig.add_trace(
                go.Scatterpolar(
                    r=90
                    * np.cos(
                        np.radians(
                            90 - solpos_unfiltered[Variables.APPARENT_ZENITH.col_name]
                        )
                    ),
                    theta=solpos_unfiltered[Variables.AZIMUTH.col_name],
                    mode="markers",
                    marker=dict(
                        color=solpos_unfiltered[var],
                        size=marker_size,
                        line_width=0,
                        colorscale=var_color,
                        cmin=range_z[0],
                        cmax=range_z[1],
                        colorbar=dict(thickness=30, title=var_unit + "<br>  "),
                    ),
                    customdata=np.stack(
                        (
                            solpos_unfiltered[Variables.DAY.col_name],
                            solpos_unfiltered[Variables.MONTH_NAMES.col_name],
                            solpos_unfiltered[Variables.HOUR.col_name],
                            solpos_unfiltered[Variables.ELEVATION.col_name],
                            solpos_unfiltered[Variables.AZIMUTH.col_name],
                            solpos_unfiltered[var],
                        ),
                        axis=-1,
                    ),
                    hovertemplate="month: %{customdata[1]}"
                    + "<br>day: %{customdata[0]:.0f}"
                    + "<br>hour: %{customdata[2]:.0f}:00"
                    + "<br>sun altitude: %{customdata[3]:.2f}"
                    + degrees_unit
                    + "<br>sun azimuth: %{customdata[4]:.2f}"
                    + degrees_unit
                    + "<br>"
                    + "<br><b>"
                    + var_name
                    + ": %{customdata[5]:.2f}"
                    + var_unit
                    + "</b>",
                    name="",
                )
            )

    # draw equinox and sostices
    for date in pd.to_datetime(["2019-03-21", "2019-06-21", "2019-12-21"]):
        times = pd.date_range(
            date,
            date + pd.Timedelta(Variables.TWENTY_FOUR_HOUR.col_name),
            freq=Variables.FIVE_MINUTE.col_name,
            tz=tz,
        )
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos[Variables.APPARENT_ELEVATION.col_name] > 0, :]

        fig.add_trace(
            go.Scatterpolar(
                r=90 * np.cos(np.radians(90 - solpos.apparent_zenith)),
                theta=solpos.azimuth,
                mode="lines",
                line_color="orange",
                line_width=3,
                customdata=90 - solpos.apparent_zenith,
                hovertemplate="<br>sun altitude: %{customdata:.2f}"
                + degrees_unit
                + "<br>sun azimuth: %{theta:.2f}"
                + degrees_unit
                + "<br>",
                name="",
            )
        )

    # draw sunpath on the 21st of each other month
    for date in pd.to_datetime(["2019-01-21", "2019-02-21", "2019-4-21", "2019-5-21"]):
        times = pd.date_range(
            date,
            date + pd.Timedelta(Variables.TWENTY_FOUR_HOUR.col_name),
            freq=Variables.FIVE_MINUTE.col_name,
            tz=tz,
        )
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos[Variables.APPARENT_ELEVATION.col_name] > 0, :]

        fig.add_trace(
            go.Scatterpolar(
                r=90 * np.cos(np.radians(90 - solpos.apparent_zenith)),
                theta=solpos.azimuth,
                mode="lines",
                line_color="orange",
                line_width=1,
                customdata=90 - solpos.apparent_zenith,
                hovertemplate="<br>sun altitude: %{customdata:.2f}"
                + degrees_unit
                + "<br>sun azimuth: %{theta:.2f}"
                + degrees_unit
                + "<br>",
                name="",
            )
        )
    fig.update_layout(
        showlegend=False,
        polar=dict(
            radialaxis_tickfont_size=10,
            angularaxis=dict(
                tickfont_size=10,
                rotation=90,  # start position of angular axis
                direction="clockwise",
            ),
        ),
    )

    fig.update_layout(
        autosize=False,
    )

    fig.update_layout(
        template=template, title_x=0.5, dragmode=False, margin=tight_margins
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False),
        )
    )
    return fig


def custom_cartesian_solar(df, meta, global_local, var, si_ip):
    """Return a graph of a latitude and longitude solar diagram."""
    latitude = float(meta[Variables.LAT.col_name])
    longitude = float(meta[Variables.LON.col_name])
    time_zone = float(meta[Variables.TIME_ZONE.col_name])
    tz = "UTC"

    # Separate filtered and unfiltered data using utility function
    # Note: For "None" variable, pass None to avoid checking for original column
    filter_var = None if var == "None" else var
    filter_info = separate_filtered_data(df, filter_var)
    df_unfiltered = filter_info["df_unfiltered"]
    df_filtered = filter_info["df_filtered"]
    original_var_col = filter_info["original_var_col"]
    use_original_for_filtered = filter_info["use_original_for_filtered"]
    # Adjust for "None" case
    if var == "None":
        original_var_col = None
        use_original_for_filtered = False

    variable = VariableInfo.from_col_name(var)
    if var != "None":
        var_unit = variable.get_unit(si_ip)
        var_range = variable.get_range(si_ip)
        var_name = variable.get_name()
        var_color = variable.get_color()
        if global_local == "global":
            # Set Global values for Max and minimum
            range_z = var_range
        else:
            # Set maximum and minimum according to data
            if len(df_unfiltered) > 0:
                data_max, data_min = get_max_min_value(df_unfiltered[var])
            else:
                data_max, data_min = var_range
            range_z = [data_min, data_max]

    if var == "None":
        var_color = "orange"
        marker_size = 3
    else:
        if len(df_unfiltered) > 0:
            vals = df_unfiltered[var]
            marker_size = ((vals - vals.min()) / (vals.max() - vals.min()) + 1) * 4
        else:
            marker_size = 3

    fig = go.Figure()

    # Draw filtered data (gray) if any
    if df_filtered is not None and len(df_filtered) > 0:
        if var == "None":
            fig.add_trace(
                go.Scatter(
                    y=df_filtered[Variables.ELEVATION.col_name],
                    x=df_filtered[Variables.AZIMUTH.col_name],
                    mode="markers",
                    marker_color="gray",
                    marker_size=marker_size * 0.7,
                    marker_opacity=0.5,
                    marker_line_width=0,
                    customdata=np.stack(
                        (
                            df_filtered[Variables.DAY.col_name],
                            df_filtered[Variables.MONTH_NAMES.col_name],
                            df_filtered[Variables.HOUR.col_name],
                            df_filtered[Variables.ELEVATION.col_name],
                            df_filtered[Variables.AZIMUTH.col_name],
                        ),
                        axis=-1,
                    ),
                    hovertemplate="<b>Filtered Data</b><br>month: %{customdata[1]}"
                    + "<br>day: %{customdata[0]:.0f}"
                    + "<br>hour: %{customdata[2]:.0f}:00"
                    + "<br>sun altitude: %{customdata[3]:.2f}"
                    + degrees_unit
                    + "<br>sun azimuth: %{customdata[4]:.2f}"
                    + degrees_unit
                    + "<br>",
                    name="Filtered",
                )
            )
        else:
            # For filtered data with variable, use original values
            if use_original_for_filtered:
                filtered_var_vals = df_filtered[original_var_col]
            else:
                filtered_var_vals = df_filtered[var]

            fig.add_trace(
                go.Scatter(
                    y=df_filtered[Variables.ELEVATION.col_name],
                    x=df_filtered[Variables.AZIMUTH.col_name],
                    mode="markers",
                    marker=dict(
                        color="gray",
                        size=marker_size * 0.7,
                        opacity=0.5,
                        line_width=0,
                    ),
                    customdata=np.stack(
                        (
                            df_filtered[Variables.DAY.col_name],
                            df_filtered[Variables.MONTH_NAMES.col_name],
                            df_filtered[Variables.HOUR.col_name],
                            df_filtered[Variables.ELEVATION.col_name],
                            df_filtered[Variables.AZIMUTH.col_name],
                            filtered_var_vals,
                        ),
                        axis=-1,
                    ),
                    hovertemplate="<b>Filtered Data</b><br>month: %{customdata[1]}"
                    + "<br>day: %{customdata[0]:.0f}"
                    + "<br>hour: %{customdata[2]:.0f}:00"
                    + "<br>sun altitude: %{customdata[3]:.2f}"
                    + degrees_unit
                    + "<br>sun azimuth: %{customdata[4]:.2f}"
                    + degrees_unit
                    + "<br>"
                    + "<br><b>"
                    + var_name
                    + ": %{customdata[5]:.2f}"
                    + var_unit
                    + "</b>",
                    name="Filtered",
                )
            )

    # Draw unfiltered data (normal colors)
    if len(df_unfiltered) > 0:
        if var == "None":
            fig.add_trace(
                go.Scatter(
                    y=df_unfiltered[Variables.ELEVATION.col_name],
                    x=df_unfiltered[Variables.AZIMUTH.col_name],
                    mode="markers",
                    marker_color="orange",
                    marker_size=marker_size,
                    marker_line_width=0,
                    customdata=np.stack(
                        (
                            df_unfiltered[Variables.DAY.col_name],
                            df_unfiltered[Variables.MONTH_NAMES.col_name],
                            df_unfiltered[Variables.HOUR.col_name],
                            df_unfiltered[Variables.ELEVATION.col_name],
                            df_unfiltered[Variables.AZIMUTH.col_name],
                        ),
                        axis=-1,
                    ),
                    hovertemplate="month: %{customdata[1]}"
                    + "<br>day: %{customdata[0]:.0f}"
                    + "<br>hour: %{customdata[2]:.0f}:00"
                    + "<br>sun altitude: %{customdata[3]:.2f}"
                    + degrees_unit
                    + "<br>sun azimuth: %{customdata[4]:.2f}"
                    + degrees_unit
                    + "<br>",
                    name="",
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    y=df_unfiltered[Variables.ELEVATION.col_name],
                    x=df_unfiltered[Variables.AZIMUTH.col_name],
                    mode="markers",
                    marker=dict(
                        color=df_unfiltered[var],
                        size=marker_size,
                        line_width=0,
                        colorscale=var_color,
                        cmin=range_z[0],
                        cmax=range_z[1],
                        colorbar=dict(thickness=30, title=var_unit + "<br>  "),
                    ),
                    customdata=np.stack(
                        (
                            df_unfiltered[Variables.DAY.col_name],
                            df_unfiltered[Variables.MONTH_NAMES.col_name],
                            df_unfiltered[Variables.HOUR.col_name],
                            df_unfiltered[Variables.ELEVATION.col_name],
                            df_unfiltered[Variables.AZIMUTH.col_name],
                            df_unfiltered[var],
                        ),
                        axis=-1,
                    ),
                    hovertemplate="month: %{customdata[1]}"
                    + "<br>day: %{customdata[0]:.0f}"
                    + "<br>hour: %{customdata[2]:.0f}:00"
                    + "<br>sun altitude: %{customdata[3]:.2f}"
                    + degrees_unit
                    + "<br>sun azimuth: %{customdata[4]:.2f}"
                    + degrees_unit
                    + "<br>"
                    + "<br><b>"
                    + var_name
                    + ": %{customdata[5]:.2f}"
                    + var_unit
                    + "</b>",
                    name="",
                )
            )

    # draw equinox and sostices
    for date in pd.to_datetime(["2019-03-21", "2019-06-21", "2019-12-21"]):
        times = pd.date_range(
            date,
            date + pd.Timedelta(Variables.TWENTY_FOUR_HOUR.col_name),
            freq=Variables.FIVE_MINUTE.col_name,
            tz=tz,
        )
        delta = timedelta(days=0, hours=time_zone - 1, minutes=0)
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos[Variables.APPARENT_ELEVATION.col_name] > 0, :]

        fig.add_trace(
            go.Scatter(
                y=(90 - solpos.apparent_zenith),
                x=solpos.azimuth,
                mode="markers",
                marker_color="orange",
                marker_size=4,
                hovertemplate="<br>sun altitude: %{y:.2f}"
                + degrees_unit
                + "<br>sun azimuth: %{x:.2f}"
                + degrees_unit
                + "<br>",
                name="",
            )
        )

    # draw sunpath on the 21st of each other month
    for date in pd.to_datetime(["2019-01-21", "2019-02-21", "2019-4-21", "2019-5-21"]):
        times = pd.date_range(
            date,
            date + pd.Timedelta(Variables.TWENTY_FOUR_HOUR.col_name),
            freq=Variables.FIVE_MINUTE.col_name,
            tz=tz,
        )
        delta = timedelta(days=0, hours=time_zone - 1, minutes=0)
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos[Variables.APPARENT_ELEVATION.col_name] > 0, :]

        fig.add_trace(
            go.Scatter(
                y=(90 - solpos.apparent_zenith),
                x=solpos.azimuth,
                mode="markers",
                marker_color="orange",
                marker_size=3,
                hovertemplate="<br>sun altitude: %{y:.2f}"
                + degrees_unit
                + "<br>sun azimuth: %{x:.2f}"
                + degrees_unit
                + "<br>",
                name="",
            )
        )

    fig.update_layout(
        showlegend=False,
        xaxis_range=[0, 360],
        yaxis_range=[0, 90],
        xaxis_tickmode="array",
        xaxis_tickvals=[
            0,
            20,
            40,
            60,
            80,
            100,
            120,
            140,
            160,
            180,
            200,
            220,
            240,
            260,
            280,
            300,
            320,
            340,
            360,
        ],
    )

    fig.update_layout(template=template, margin=tight_margins, dragmode=False)
    fig.update_xaxes(
        title_text="Azimuth angle (°)",
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )
    fig.update_yaxes(
        title_text="Altitude angle (°)",
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )

    return fig
