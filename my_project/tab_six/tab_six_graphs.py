import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.express as px
from math import ceil, floor
import numpy as np

from my_project.global_scheme import unit_dict, range_dict, name_dict, color_dict, template


month_lst = ["Jan","Feb","Mar","Apr","May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

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

def custom_summary(df, global_local, var, time_filter_info, data_filter_info, normalize):
    """ Return the custom summary barcharts.
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

    color_below = var_color[0]
    color_above = var_color[-1]
    color_in = var_color[len(var_color)//2]

    if time_filter:
        if start_month <= end_month:
            df.loc[(df['month'] < start_month) | (df['month'] > end_month)] 
        else:
            df.loc[(df['month'] >= end_month) & (df['month'] <= start_month)] 
        if start_hour <= end_hour:
            df.loc[(df['hour'] < start_hour) | (df['hour'] > end_hour)] 
        else:
            df.loc[(df['hour'] >= end_hour) & (df['hour'] <= start_hour)] 

    if data_filter:
        if min_val <= max_val:
            df.loc[(df[filter_var] < min_val) | (df[filter_var] > max_val)] 
        else:
            df.loc[(df[filter_var] >= max_val) & (df[filter_var] <= min_val)] 
    
    month_in = []
    month_below = []
    month_above = []

    min_val = str(min_val)
    max_val = str(max_val)

    for i in range(1, 13):
        query = "month==" + str(i) + " and (" + var + ">=" + min_val + " and " + var + "<=" + max_val + ")"
        a = df.query(query)["DOY"].count()
        month_in.append(a)
        query = "month==" + str(i) + " and (" + var + "<" + min_val + ")"
        b = df.query(query)["DOY"].count()
        month_below.append(b)
        query = "month==" + str(i) + " and " + var + ">" + max_val
        c = df.query(query)["DOY"].count()
        month_above.append(c)

    fig = go.Figure()
    trace1 = go.Bar(x = list(range(0, 13)), y = month_in, name = " IN range", marker_color = color_in)
    trace2 = go.Bar(x = list(range(0, 13)), y = month_below, name = " BELOW range", marker_color = color_below)
    trace3 = go.Bar(x = list(range(0, 13)), y = month_above, name = " ABOVE range", marker_color = color_above)
    data = [trace2, trace1, trace3]

    fig = go.Figure(data = data)
    fig.update_layout(barmode = 'stack')

    if normalize:
        title = "Percentage of time the " + var_name + " is in the range " + min_val + " to " + max_val + " " + var_unit
        fig.update_yaxes(title_text = "%")
        fig.update_layout(title = title, barnorm = "percent")
    else:
        title = "Number of hours the " + var_name + " is in the range " + min_val+" to " + max_val + " " + var_unit
        fig.update_yaxes(title_text = "hours")
        fig.update_layout(title = title, barnorm = "")
    if time_filter:
        title += "<br>between the months of " + month_lst[start_month - 1] + " to " + month_lst[end_month - 1] + " and between " + str(start_hour) + ":00-" + str(end_hour) + ":00 hours"
    if data_filter:
        title += ",<br>when the " + filter_name + " is between " + str(min_val) + " and " + str(min_val) + filter_unit
    return fig

def three_var_graph(df, global_local, var_x, var_y, colorby, time_filter_info3, data_filter_info3):
    """ Return the custom graph plotting three variables.
    """
    time_filter = time_filter_info3[0]
    start_month = time_filter_info3[1][0]
    end_month = time_filter_info3[1][1]
    start_hour = time_filter_info3[2][0]
    end_hour = time_filter_info3[2][1]
    data_filter = data_filter_info3[0]
    filter_var = data_filter_info3[1]
    min_val = data_filter_info3[2]
    max_val = data_filter_info3[3]

    var_unit = str(colorby) + "_unit"
    var_unit = unit_dict[var_unit]
    var_range = str(colorby) + "_range"
    var_range = range_dict[var_range]
    var_name = str(colorby) + "_name"
    var_name = name_dict[var_name]
    var_color = str(colorby) + "_color"
    var_color = color_dict[var_color]
    colorscale = var_color

    if time_filter:
        if start_month <= end_month:
            df.loc[(df['month'] < start_month) | (df['month'] > end_month)]
        else:
            df.loc[(df['month'] >= end_month) & (df['month'] <= start_month)]

        if start_hour <= end_hour:
            df.loc[(df['hour'] < start_hour ) | (df['hour'] > end_hour)]
        else:
            df.loc[(df['hour'] >= end_hour) & (df['hour'] <= start_hour )]

    if data_filter:
        if min_val <= max_val:
            df.loc[(df[filter_var] < min_val) | (df[filter_var] > max_val)]
        else:
            df.loc[(df[filter_var] >= max_val) & (df[filter_var] <= min_val)]

    title = var_x + " vs " + var_y + " colored by " + colorby
    fig = px.scatter(
            df, 
            x = var_x, 
            y = var_y, 
            color = colorby,
            color_continuous_scale = colorscale,
            opacity = 0.4,
            range_color = var_range,
            marginal_x = "histogram", 
            marginal_y = "histogram",
            title = title
        )
    return fig

def two_var_graph(df, global_local, var_x, var_y, colorby, time_filter_info3, data_filter_info3):
    """ Return the custom graph plotting two variables.
    """
    time_filter = time_filter_info3[0]
    start_month = time_filter_info3[1][0]
    end_month = time_filter_info3[1][1]
    start_hour = time_filter_info3[2][0]
    end_hour = time_filter_info3[2][1]
    data_filter = data_filter_info3[0]
    filter_var = data_filter_info3[1]
    min_val = data_filter_info3[2]
    max_val = data_filter_info3[3]

    var_unit = str(colorby) + "_unit"
    var_unit = unit_dict[var_unit]
    var_range = str(colorby) + "_range"
    var_range = range_dict[var_range]
    var_name = str(colorby) + "_name"
    var_name = name_dict[var_name]
    var_color = str(colorby) + "_color"
    var_color = color_dict[var_color]

    title =  "Simultaneous frequency of " + var_x + " and " + var_y

    if time_filter:
        if start_month <= end_month:
            df.loc[(df['month'] < start_month) | (df['month'] > end_month)]
        else:
            df.loc[(df['month'] >= end_month) & (df['month'] <= start_month)]

        if start_hour <= end_hour:
            df.loc[(df['hour'] < start_hour ) | (df['hour'] > end_hour)]
        else:
            df.loc[(df['hour'] >= end_hour) & (df['hour'] <= start_hour )]

    if data_filter:
        if min_val <= max_val:
            df.loc[(df[filter_var] < min_val) | (df[filter_var] > max_val)]
        else:
            df.loc[(df[filter_var] >= max_val) & (df[filter_var] <= min_val)]

    fig = px.density_heatmap(
                df, 
                x = var_x, 
                y = var_y,
                title = title,
                marginal_x = "histogram",
                marginal_y = "histogram",
            )
    return fig 