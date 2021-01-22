from datetime import datetime, time, timedelta, timezone
from math import ceil, cos, floor, radians
import math

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from my_project.extract_df import create_df
from my_project.global_scheme import (color_dict, name_dict, range_dict,
                                      template, unit_dict)
from my_project.template_graphs import daily_profile, heatmap
from plotly.subplots import make_subplots
from pvlib import solarposition


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

    # draw equinox and sostices
    for date in pd.to_datetime(['2019-03-21', '2019-06-21', '2019-12-21']):
      times = pd.date_range(date, date+pd.Timedelta('24h'), freq='5min', tz=tz)
      times=times-delta
      solpos = solarposition.get_solarposition(times, latitude, longitude)
      solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

      fig.add_trace(go.Scatter(
            y = (90-solpos.apparent_zenith),
            x = solpos.azimuth ,
            mode = 'markers',
            marker_color="orange",
            marker_size=4,
            hovertemplate =
            "<br>sun altitude: %{y:.2f}"+"\u00B0 deg"+
            "<br>sun azimuth: %{x:.2f}"+"\u00B0 deg"+
            "<br>",
            name="",
            ))  

    #draw sunpath on the 21st of each other month 
    for date in pd.to_datetime(['2019-01-21', '2019-02-21', '2019-4-21', '2019-5-21']):
      times = pd.date_range(date, date+pd.Timedelta('24h'), freq='5min', tz=tz)
      times=times-delta
      solpos = solarposition.get_solarposition(times, latitude, longitude)
      solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

      fig.add_trace(go.Scatter(
            y = (90-solpos.apparent_zenith),
            x = solpos.azimuth ,
            mode = 'markers',
            marker_color="orange",
            marker_size=3,
            hovertemplate =
            "<br>sun altitude: %{y:.2f}"+"\u00B0 deg"+
            "<br>sun azimuth: %{x:.2f}"+"\u00B0 deg"+
            "<br>",
            name="",
            )) 
      
    #draw annalemma
    fig.add_trace(go.Scatter(
            y = epw_df['elevation'],
            x = epw_df['azimuth'] ,
            mode = 'markers',
            marker=dict(
            color="orange",
            size=3,
            line_width=0,
            ), 
            customdata=np.stack((epw_df["day"],epw_df["month_names_long"],epw_df["hour"], 
                        epw_df["elevation"],epw_df["azimuth"]),axis=-1),
            hovertemplate =
            "month: %{customdata[1]}"+
            "<br>day: %{customdata[0]:.0f}"+
            "<br>hour: %{customdata[2]:.0f}:00"+
            "<br>sun altitude: %{customdata[3]:.2f}"+"\u00B0 deg"+
            "<br>sun azimuth: %{customdata[4]:.2f}"+"\u00B0 deg"+
            "<br>",
            name="",
            ))
    

    fig.update_layout(
        showlegend = False,xaxis_range=[0,360],yaxis_range=[0,90], xaxis_tickmode="array", 
        xaxis_tickvals=[0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360]
        )
    Title = "Cartesian Sun-Path"
    fig.update_layout(template=template,title=Title,)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

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

    #draw altitude circles
    for i in range(10):
      pt=[]
      for j in range(361):
        pt.append(j)

      fig.add_trace(go.Scatterpolar(
          r = [90*math.cos(math.radians(i*10))]*361,
          theta = pt ,
          mode = 'lines',
          line_color="silver",
          line_width=1,
          #customdata=10,
          hovertemplate ="Altitude circle<br>"+str(i*10)+"\u00B0 deg",
          name="", 
          )) 
      
    #draw annalemma

    fig.add_trace(go.Scatterpolar(
      r = 90*np.cos(np.radians(90-solpos["apparent_zenith"])),
      theta = solpos["azimuth"] ,
      mode = 'markers',
      marker_color="orange",
      marker_size=3,
      marker_line_width=0,
      customdata=np.stack((solpos["day"],solpos["month_names_long"],solpos["hour"], 
                      solpos["elevation"],solpos["azimuth"]),axis=-1),
      hovertemplate =
      "month: %{customdata[1]}"+
      "<br>day: %{customdata[0]:.0f}"+
      "<br>hour: %{customdata[2]:.0f}:00"+
      "<br>sun altitude: %{customdata[3]:.2f}"+"\u00B0 deg"+
      "<br>sun azimuth: %{customdata[4]:.2f}"+"\u00B0 deg"+
      "<br>",
        name="",
      ))
        
    fig.add_trace(go.Scatterpolar(
        r = 90*np.cos(np.radians(90-solpos["apparent_zenith"])),
        theta = solpos["azimuth"] ,
        mode = 'markers',
        marker=dict(
            color="orange",
            size=3,
            line_width=0,
            customdata=np.stack((solpos["day"],solpos["month_names_long"],solpos["hour"], 
                                solpos["elevation"],solpos["azimuth"]),axis=-1),
        hovertemplate =
        "month: %{customdata[1]}"+
        "<br>day: %{customdata[0]:.0f}"+
        "<br>hour: %{customdata[2]:.0f}:00"+
        "<br>sun altitude: %{customdata[3]:.2f}"+"\u00B0 deg"+
        "<br>sun azimuth: %{customdata[4]:.2f}"+"\u00B0 deg"+
        "<br>",
        name="",        
    ))
    )
      

    # draw equinox and sostices
    for date in pd.to_datetime(['2019-03-21', '2019-06-21', '2019-12-21']):
      times = pd.date_range(date, date+pd.Timedelta('24h'), freq='5min', tz=tz)
      times=times-delta
      solpos = solarposition.get_solarposition(times, latitude, longitude)
      solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

      fig.add_trace(go.Scatterpolar(
            r = 90*np.cos(np.radians(90-solpos.apparent_zenith)),
            theta = solpos.azimuth ,
            mode = 'lines',
            line_color="orange",
            line_width=3,
            customdata= 90-solpos.apparent_zenith,
            hovertemplate =
            "<br>sun altitude: %{customdata:.2f}"+"\u00B0 deg"+
            "<br>sun azimuth: %{theta:.2f}"+"\u00B0 deg"+
            "<br>",
            name="",
            ))  

    #draw sunpath on the 21st of each other month 
    for date in pd.to_datetime(['2019-01-21', '2019-02-21', '2019-4-21', '2019-5-21']):
      times = pd.date_range(date, date+pd.Timedelta('24h'), freq='5min', tz=tz)
      times=times-delta
      solpos = solarposition.get_solarposition(times, latitude, longitude)
      solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

      fig.add_trace(go.Scatterpolar(
            r = 90*np.cos(np.radians(90-solpos.apparent_zenith)),
            theta = solpos.azimuth ,
            mode = 'lines',
            line_color="orange",
            line_width=1,
            customdata= 90-solpos.apparent_zenith,
            hovertemplate =
            "<br>sun altitude: %{customdata:.2f}"+"\u00B0 deg"+
            "<br>sun azimuth: %{theta:.2f}"+"\u00B0 deg"+
            "<br>",
            name="",
            )) 
      
    fig.update_layout(
        showlegend = False,
        polar = dict(
          radialaxis_tickfont_size = 10,
          angularaxis = dict(
            tickfont_size=10,
            rotation=90, # start position of angular axis
            direction="counterclockwise"
          )
        ))

    fig.update_layout(
        autosize=False,
        width=800,
        height=800,
        #template="simple_white",
    )

    Title = "Spherical Sun-Path"
    fig.update_layout(title=Title)

    fig.update_layout(template=template,title=Title,)

    fig.update_layout(
        polar = dict(
            radialaxis = dict(visible=False),
        )
    )
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
             go.Scatter(x=GHrad_month_ave.loc[GHrad_month_ave["month"]==i+1,"hour"],
                     y=GHrad_month_ave.loc[GHrad_month_ave["month"]==i+1,"GHrad"],
                     fill='tozeroy',
                     mode="lines",line_color="orange",line_width=2,
                     name="",showlegend=False,
                     customdata=epw_df.loc[epw_df["month"]==i+1,"month_names_long"],
                     hovertemplate = ('<b>'+"Global Horizontal Solar Radiation"+': %{y:.2f} '+"Wh/m<sup>2</sup>"+'</b><br>'+\
                                    'Month: %{customdata}<br>'+\
                                    'Hour: %{x}:00<br>'),
                     ),
                row=1, col=i+1,
            )

        fig.add_trace(
            go.Scatter(x=DifHrad_month_ave.loc[DifHrad_month_ave["month"]==i+1,"hour"],
                    y=DifHrad_month_ave.loc[DifHrad_month_ave["month"]==i+1,"DifHrad"],
                    fill="tozeroy",
                    mode="lines",line_color="dodgerblue",line_width=2,
                    name="",showlegend=False,
                    customdata=epw_df.loc[epw_df["month"]==i+1,"month_names_long"],
                    hovertemplate = ('<b>'+"Diffuse Horizontal Solar Radiation"+': %{y:.2f} '+"Wh/m<sup>2</sup>"+'</b><br>'+\
                                    'Month: %{customdata}<br>'+\
                                    'Hour: %{x}:00<br>'),
                    ),
                row=1, col=i+1,
            )

      #print(len(epw_df.loc[epw_df["month"]==i+1,"hour"])/24)
        fig.update_xaxes( range=[0, 25], row=1, col=i+1)
        fig.update_yaxes( range=[0, 1000], row=1, col=i+1)
    fig.update_layout(template=template)

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

    #draw altitude circles
    for i in range(10):
      pt=[]
      for j in range(361):
        pt.append(j)

      fig.add_trace(go.Scatterpolar(
          r = [90*math.cos(math.radians(i*10))]*361,
          theta = pt ,
          mode = 'lines',
          line_color="silver",
          line_width=1,
          #customdata=10,
          hovertemplate ="Altitude circle<br>"+str(i*10)+"\u00B0 deg",
          name="", 
          )) 
      
    #draw annalemma
    fig.add_trace(go.Scatterpolar(
        r = 90*np.cos(np.radians(90-solpos["apparent_zenith"])),
        theta = solpos["azimuth"] ,
        mode = 'markers',
        marker=dict(
          color=solpos[var],
          size=marker_size,
          line_width=0,
          colorscale=var_color,
          cmin=range_z[0],
          cmax=range_z[1],
          colorbar=dict(
              thickness=30,
              title=var_unit+"<br>  ")
          ),
        customdata=np.stack((solpos["day"],solpos["month_names_long"],solpos["hour"], 
                             solpos["elevation"],solpos["azimuth"],solpos[var]),axis=-1),
        hovertemplate =
        "month: %{customdata[1]}"+
        "<br>day: %{customdata[0]:.0f}"+
        "<br>hour: %{customdata[2]:.0f}:00"+
        "<br>sun altitude: %{customdata[3]:.2f}"+"\u00B0 deg"+
        "<br>sun azimuth: %{customdata[4]:.2f}"+"\u00B0 deg"+
        "<br>"+
        "<br><b>"+var_name+': %{customdata[5]:.2f}'+var_unit+"</b>",
        name="",
        ))
      

    # draw equinox and sostices
    for date in pd.to_datetime(['2019-03-21', '2019-06-21', '2019-12-21']):
      times = pd.date_range(date, date+pd.Timedelta('24h'), freq='5min', tz=tz)
      times=times-delta
      solpos = solarposition.get_solarposition(times, latitude, longitude)
      solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

      fig.add_trace(go.Scatterpolar(
            r = 90*np.cos(np.radians(90-solpos.apparent_zenith)),
            theta = solpos.azimuth ,
            mode = 'lines',
            line_color="orange",
            line_width=3,
            customdata= 90-solpos.apparent_zenith,
            hovertemplate =
            "<br>sun altitude: %{customdata:.2f}"+"\u00B0 deg"+
            "<br>sun azimuth: %{theta:.2f}"+"\u00B0 deg"+
            "<br>",
            name="",
            ))  

    #draw sunpath on the 21st of each other month 
    for date in pd.to_datetime(['2019-01-21', '2019-02-21', '2019-4-21', '2019-5-21']):
      times = pd.date_range(date, date+pd.Timedelta('24h'), freq='5min', tz=tz)
      times=times-delta
      solpos = solarposition.get_solarposition(times, latitude, longitude)
      solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

      fig.add_trace(go.Scatterpolar(
            r = 90*np.cos(np.radians(90-solpos.apparent_zenith)),
            theta = solpos.azimuth ,
            mode = 'lines',
            line_color="orange",
            line_width=1,
            customdata= 90-solpos.apparent_zenith,
            hovertemplate =
            "<br>sun altitude: %{customdata:.2f}"+"\u00B0 deg"+
            "<br>sun azimuth: %{theta:.2f}"+"\u00B0 deg"+
            "<br>",
            name="",
            )) 
      
    fig.update_layout(
        showlegend = False,
        polar = dict(
          radialaxis_tickfont_size = 10,
          angularaxis = dict(
            tickfont_size=10,
            rotation=90, # start position of angular axis
            direction="counterclockwise"
          )
        ))

    fig.update_layout(
        autosize=False,
        width=800,
        height=800,
        #template="simple_white",
    )


    fig.update_layout(title=Title)

    fig.update_layout(template=template,title=Title,)

    fig.update_layout(
        polar = dict(
            radialaxis = dict(visible=False),
        )
    )

    return fig

