import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pvlib import solarposition
from datetime import time, datetime, timedelta, timezone
import numpy as np
from math import cos, radians, ceil, floor
from my_project.extract_df import create_df
from my_project.template_graphs import heatmap, daily_profile
from my_project.global_scheme import template, unit_dict, range_dict, name_dict, color_dict

####################################
### POLAR/LAT-LONG GRAPH SELECT ###
###################################
def lat_long_solar(epw_df, meta):
    """ Return a graph of a latitude and longitude solar diagram. 
    """
    # Meta data
    city = meta[1]
    country = meta[3]
    latitude = float(meta[-4])
    longitude = float(meta[-3])
    time_zone = float(meta[-2])
    location_name = city + ", " + country
    # Adjust dateime based on timezone
    date = datetime(2000, 6, 21, 12 - 1, 0, 0, 0, tzinfo = timezone.utc)
    tz = timedelta(days = 0, hours = time_zone - 1, minutes = 0)
    date = date-tz
    tz = 'UTC'

    times = pd.date_range('2019-01-01 00:00:00', '2020-01-01', closed = 'left',
                        freq = 'H', tz = tz)
    delta = timedelta(days = 0, hours = time_zone - 1, minutes = 0)
    times = times - delta
    solpos = solarposition.get_solarposition(times, latitude, longitude)
    # remove nighttime
    solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

    fig = go.Figure()

    # draw annalemma
    fig.add_trace(go.Scatter(
        y = (90 - solpos.apparent_zenith),
        x = solpos.azimuth ,
        mode = 'markers',
        marker_color = "orange",
        marker_size = 1
        ))

    # draw equinox and sostices
    for date in pd.to_datetime(['2019-03-21', '2019-06-21', '2019-12-21']):
        times = pd.date_range(date, date + pd.Timedelta('24h'), freq = '5min', tz = tz)
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

        fig.add_trace(go.Scatter(
                        y = (90 - solpos.apparent_zenith),
                        x = solpos.azimuth ,
                        mode = 'markers',
                        marker_color = "orange",
                        marker_size = 4 
                    ))  

    # draw sunpath on the 21st of each other month 
    for date in pd.to_datetime(['2019-01-21', '2019-02-21', '2019-4-21', '2019-5-21']):
        times = pd.date_range(date, date+pd.Timedelta('24h'), freq = '5min', tz = tz)
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

        fig.add_trace(go.Scatter(
                        y = (90 - solpos.apparent_zenith),
                        x = solpos.azimuth ,
                        mode = 'markers',
                        marker_color = "orange",
                        marker_size = 3 
                    )) 

    fig.update_layout(
        title = "Cartesian Sun-Path",
        title_x = 0.5,
        template = template,
        showlegend = False, xaxis_range = [0, 360], 
        yaxis_range = [0, 90], xaxis_tickmode = "array", 
        xaxis_tickvals = [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360]
    )

    return fig 

def polar_solar(epw_df, meta):
    """
    """
    # Meta data
    city = meta[1]
    country = meta[3]
    latitude = float(meta[-4])
    longitude = float(meta[-3])
    time_zone = float(meta[-2])
    location_name = city + ", " + country
    # Adjust dateime based on timezone
    date = datetime(2000, 6, 21, 12 - 1, 0, 0, 0, tzinfo = timezone.utc)
    tz = timedelta(days = 0, hours = time_zone - 1, minutes = 0)
    date = date-tz

    tz = 'UTC'
    times = pd.date_range('2019-01-01 00:00:00', '2020-01-01', closed='left',
                        freq = 'H', tz = tz)
    delta = timedelta(days = 0, hours = time_zone - 1, minutes = 0)
    times = times - delta
    solpos = solarposition.get_solarposition(times, latitude, longitude)
    # remove nighttime
    solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

    fig = go.Figure()

    # draw altitude circles
    for i in range(10):
        pt = []
        for j in range(360):
            pt.append(j)

        fig.add_trace(go.Scatterpolar(
                r = [90 * cos(radians(i * 10))] * 361,
                theta = pt ,
                mode = 'lines',
                line_color = "silver",
                line_width = 1
            )) 
    
    # draw annalemma
    fig.add_trace(go.Scatterpolar(
                r = 90 * np.cos(np.radians(90 - solpos.apparent_zenith)),
                theta = solpos.azimuth ,
                mode = 'markers',
                marker_color = "orange",
                marker_size = 1 
            ))

    # draw equinox and sostices
    for date in pd.to_datetime(['2019-03-21', '2019-06-21', '2019-12-21']):
        times = pd.date_range(date, date+pd.Timedelta('24h'), freq = '5min', tz = tz)
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

        fig.add_trace(go.Scatterpolar(
                    r = 90 * np.cos(np.radians(90 - solpos.apparent_zenith)),
                    theta = solpos.azimuth ,
                    mode = 'lines',
                    line_color = "orange",
                    line_width = 3
                ))  

    # draw sunpath on the 21st of each other month 
    for date in pd.to_datetime(['2019-01-21', '2019-02-21', '2019-4-21', '2019-5-21']):
        times = pd.date_range(date, date + pd.Timedelta('24h'), freq = '5min', tz = tz)
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

        fig.add_trace(go.Scatterpolar(
                    r = 90 * np.cos(np.radians(90 - solpos.apparent_zenith)),
                    theta = solpos.azimuth ,
                    mode = 'lines',
                    line_color = "orange",
                    line_width = 1
                )) 
    fig.update_layout(
        title = "Spherical Sun-Path",
        title_x = 0.5,
        height = 600,
        template = template,
        showlegend = False,
        polar = dict(
        radialaxis_tickfont_size = 10,
        angularaxis = dict(
            tickfont_size = 10,
            rotation = 90, # start position of angular axis
            direction = "counterclockwise"
        )
    ))
    return fig

