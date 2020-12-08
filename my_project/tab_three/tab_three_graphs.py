import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pythermalcomfort.models import adaptive_ashrae
from pythermalcomfort.psychrometrics import running_mean_outdoor_temperature
from math import ceil, floor
import numpy as np

from my_project.extract_df import create_df
from my_project.template_graphs import heatmap, yearly_profile, daily_profile
from my_project.global_scheme import template, range_dict

def get_ashrae(df):
    """ calculate the ashrae for the yearly DBT 
    """
    DBT_day_ave = df.groupby(['DOY'])['DBT'].mean().reset_index()
    DBT_day_ave = DBT_day_ave['DBT'].tolist()
    n = 7  
    cmf55 = []
    lo80 = []
    hi80 = []
    lo90 = []
    hi90 = []
    for i in range(len(DBT_day_ave)):
        if i < n:
            lastDays = DBT_day_ave[-n + i:]+DBT_day_ave[0:i]
        else:
            lastDays = DBT_day_ave[i - n:i]
        lastDays.reverse()
        lastDays = [10 if x <= 10 else x for x in lastDays]
        lastDays = [32 if x >= 32 else x for x in lastDays]
        rmt = running_mean_outdoor_temperature(lastDays, alpha = 0.9)
        if DBT_day_ave[i] >= 40: 
            DBT_day_ave[i] = 40
        elif DBT_day_ave[i] <= 10: 
            DBT_day_ave[i] = 10
        r = adaptive_ashrae(tdb = DBT_day_ave[i], tr = DBT_day_ave[i], t_running_mean = rmt, v = 0.5)
        cmf55.append(r['tmp_cmf'])
        lo80.append(r['tmp_cmf_80_low'])
        hi80.append(r['tmp_cmf_80_up'])
        lo90.append(r['tmp_cmf_90_low'])
        hi90.append(r['tmp_cmf_90_up'])
    return lo80, hi80, lo90, hi90

######################
### YEARLY PROFILE ###
######################
def yearly_profile_dbt(df, global_local):
    """ Return the figure for the yearly profile for DBT variable.
    """
    lo80, hi80, lo90, hi90 = get_ashrae(df)
    return yearly_profile(df, "DBT", global_local, lo80, hi80, lo90, hi90)

def yearly_profile_rh(df, global_local):
    """ Return the figure for the yearly profile for RH variable 
    """
    return yearly_profile(df, "RH", global_local, [], [], [], [])

#####################
### DAILY PROFILE ###
#####################
def daily_profile_dbt(df, global_local):
    """ Return the figure for the yearly profile for DBT variable.
    """
    return daily_profile(df, "DBT", global_local)

def daily_profile_rh(df, global_local):
    """ Return the figure for the yearly profile for RH variable 
    """
    return daily_profile(df, "RH", global_local)

#########################
### HEATMAP FUNCTIONS ### 
#########################
def heatmap_dbt(df, global_local):
    """ Return the figure for the heatmap for DBT variable.
    """
    return heatmap(df, "DBT", global_local)

def heatmap_rh(df, global_local):
    """ Return the figure for the heatmap for RH variable.
    """
    return heatmap(df, "RH", global_local)

# def heatmap_dbt(epw_df, meta, units, global_local):
#     """ Return a figure of the heatmap for DBT
#     """
#     colors = ["#00b3ff", "#000082", "#ff0000", "#ffff00"]
#     title = "Dry Bulb Temperatures (degC)"
#     if global_local == "global":
#         # Set Global values for max and min
#         data_min = range_dict['DBT_range'][0]
#         data_max = range_dict['DBT_range'][1]
#     else:
#         # Set maximum and minimum according to data
#         data_min = (5 * floor(epw_df["DBT"].min() / 5))
#         data_max = (5 * ceil(epw_df["DBT"].max() / 5))
#     z_vals = epw_df["DBT"]
#     hover = 'DOY: %{x}<br>hour: %{y}<br>RH: %{z}<extra></extra>'
#     return heatmap(epw_df, colors, title, data_min, data_max, z_vals, hover)

# def heatmap_humidity(epw_df, meta, units, global_local):
#     """ Return a figure of the heatmap for humidity. 
#     """
#     colors = ["#ffe600", "#00c8ff", "#0000ff"]
#     title = "Relative Humiditys (degC)"
#     if global_local == "global":
#         # Set Global values for max and min
#         data_min = range_dict['RH_range'][0]
#         data_max = range_dict['RH_range'][1]
#     else:
#         # Set maximum and minimum according to data
#         data_min = (5 * floor(epw_df["RH"].min() / 5))
#         data_max = (5 * ceil(epw_df["RH"].max() / 5))
#     z_vals = epw_df["RH"]
#     hover = 'DOY: %{x}<br>hour: %{y}<br>RH: %{z}<extra></extra>'
#     return heatmap(epw_df, colors, title, data_min, data_max, z_vals, hover)
