import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.express as px

from my_project.global_scheme import template, color_dict, range_dict
from my_project.template_graphs import heatmap, wind_rose


#################
### WIND ROSE ###
#################
# def annual_windrose(df, meta):
#     """ Return the annual windrose.
#     """
#     return wind_rose(df, meta, "Annual Wind Rose", [1, 12], [1, 24])

# def winter_windrose(df, meta):
#     """ Return the winter windrose graph for the seasonal section.
#     """
#     return wind_rose(df, meta, "", [12, 2], [1, 24])

# def spring_windrose(df, meta):
#     """ Return the spring windrose graph for the seasonal section.
#     """
#     return wind_rose(df, meta, "", [3, 5], [1, 24])

# def summer_windrose(df, meta):
#     """ Return the summer windrose graph for the seasonal section.
#     """
#     return wind_rose(df, meta, "", [6, 8], [1, 24])

# def fall_windrose(df, meta):
#     """ Return the fall windrose graph for the seasonal section.
#     """
#     return wind_rose(df, meta, "", [9, 12], [1, 24])

# def morning_windrose(df, meta):
#     """ Return the morning windrose for the daily section.
#     """
#     return wind_rose(df, meta, "", [1, 12], [6, 13])

# def noon_windrose(df, meta):
#     """ Return the afternoon windrose for the daily section.
#     """
#     return wind_rose(df, meta, "", [1, 12], [14, 21])

# def night_windrose(df, meta):
#     """ Return the night windrose for the daily section.
#     """
#     return wind_rose(df, meta, "", [1, 12], [22, 5])

################
### HEAT MAP ###
################
# def wind_speed_heatmap(df, global_local):
#     return heatmap(df, 'Wspeed', global_local)

# def wind_direction_heatmap(df, global_local):
#     return heatmap(df, 'Wdir', global_local)