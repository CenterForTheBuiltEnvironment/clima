import pandas as pd
import plotly.express as px


def world_map(meta):
    """Return the world map showing the current location."""
    latitude = float(meta["lat"])
    longitude = float(meta["lon"])
    city = meta["city"]
    country = meta["country"]
    time_zone = float(meta["time_zone"])
    lat_long_df = pd.DataFrame(
        data={
            "Lat": [latitude],
            "Long": [longitude],
            "City": [city],
            "Country": [country],
            "Time Zone": [time_zone],
            "Size": [10],
        }
    )

    fig = px.scatter_mapbox(
        lat_long_df,
        lat="Lat",
        lon="Long",
        hover_name="City",
        hover_data=["Country", "Time Zone"],
        color_discrete_sequence=["red"],
        zoom=5,
        height=300,
        size="Size",
    )
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
