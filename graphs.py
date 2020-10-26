import pandas as pd
import plotly.express as px
from extract_df import create_df

default_url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw"
epw_df, location_name = create_df(default_url)

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

def create_violin_temperature():
    """ Violin plot for Temperature Profile.
    """
    custom_ylim = (-40, 50)
    title = "Temperature" + " profile<br>" + location_name
    y = "DBT"
    height = 1000
    width = 350
    labels = dict(DBT = "Temperature (degC)")
    return create_violin(custom_ylim, title, y, height, width, labels)

def create_violin_humidity():
    """ Violin plot for Humidity Profile.
    """
    custom_ylim = (0, 100)
    title = ("Relative Humidity" + " profile<br>" + location_name + "")
    y = "RH"
    height = 1000
    width = 350
    labels = dict(RH = "Relative Humitdity (%)")
    return create_violin(custom_ylim, title, y, height, width, labels)

def create_violin_solar():
    """ Violin plot for Solar Radiation.
    """
    custom_ylim = (0, 1200)
    title = ("Solar Radiation" + " profile<br>" + location_name + "")
    y = epw_df.loc[epw_df["GHrad"] > 0, "GHrad"]
    height = 1000
    width = 350
    labels = dict(y = "Global Horizontal Solar Radiation (W/h m^2)")
    return create_violin(custom_ylim, title, y, height, width, labels)

def create_violin_wind():
    """ Violin plot for Wind Speed.
    """
    custom_ylim = (0, 25)
    title = ("Wind Speed" + " profile<br>" + location_name + "")
    y = "Wspeed"
    height = 1000
    width = 350 
    labels = dict(Wspeed = "Wind Speed (m/s)")
    return create_violin(custom_ylim, title, y, height, width, labels)

