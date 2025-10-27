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


def monthly_solar(epw_df, si_ip):
    g_h_rad_month_ave = (
        epw_df.groupby([Variables.MONTH.col_name, Variables.HOUR.col_name])[
            Variables.GLOB_HOR_RAD.col_name
        ]
        .median()
        .reset_index()
    )
    dif_h_rad_month_ave = (
        epw_df.groupby([Variables.MONTH.col_name, Variables.HOUR.col_name])[
            Variables.DIF_HOR_RAD.col_name
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

    for month_num in range(1, 13):
        col_idx = month_num
        # We only need legend entries for the first pair, since the others repeat.
        is_first = col_idx == 1

        fig.add_trace(
            go.Scatter(
                x=g_h_rad_month_ave.loc[
                    g_h_rad_month_ave[Variables.MONTH.col_name] == month_num,
                    Variables.HOUR.col_name,
                ],
                y=g_h_rad_month_ave.loc[
                    g_h_rad_month_ave[Variables.MONTH.col_name] == month_num,
                    Variables.GLOB_HOR_RAD.col_name,
                ],
                fill="tozeroy",
                mode="lines",
                line_color="orange",
                line_width=2,
                name="Global",
                showlegend=is_first,
                customdata=epw_df.loc[
                    epw_df[Variables.MONTH.col_name] == month_num,
                    Variables.MONTH_NAMES.col_name,
                ],
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

        fig.add_trace(
            go.Scatter(
                x=dif_h_rad_month_ave.loc[
                    dif_h_rad_month_ave[Variables.MONTH.col_name] == month_num,
                    Variables.HOUR.col_name,
                ],
                y=dif_h_rad_month_ave.loc[
                    dif_h_rad_month_ave[Variables.MONTH.col_name] == month_num,
                    Variables.DIF_HOR_RAD.col_name,
                ],
                fill="tozeroy",
                mode="lines",
                line_color="dodgerblue",
                line_width=2,
                name="Diffuse",
                showlegend=is_first,
                customdata=epw_df.loc[
                    epw_df[Variables.MONTH.col_name] == month_num,
                    Variables.MONTH_NAMES.col_name,
                ],
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
    solpos = df.loc[df[Variables.APPARENT_ELEVATION.col_name] > 0, :]
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
            data_max, data_min = get_max_min_value(solpos[var])
            range_z = [data_min, data_max]

    tz = "UTC"
    times = pd.date_range(
        "2019-01-01 00:00:00", "2020-01-01", inclusive="left", freq="h", tz=tz
    )
    delta = timedelta(days=0, hours=time_zone - 1, minutes=0)
    times = times - delta
    solpos = df.loc[df[Variables.APPARENT_ELEVATION.col_name] > 0, :]

    if var == "None":
        var_color = "orange"
        marker_size = 3
    else:
        vals = solpos[var]
        marker_size = ((vals - vals.min()) / (vals.max() - vals.min()) + 1) * 4

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
    # Draw annalemma
    if var == "None":
        fig.add_trace(
            go.Scatterpolar(
                r=90
                * np.cos(np.radians(90 - solpos[Variables.APPARENT_ZENITH.col_name])),
                theta=solpos[Variables.AZIMUTH.col_name],
                mode="markers",
                marker_color="orange",
                marker_size=marker_size,
                marker_line_width=0,
                customdata=np.stack(
                    (
                        solpos[Variables.DAY.col_name],
                        solpos[Variables.MONTH_NAMES.col_name],
                        solpos[Variables.HOUR.col_name],
                        solpos[Variables.ELEVATION.col_name],
                        solpos[Variables.AZIMUTH.col_name],
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
                * np.cos(np.radians(90 - solpos[Variables.APPARENT_ZENITH.col_name])),
                theta=solpos[Variables.AZIMUTH.col_name],
                mode="markers",
                marker=dict(
                    color=solpos[var],
                    size=marker_size,
                    line_width=0,
                    colorscale=var_color,
                    cmin=range_z[0],
                    cmax=range_z[1],
                    colorbar=dict(thickness=30, title=var_unit + "<br>  "),
                ),
                customdata=np.stack(
                    (
                        solpos[Variables.DAY.col_name],
                        solpos[Variables.MONTH_NAMES.col_name],
                        solpos[Variables.HOUR.col_name],
                        solpos[Variables.ELEVATION.col_name],
                        solpos[Variables.AZIMUTH.col_name],
                        solpos[var],
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
            data_max, data_min = get_max_min_value(df[var])
            range_z = [data_min, data_max]

    if var == "None":
        var_color = "orange"
        marker_size = 3
    else:
        vals = df[var]
        marker_size = ((vals - vals.min()) / (vals.max() - vals.min()) + 1) * 4

    fig = go.Figure()

    # draw annalemma
    if var == "None":
        fig.add_trace(
            go.Scatter(
                y=df[Variables.ELEVATION.col_name],
                x=df[Variables.AZIMUTH.col_name],
                mode="markers",
                marker_color="orange",
                marker_size=marker_size,
                marker_line_width=0,
                customdata=np.stack(
                    (
                        df[Variables.DAY.col_name],
                        df[Variables.MONTH_NAMES.col_name],
                        df[Variables.HOUR.col_name],
                        df[Variables.ELEVATION.col_name],
                        df[Variables.AZIMUTH.col_name],
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
                y=df[Variables.ELEVATION.col_name],
                x=df[Variables.AZIMUTH.col_name],
                mode="markers",
                marker=dict(
                    color=df[var],
                    size=marker_size,
                    line_width=0,
                    colorscale=var_color,
                    cmin=range_z[0],
                    cmax=range_z[1],
                    colorbar=dict(thickness=30, title=var_unit + "<br>  "),
                ),
                customdata=np.stack(
                    (
                        df[Variables.DAY.col_name],
                        df[Variables.MONTH_NAMES.col_name],
                        df[Variables.HOUR.col_name],
                        df[Variables.ELEVATION.col_name],
                        df[Variables.AZIMUTH.col_name],
                        df[var],
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
