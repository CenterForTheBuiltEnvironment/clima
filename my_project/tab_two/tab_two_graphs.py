import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.express as px

from my_project.extract_df import create_df
from my_project.template_graphs import create_violin
from my_project.global_scheme import template

# Color scheme and templates
DBT_color = 'Reds'
RH_color = 'GnBu'
GHrad_color = 'YlOrRd_r'
Wspeed_color = 'Blues_r'

##################
### WORLD MAP ###
#################
def world_map(df, meta): 
    """ Return the world map showing the current location. 
    """
    latitude = float(meta[-4])
    longitude = float(meta[-3])
    city = meta[1]
    country = meta[3]
    time_zone = float(meta[-2])
    lat_long_df = pd.DataFrame(data = {"Lat": [latitude], "Long":[longitude], "City": [city], 
    "Country": [country], "Time Zone" :[time_zone], "Size": [10]})

    fig = px.scatter_mapbox(lat_long_df, lat = "Lat", lon = "Long", hover_name = "City", hover_data = ["Country", "Time Zone"],
                        color_discrete_sequence = ["red"], zoom = 5, height = 300, size = "Size")
    fig.update_layout(
        mapbox_style = "white-bg",
        mapbox_layers = [
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
    fig.update_layout(margin = {"r":0, "t":0, "l":0, "b":0})
    return fig

###################################
### DAY VS NIGHT VIOLIN GRAPHS ###
##################################
def dbt_violin(df, meta):
    city = meta[1]
    country = meta[3]
    location_name = city + ", " + country
    title = {
        'text': "Temperature" + " profile<br>" + location_name,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
    y_title = "Temperature (degC)"
    y_lim = (-40, 50)
    return create_violin(df, "DBT", title, y_title, y_lim)

def humidity_violin(df, meta):
    city = meta[1]
    country = meta[3]
    location_name = city + ", " + country
    title = {
        'text': "Relative Humidity" + " profile<br>" + location_name + "",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
    y_title = "Relative Humitdity (%)"
    y_lim = [0, 100]
    return create_violin(df, "RH", title, y_title, y_lim)

def solar_violin(df, meta):
    city = meta[1]
    country = meta[3]
    location_name = city + ", " + country
    title = {
        'text': "Global Horizontal Solar Radiation" + " profile<br>" + location_name + "",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
    y_title = "Global Horizontal Solar Radiation (W/h m^2)"
    y_lim = [0, 1200]
    return create_violin(df, "GHrad", title, y_title, y_lim)

def wind_violin(df, meta):
    city = meta[1]
    country = meta[3]
    location_name = city + ", " + country
    title = {
        'text': "Wind Speed" + " profile<br>" + location_name + "",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
    y_title = "Wind Speed (m/s)"
    y_lim = [0, 35]
    return create_violin(df, "Wspeed", title, y_title, y_lim)


