import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.express as px
from math import ceil, floor
import numpy as np

from my_project.global_scheme import unit_dict, range_dict, name_dict, color_dict, template

def custom_heatmap(df, global_local, var, time_filter_info, data_filter_info):
    """ Return the customizable heatmap.
    """
    time_filter = time_filter_info[0]
    start_month = time_filter_info[1][0]
    end_month = time_filter_info[1][1]
    start_hour = time_filter_info[2][0]
    end_hour = time_filter_info[2][1]
    data_filter = data_filter_info[0]
    filter_var = data_filter_info[1]
    min_val = data_filter_info[2]
    max_val = data_filter_info[3]

    if time_filter:
        if start_month <= end_month:
            mask = ((df['month'] < start_month) | (df['month'] > end_month))
            df[var][mask] = None
        else:
            mask = ((df['month'] >= end_month) & (df['month'] <= start_month))
            df[var][mask] = None

        if start_hour <= end_hour:
            mask = ((df['hour'] < start_hour) | (df['hour'] > end_hour))
            df[var][mask] = None
        else:
            mask = ((df['hour'] >= end_hour) & (df['hour'] <= start_hour))
            df[var][mask] = None

    if data_filter:
        if min_val <= max_val:
            mask = ((df[filter_var] < min_val) | (df[filter_var] > max_val))
            df[var][mask] = None  
        else:
            mask = ((df[filter_var] >= max_val) & (df[filter_var] <= min_val))
            df[var][mask] = None

    var_unit = str(var) + "_unit"
    var_unit = unit_dict[var_unit]
    var_range = str(var) + "_range"
    var_range = range_dict[var_range]
    var_name = str(var) + "_name"
    var_name = name_dict[var_name]
    var_color = str(var) + "_color"
    var_color = color_dict[var_color]
    filter_name = str(filter_var) + "_name"
    filter_name = name_dict[filter_name]
    filter_unit = str(filter_var) + "_unit"
    filter_unit = unit_dict[filter_unit]

    if global_local == "global":
        # Set Global values for Max and minimum
        range_z = var_range
    else:
        # Set maximum and minimum according to data
        data_max = (5 * ceil(df[var].max()/5))
        data_min=(5 * floor(df[var].min()/5))
        range_z = [data_min, data_max]

    title = var_name + " (" + var_unit + ")"
    month_lst = ["Jan","Feb","Mar","Apr","May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    if time_filter:
        title += "<br>between the months of " + month_lst[start_month - 1] + " and " + month_lst[end_month - 1] + " and between the hours " + str(start_hour) + ":00 and " + str(end_hour) + ":00"
    if data_filter:
        title += "<br>when the " + filter_name + " is between " + str(min_val) + " and " + str(max_val) + filter_unit

    fig = go.Figure(
            data = go.Heatmap(
                    y = df["hour"],
                    x = df["DOY"],
                    z = df[var],
                    colorscale = var_color,
                    zmin = range_z[0], 
                    zmax = range_z[1],
                    connectgaps = False,
                    hoverongaps = False,
                    customdata = np.stack((df["month_names"],df["day"]), axis = -1),
                                    hovertemplate = ('<b>'+ var + ': %{z:.2f} '+ var_unit +'</b><br>'+\
                                                    'Month: %{customdata[0]}<br>' + \
                                                    'Day: %{customdata[1]}<br>' + \
                                                    'Hour: %{y}:00<br>'),
                                    colorbar = dict(title = var_unit)
                    )
        )                     
    fig.update_layout(
        template = template,
        title = title,
        xaxis_nticks = 53,
        yaxis_nticks = 13,
        yaxis = dict(range = (1, 24)),
        xaxis = dict(range = (1, 365)),
    )
    fig.update_yaxes(title_text = "hours of the day")
    fig.update_xaxes(title_text = "days of the year")
    return fig