#######################
### SOLAR RADIATION ###
#######################
def monthly_solar(epw_df, meta):
    """
    """
    GHrad_month_ave = epw_df.groupby(['month','hour'])['GHrad'].median().reset_index()
    DifHrad_month_ave = epw_df.groupby(['month','hour'])['DifHrad'].median().reset_index()
    monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    fig = make_subplots(rows = 1, cols = 12, subplot_titles = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"))

    for i in range(12):
        
        fig.add_trace(
            go.Scatter(
                x = GHrad_month_ave.loc[GHrad_month_ave["month"] == i + 1,"hour"], 
                y = GHrad_month_ave.loc[GHrad_month_ave["month"] == i + 1, "GHrad"], fill = 'tozeroy',
                mode = "lines", line_color = "orange", line_width = 2, name = None, showlegend = False
            ),
            row = 1, col = i + 1,
        )
        fig.add_trace(
            go.Scatter(
                x = DifHrad_month_ave.loc[DifHrad_month_ave["month"] == i + 1, "hour"], 
                y = DifHrad_month_ave.loc[DifHrad_month_ave["month"] == i + 1, "DifHrad"], fill = "tozeroy",
                mode = "lines", line_color = "dodgerblue", line_width = 2, name = None, showlegend = False
            ),
            row = 1, col = i + 1,
        )
        fig.add_trace(
            go.Scatter(
                x = epw_df.loc[epw_df["month"] == i + 1, "hour"], 
                y = epw_df.loc[epw_df["month"] == i + 1, "GHrad"],
                mode="markers",marker_color="#ff8400",
                marker_size = 2, name = monthList[i], showlegend = False
            ),
            row = 1, col = i + 1,
        )
        fig.add_trace(
            go.Scatter(
                x = epw_df.loc[epw_df["month"] == i + 1, "hour"],
                y = epw_df.loc[epw_df["month"] == i + 1, "DifHrad"],
                mode = "markers", marker_color = "skyblue",
                marker_size = 2, name = monthList[i], showlegend = False
            ),
            row = 1, col = i + 1,
        )
        fig.update_xaxes(range = [0, 25], row = 1, col = i + 1)
        fig.update_yaxes(range = [0, 1000], row = 1, col = i + 1)
    fig.update_layout(template = template)
    return fig

def yearly_solar_radiation(df):
    """ Return the figure with yearly solar radiation split. 
    """
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = [0],
            y = [0],
            mode = "markers", 
            marker_size = df["GHrad"].sum() / (8760 / 2),
            marker_sizemode = "area",
            marker_color = "#f9c74f",
            text = [str(df["GHrad"].sum()) + " KW/h/m2"],
            name = "Global Solar Radiation"
        )
    )
    fig.add_trace(
        go.Scatter(
            x = [0],
            y = [0],
            mode = "markers",
            marker_size = (df["GHrad"].sum() - df["DifHrad"].sum()) / (8760 / 2),
            marker_sizemode = "area",
            marker_color = "#f3722c",
            text = [str(df["DifHrad"].sum()) + " KW/h/m2"],
            name = "Direct Solar Radiation"
        )
    )
    fig.update_layout(
        template = template,
        legend = dict(
            x = 0,
            y = -0.5
        ),
    )
    return fig

###################
### CLOUD COVER ###
###################
# def cloud_cover(df, global_local, var, min_val, max_val):
#     """ Return the custom summary barcharts.
#     """

#     var_unit = str(var) + "_unit"
#     var_unit = unit_dict[var_unit]
#     var_range = str(var) + "_range"
#     var_range = range_dict[var_range]
#     var_name = str(var) + "_name"
#     var_name = name_dict[var_name]
#     var_color = str(var) + "_color"
#     var_color = color_dict[var_color]

#     color_below = var_color[0]
#     color_above = var_color[-1]
#     color_in = var_color[len(var_color)//2]

#     month_in = []
#     month_below = []
#     month_above = []

#     min_val = str(min_val)
#     max_val = str(max_val)

