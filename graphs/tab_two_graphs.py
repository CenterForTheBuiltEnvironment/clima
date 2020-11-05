import pandas as pd
import plotly.express as px
from extract_df import create_df
import plotly.graph_objects as go
from plotly.colors import n_colors

default_url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw"
epw_df, meta = create_df(default_url)

# Meta data
city = meta[1]
country = meta[3]
latitude = float(meta[-4])
longitude = float(meta[-3])
time_zone = float(meta[-2])
location_name = city + ", " + country

# Color scheme and templates
DBT_color = 'Reds'
RH_color = 'GnBu'
GHrad_color = 'YlOrRd_r'
Wspeed_color = 'Blues_r'
template = "ggplot2"

### Violin Graphs ###
def create_violin(custom_ylim, title, y, height, width, labels):
    """ General function to create a violin plot. 
    """
    fig = px.violin(data_frame = epw_df, x = None, y = y, template = template, 
        range_y = custom_ylim, height = height, width = width, points = False, box = False, 
        title = title, labels = labels)
    return fig

def temperature():
    """ Violin plot for Temperature Profile.
    """
    custom_ylim = (-40, 50)
    title = "Temperature" + " profile<br>" + location_name
    y = "DBT"
    height = 1000
    width = 350
    labels = dict(DBT = "Temperature (degC)")
    return create_violin(custom_ylim, title, y, height, width, labels)

def humidity():
    """ Violin plot for Humidity Profile.
    """
    custom_ylim = (0, 100)
    title = ("Relative Humidity" + " profile<br>" + location_name + "")
    y = "RH"
    height = 1000
    width = 350
    labels = dict(RH = "Relative Humitdity (%)")
    return create_violin(custom_ylim, title, y, height, width, labels)

def solar():
    """ Violin plot for Solar Radiation.
    """
    custom_ylim = (0, 1200)
    title = ("Solar Radiation" + " profile<br>" + location_name + "")
    y = epw_df.loc[epw_df["GHrad"] > 0, "GHrad"]
    height = 1000
    width = 350
    labels = dict(y = "Global Horizontal Solar Radiation (W/h m^2)")
    return create_violin(custom_ylim, title, y, height, width, labels)

def wind():
    """ Violin plot for Wind Speed.
    """
    custom_ylim = (0, 25)
    title = ("Wind Speed" + " profile<br>" + location_name + "")
    y = "Wspeed"
    height = 1000
    width = 350 
    labels = dict(Wspeed = "Wind Speed (m/s)")
    return create_violin(custom_ylim, title, y, height, width, labels)

def monthly_dbt():
    """
    """
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    colors = n_colors('rgb(0, 200, 200)', 'rgb(200, 10, 10)', 12, colortype='rgb')
    fig = go.Figure()
    for i in range(0,12):
        data_line = epw_df.loc[epw_df["month"] == i + 1, "DBT"]
        fig.add_trace(go.Violin(y = data_line, line_color = colors[i], name = month_names[i]))
    fig.update_traces(meanline_visible = True, orientation = 'v', width = 0.8, points = False)
    return fig

def monthly_dbt_day_night():
    fig = go.Figure()

    maskDay = (epw_df["GHrad"]>0)
    maskNight = (epw_df["GHrad"]<=0)

    data_day = epw_df.loc[maskDay, "DBT"]
    data_night = epw_df.loc[maskNight, "DBT"]

    monthNames_day = epw_df.loc[maskDay, "month_names"]
    monthNames_nigth = epw_df.loc[maskNight, "month_names"]

    fig.add_trace(go.Violin(x = monthNames_day, y = data_day, line_color = 'rgb(200, 10, 10)', name = "Day", side = 'negative'))
    fig.add_trace(go.Violin(x = monthNames_nigth, y = data_night, line_color = 'rgb(0, 200, 200)', name = "Night", side = 'positive'))


    fig.update_traces(meanline_visible = True, orientation = 'v', width = 0.8, points = False,)
    fig.update_layout(xaxis_showgrid = True, xaxis_zeroline = True, violinmode = 'overlay')
    return fig 

