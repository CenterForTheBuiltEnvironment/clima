import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pythermalcomfort.models import adaptive_ashrae
from pythermalcomfort.psychrometrics import running_mean_outdoor_temperature
from pprint import pprint
from my_project.extract_df import create_df
import math
import numpy as np

template = "ggplot2"

def three_vars(df, meta):
    var_x = 'DBT' #@param ["DBT", "DPT","RH","GHrad","DNrad","DifHrad","Wdir","Wspeed","Oskycover","Vis","hour","month","azimuth","elevation","comfortASHRAE55"]
    var_y = 'RH' #@param ["DBT", "DPT","RH","GHrad","DNrad","DifHrad","Wdir","Wspeed","Oskycover","Vis","hour","month","azimuth","elevation","comfortASHRAE55"]
    color_by = 'Wdir' #@param ["DBT", "DPT","RH","GHrad","DNrad","DifHrad","Wdir","Wspeed","Oskycover","Vis","hour","month","azimuth","elevation","comfortASHRAE55"]

    if color_by == "DBT" or color_by == "DPT":
        colorscale = ["#00b3ff", "#000082", "#ff0000", "#ffff00"]
    elif color_by== "RH":
        colorscale = ["#ffe600", "#00c8ff", "#0000ff"]
    elif color_by == "GHrad" or color_by == "DNrad" or color_by == "DifHrad":
        colorscale = ["#293a59", "#ff0000", "#ffff00", "#ffffff"]
    elif color_by == "Wspeed":
        colorscale = ["#94f3ff", "#30b3ff", "#6f02c2", "#c20202"]
    elif color_by == "Wdir":
        colorscale = ["#1690c4", "#4bad54", "#fae978", "#fae978", "#d90012", "#1690c4"]
    elif color_by == "hour":
        colorscale = ["#000000", "#355e7e", "#6b5c7b", "#c06c84", "#f8b195", "#c92a42", "#c92a42", "#c92a42", "#000000"]
    elif color_by == "Oskycover" or color_by == "Vis":
        colorscale = ["#00aaff", "#ffffff", "#c2c2c2"]

    fig = px.scatter(df, x = var_x, y = var_y, color = color_by,
                    color_continuous_scale = colorscale,
                    opacity = 0.7,
                    marginal_x = "histogram", marginal_y = "histogram")
    return fig

def two_vars(df, meta):
    return ...