#     for i in range(1, 13):
#         query = "month==" + str(i) + " and (" + var + ">=" + min_val + " and " + var + "<=" + max_val + ")"
#         print(df.query(query))
#         a = df.query(query)["DOY"].count()
#         month_in.append(a)
#         query = "month==" + str(i) + " and (" + var + "<" + min_val + ")"
#         b = df.query(query)["DOY"].count()
#         month_below.append(b)
#         query = "month==" + str(i) + " and " + var + ">" + max_val
#         c = df.query(query)["DOY"].count()
#         month_above.append(c)

#     fig = go.Figure()
#     trace1 = go.Bar(x = list(range(0, 13)), y = month_in, name = " IN range", marker_color = color_in)
#     trace2 = go.Bar(x = list(range(0, 13)), y = month_below, name = " BELOW range", marker_color = color_below)
#     trace3 = go.Bar(x = list(range(0, 13)), y = month_above, name = " ABOVE range", marker_color = color_above)
#     data = [trace2, trace1, trace3]

#     fig = go.Figure(data = data)
#     fig.update_layout(barmode = 'stack')

#     title = "Number of hours the " + var_name + " is in the range " + min_val+" to " + max_val + " " + var_unit
#     fig.update_yaxes(title_text = "hours")
#     fig.update_layout(title = title, barnorm = "")
#     return fig

#######################
### CUSTOM SUN PATH ###
#######################
def polar_graph(df, meta, global_local, var):
    """ Return the figure for the custom sun path.
    """
    latitude = float(meta[-4])
    longitude = float(meta[-3])
    time_zone = float(meta[-2])
    var_unit = unit_dict[str(var) + "_unit"]
    var_range = range_dict[str(var) + "_range"]
    var_name = name_dict[str(var) + "_name"]
    var_color = color_dict[str(var) + "_color"]
    Title = var_name + " (" + var_unit + ") on Spherical Sun-Path"
    tz = 'UTC'
    times = pd.date_range('2019-01-01 00:00:00', '2020-01-01', closed = 'left', freq = 'H', tz = tz)
    delta = timedelta(days = 0, hours = time_zone - 1, minutes = 0)
    times = times - delta
    solpos = df.loc[df['apparent_elevation'] > 0, :]
    if global_local == "global":
        # Set Global values for Max and minimum
        range_z = var_range
    else:
        # Set maximum and minimum according to data
        data_max = (5 * ceil(solpos[var].max() / 5))
        data_min = (5 * floor(solpos[var].min() / 5))
        range_z = [data_min, data_max]
    var = solpos[var]
    marker_size = (((var - var.min()) / var.max()) + 1) * 4

    fig = go.Figure()
    for i in range(10):
        pt = [j for j in range(360)]
        fig.add_trace(
            go.Scatterpolar(
                r = [90 * cos(radians(i * 10))] * 361,
                theta = pt,
                mode = 'lines',
                line_color = "silver",
                line_width = 1
            )
        ) 
    # Draw annalemma
    fig.add_trace(
        go.Scatterpolar(
            r = 90 * np.cos(np.radians(90 - solpos["apparent_zenith"])),
            theta = solpos["azimuth"],
            mode = 'markers',
            marker = dict(
                color = var,
                size = marker_size,
                line_width = 0,
                colorscale = var_color,
                cmin = range_z[0],
                cmax = range_z[1],
                colorbar = dict(
                    thickness = 30,
                    title = var_unit + "<br>  ")
            )        
        )
    )
    # draw equinox and sostices
    for date in pd.to_datetime(['2019-03-21', '2019-06-21', '2019-12-21']):
        times = pd.date_range(date, date + pd.Timedelta('24h'), freq = '5min', tz = tz)
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]
        fig.add_trace(
            go.Scatterpolar(
                r = 90 * np.cos(np.radians(90 - solpos.apparent_zenith)),
                theta = solpos.azimuth ,
                mode = 'lines',
                line_color = "orange",
                line_width = 3
            )
        )  
    # Draw sunpath on the 21st of each other month 
    for date in pd.to_datetime(['2019-01-21', '2019-02-21', '2019-4-21', '2019-5-21']):
        times = pd.date_range(date, date+pd.Timedelta('24h'), freq = '5min', tz = tz)
        times = times - delta
        solpos = solarposition.get_solarposition(times, latitude, longitude)
        solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]
        fig.add_trace(
            go.Scatterpolar(
                r = 90 * np.cos(np.radians(90 - solpos.apparent_zenith)),
                theta = solpos.azimuth,
                mode = 'lines',
                line_color = "orange",
                line_width = 1
            )
        ) 
    fig.update_layout(
        showlegend = False,
        polar = dict(
        radialaxis_tickfont_size = 10,
        angularaxis = dict(
                tickfont_size = 10,
                rotation = 90, # start position of angular axis
                direction = "counterclockwise"
            )
        )
    )
    fig.update_layout(
        autosize = False,
        width = 800,
        height = 800,
        title = Title,
        title_x = 0.5,
    )
    return fig