from datetime import timedelta
from math import ceil, cos, floor, radians

import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from my_project.global_scheme import (
    template,
    mapping_dictionary,
    degrees_unit,
    tight_margins,
    month_lst,
)
from plotly.subplots import make_subplots
from pvlib import solarposition


def monthly_solar(epw_df, si_ip):
    g_h_rad_month_ave = (
        epw_df.groupby(["month", "hour"])["glob_hor_rad"].median().reset_index()
    )
    dif_h_rad_month_ave = (
        epw_df.groupby(["month", "hour"])["dif_hor_rad"].median().reset_index()
    )
    fig = make_subplots(
        rows=1,
        cols=12,
        subplot_titles=month_lst,
    )

    for i in range(12):

        fig.add_trace(
            go.Scatter(
                x=g_h_rad_month_ave.loc[g_h_rad_month_ave["month"] == i + 1, "hour"],
                y=g_h_rad_month_ave.loc[
                    g_h_rad_month_ave["month"] == i + 1, "glob_hor_rad"
                ],
                fill="tozeroy",
                mode="lines",
                line_color="orange",
                line_width=2,
                name=None,
                showlegend=False,
                customdata=epw_df.loc[epw_df["month"] == i + 1, "month_names"],
                hovertemplate=(
                    "<b>"
                    + "Global Horizontal Solar Radiation"
                    + ": %{y:.2f} "
                    + mapping_dictionary["glob_hor_rad"][si_ip]["unit"]
                    + "</b><br>"
                    + "Month: %{customdata}<br>"
                    + "Hour: %{x}:00<br>"
                ),
            ),
            row=1,
            col=i + 1,
        )

        fig.add_trace(
            go.Scatter(
                x=dif_h_rad_month_ave.loc[
                    dif_h_rad_month_ave["month"] == i + 1, "hour"
                ],
                y=dif_h_rad_month_ave.loc[
                    dif_h_rad_month_ave["month"] == i + 1, "dif_hor_rad"
                ],
                fill="tozeroy",
                mode="lines",
                line_color="dodgerblue",
                line_width=2,
                name=None,
                showlegend=False,
                customdata=epw_df.loc[epw_df["month"] == i + 1, "month_names"],
                hovertemplate=(
                    "<b>"
                    + "Diffuse Horizontal Solar Radiation"
                    + ": %{y:.2f} "
                    + mapping_dictionary["dif_hor_rad"][si_ip]["unit"]
                    + "</b><br>"
                    + "Month: %{customdata}<br>"
                    + "Hour: %{x}:00<br>"
                ),
            ),
            row=1,
            col=i + 1,
        )

        fig.update_xaxes(range=[0, 25], row=1, col=i + 1)
        if si_ip == "si":
            fig.update_yaxes(range=[0, 1000], row=1, col=i + 1)
        if si_ip == "ip":
            fig.update_yaxes(range=[0, 400], row=1, col=i + 1)

    fig.update_layout(
        template=template,
        dragmode=False,
    )
    return fig


def polar_graph(df, meta, global_local, var, si_ip):
    """Return the figure for the custom sun path."""
    latitude = float(meta["lat"])
    longitude = float(meta["lon"])
    time_zone = float(meta["time_zone"])
    solpos = df.loc[df["apparent_elevation"] > 0, :]

    if var != "None":
        var_unit = mapping_dictionary[var][si_ip]["unit"]
        var_range = mapping_dictionary[var][si_ip]["range"]
        var_name = mapping_dictionary[var]["name"]
        var_color = mapping_dictionary[var]["color"]
        if global_local == "global":
            # Set Global values for Max and minimum
            range_z = var_range
        else:
            # Set maximum and minimum according to data
            data_max = 5 * ceil(solpos[var].max() / 5)
            data_min = 5 * floor(solpos[var].min() / 5)
            range_z = [data_min, data_max]

    tz = "UTC"
    times = pd.date_range(
        "2019-01-01 00:00:00", "2020-01-01", inclusive="left", freq="H", tz=tz
    )
    delta = timedelta(days=0, hours=time_zone - 1, minutes=0)
    times = times - delta
    solpos = df.loc[df["apparent_elevation"] > 0, :]

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
                r=90 * np.cos(np.radians(90 - solpos["apparent_zenith"])),
                theta=solpos["azimuth"],
                mode="markers",
                marker_color="orange",
                marker_size=marker_size,
                marker_line_width=0,
                customdata=np.stack(
                    (
                        solpos["day"],
                        solpos["month_names"],
                        solpos["hour"],
                        solpos["elevation"],
                        solpos["azimuth"],
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
                r=90 * np.cos(np.radians(90 - solpos["apparent_zenith"])),
                theta=solpos["azimuth"],
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
                        solpos["day"],
                        solpos["month_names"],
                        solpos["hour"],
                        solpos["elevation"],
                        solpos["azimuth"],
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
        times = pd.date_range(date, date + pd.Timedelta("24h"), freq="5min", tz=tz)
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos["apparent_elevation"] > 0, :]

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
        times = pd.date_range(date, date + pd.Timedelta("24h"), freq="5min", tz=tz)
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos["apparent_elevation"] > 0, :]

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
    latitude = float(meta["lat"])
    longitude = float(meta["lon"])
    time_zone = float(meta["time_zone"])
    tz = "UTC"

    if var != "None":
        var_unit = mapping_dictionary[var][si_ip]["unit"]
        var_range = mapping_dictionary[var][si_ip]["range"]
        var_name = mapping_dictionary[var]["name"]
        var_color = mapping_dictionary[var]["color"]
        if global_local == "global":
            # Set Global values for Max and minimum
            range_z = var_range
        else:
            # Set maximum and minimum according to data
            data_max = 5 * ceil(df[var].max() / 5)
            data_min = 5 * floor(df[var].min() / 5)
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
                y=df["elevation"],
                x=df["azimuth"],
                mode="markers",
                marker_color="orange",
                marker_size=marker_size,
                marker_line_width=0,
                customdata=np.stack(
                    (
                        df["day"],
                        df["month_names"],
                        df["hour"],
                        df["elevation"],
                        df["azimuth"],
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
                y=df["elevation"],
                x=df["azimuth"],
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
                        df["day"],
                        df["month_names"],
                        df["hour"],
                        df["elevation"],
                        df["azimuth"],
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
        times = pd.date_range(date, date + pd.Timedelta("24h"), freq="5min", tz=tz)
        delta = timedelta(days=0, hours=time_zone - 1, minutes=0)
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos["apparent_elevation"] > 0, :]

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
        times = pd.date_range(date, date + pd.Timedelta("24h"), freq="5min", tz=tz)
        delta = timedelta(days=0, hours=time_zone - 1, minutes=0)
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos["apparent_elevation"] > 0, :]

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
