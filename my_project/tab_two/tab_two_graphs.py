import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from my_project.template_graphs import violin
from plotly.colors import n_colors


#################
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