def custom_lat_long_solar(df, meta, global_local, var):
    """ Return a graph of a latitude and longitude solar diagram. 
    """
    # Meta data
    city = meta[1]
    country = meta[3]
    latitude = float(meta[-4])
    longitude = float(meta[-3])
    time_zone = float(meta[-2])

    var_unit = unit_dict[str(var) + "_unit"]
    var_range = range_dict[str(var) + "_range"]
    var_name = name_dict[str(var) + "_name"]
    var_color = color_dict[str(var) + "_color"]

    if global_local == "global":
        # Set Global values for Max and minimum
        range_z = var_range
    else:
        # Set maximum and minimum according to data
        data_max=(5*ceil(df[var].max()/5))
        data_min=(5*floor(df[var].min()/5))
        range_z = [data_min, data_max]

    var = df[var]
    marker_size = (((var - var.min()) / var.max()) + 1) * 4
    
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

    # draw equinox and sostices
    for date in pd.to_datetime(['2019-03-21', '2019-06-21', '2019-12-21']):
      times = pd.date_range(date, date+pd.Timedelta('24h'), freq='5min', tz=tz)
      times=times-delta
      solpos = solarposition.get_solarposition(times, latitude, longitude)
      solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

      fig.add_trace(go.Scatter(
            y = (90-solpos.apparent_zenith),
            x = solpos.azimuth ,
            mode = 'markers',
            marker_color="orange",
            marker_size=4,
            hovertemplate =
            "<br>sun altitude: %{y:.2f}"+"\u00B0 deg"+
            "<br>sun azimuth: %{x:.2f}"+"\u00B0 deg"+
            "<br>",
            name="",
            ))  

    #draw sunpath on the 21st of each other month 
    for date in pd.to_datetime(['2019-01-21', '2019-02-21', '2019-4-21', '2019-5-21']):
      times = pd.date_range(date, date+pd.Timedelta('24h'), freq='5min', tz=tz)
      times=times-delta
      solpos = solarposition.get_solarposition(times, latitude, longitude)
      solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

      fig.add_trace(go.Scatter(
            y = (90-solpos.apparent_zenith),
            x = solpos.azimuth ,
            mode = 'markers',
            marker_color="orange",
            marker_size=3,
            hovertemplate =
            "<br>sun altitude: %{y:.2f}"+"\u00B0 deg"+
            "<br>sun azimuth: %{x:.2f}"+"\u00B0 deg"+
            "<br>",
            name="",
            )) 
      
    #draw annalemma
      fig.add_trace(go.Scatter(
      y = df['elevation'],
      x = df['azimuth'] ,
      mode = 'markers',
      marker=dict(
        color=var,
        size=marker_size,
        line_width=0,
        colorscale=var_color,
        cmin=range_z[0],
        cmax=range_z[1],
        colorbar=dict(
            thickness=30,
            title=var_unit+"<br>  ")
      ),
        customdata=np.stack((df["day"],df["month_names_long"],df["hour"], 
                             df["elevation"],df["azimuth"],df[var]),axis=-1),
        hovertemplate =
        "month: %{customdata[1]}"+
        "<br>day: %{customdata[0]:.0f}"+
        "<br>hour: %{customdata[2]:.0f}:00"+
        "<br>sun altitude: %{customdata[3]:.2f}"+"\u00B0 deg"+
        "<br>sun azimuth: %{customdata[4]:.2f}"+"\u00B0 deg"+
        "<br>"+
        "<br><b>"+var_name+': %{customdata[5]:.2f}'+var_unit+"</b>",
        name="",
        ) 
      )

    fig.update_layout(
        showlegend = False,xaxis_range=[0,360],yaxis_range=[0,90], xaxis_tickmode="array", xaxis_tickvals=[0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360]
        )
    Title = var_name+" ("+var_unit+") on Spherical Sun-Path"
    fig.update_layout(template=template,title=Title,)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

    return fig 
