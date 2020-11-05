import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pvlib import solarposition
from datetime import time, datetime, timedelta, timezone
import numpy as np
import math 
from extract_df import create_df

default_url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw"
epw_df, meta = create_df(default_url)
template = "ggplot2"

# Meta data
city = meta[1]
country = meta[3]
latitude = float(meta[-4])
longitude = float(meta[-3])
time_zone = float(meta[-2])
location_name = (city + ", " + country)

# Adjust dateime based on timezone
date = datetime(2000, 6, 21, 12 - 1, 0, 0, 0, tzinfo = timezone.utc)
tz = timedelta(days = 0, hours = time_zone - 1, minutes = 0)
date = date-tz

def lat_long_solar():
    """ Return a graph of a latitude and longitude solar diagram. 
    """

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
        showlegend = False, xaxis_range = [0, 360], 
        yaxis_range = [0, 90], xaxis_tickmode = "array", 
        xaxis_tickvals = [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360]
    )

    return fig 

def polar_solar():
    """
    """
    tz = 'UTC'
    times = pd.date_range('2019-01-01 00:00:00', '2020-01-01', closed='left',
                        freq = 'H', tz = tz)
    delta=timedelta(days = 0, hours = time_zone - 1, minutes = 0)
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
                r = [90 * math.cos(math.radians(i * 10))] * 361,
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

def daily_solar():
    """
    """
    GHrad_month_ave = epw_df.groupby(['month','hour'])['GHrad'].median().reset_index()
    monthList = ["Jan","Feb","Mar","Apr","May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    fig = make_subplots(rows = 1, cols = 12, subplot_titles = ("Jan","Feb","Mar","Apr","May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"))
    for i in range(12):
        fig.add_trace(
            go.Scatter(x = epw_df.loc[epw_df["month"] == i + 1,"hour"], 
                        y = epw_df.loc[epw_df["month"] == i + 1, "GHrad"],
                        mode = "markers", marker_color = "#ffbb00",
                        marker_size = 2, name = monthList[i], showlegend = False),
                        row = 1, col = i + 1
            )
        fig.add_trace(
            go.Scatter(x = GHrad_month_ave.loc[GHrad_month_ave["month"] == i + 1, "hour"], 
                        y = GHrad_month_ave.loc[GHrad_month_ave["month"] == i + 1, "GHrad"],
                        mode = "lines", line_color = "orange", line_width = 2, name = None, 
                        showlegend = False), row = 1, col = i + 1,
        )
        fig.update_xaxes(range = [0, 25], row = 1, col = i + 1)
        fig.update_yaxes(range = [0, 1000], row = 1, col = i + 1)
    fig.update_layout(template = template)
    return fig
