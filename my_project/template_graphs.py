from plotly.colors import n_colors
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from math import ceil, floor

from .global_scheme import template
from my_project.global_scheme import unit_dict, range_dict, name_dict

def violin(df, var, global_local):
    """ Return day night violin based on the var col
    """
    mask_day = (df["hour"] >= 8) & (df["hour"] < 20)
    mask_night = (df["hour"] < 8) | (df["hour"] >= 20)
    var_unit = str(var) + "_unit"
    var_unit = unit_dict[var_unit]
    var_range = str(var) + "_range"
    var_range = range_dict[var_range]
    var_name = str(var) + "_name"
    var_name = name_dict[var_name]
    if global_local == "global":
        # Set Global values for Max and minimum
        range_y = var_range
    else:
        # Set maximumand minimum according to data
        data_min = (5 * ceil(df[var].max() / 5))
        data_max = (5 * floor(df[var].min() / 5))
        range_y = [data_min, data_max]
    colors = n_colors('rgb(0, 200, 200)', 'rgb(200, 10, 10)', 12, colortype = 'rgb')
    data_day = df.loc[mask_day, var]
    data_night = df.loc[mask_night, var]
    fig = go.Figure()
    fig.add_trace(go.Violin(x = df["fake_year"], y = data_day, line_color = 'rgb(200, 10, 10)', name = "Day", side = 'negative'))
    fig.add_trace(go.Violin(x = df["fake_year"], y = data_night, line_color = 'rgb(0, 200, 200)', name = "Night", side = 'positive'))
    fig.update_yaxes(range = var_range)
    fig.update_traces(meanline_visible = True, orientation = 'v', width = 0.8, points = False)
    fig.update_layout(xaxis_showgrid = False, xaxis_zeroline = False, height = 1000, width = 350, violingap = 0, violingroupgap = 0, violinmode = 'overlay')
    title = var_name + " (" + var_unit + ")"
    fig.update_layout(template = template, title = title)
    return fig

def heatmap(epw_df, colors, title, data_min, data_max, z_vals, hover):
    """ General function for a heatmap graph. X axis is hour, Y axis is DOY.

    Args: 
        colors -- List of colors to use
        title -- title for the graph 
        data_min -- int for the min
        data_max -- int for the max
    """
    if hover == '':
        fig = go.Figure(
            data = go.Heatmap(
                y = epw_df["hour"], 
                x = epw_df["DOY"],
                z = z_vals, 
                colorscale = colors,
                zmin = data_min, 
                zmax = data_max,
            )
        )
    else:
        fig = go.Figure(
            data = go.Heatmap(
                y = epw_df["hour"], 
                x = epw_df["DOY"],
                z = z_vals, 
                colorscale = colors,
                zmin = data_min, 
                zmax = data_max,
                hovertemplate = hover)
        )
    fig.update_layout(
        template = template,
        title = title,
        xaxis_nticks = 53,
        yaxis_nticks = 13,
    )
    return fig

def monthly(df, grouped_df, line_color, marker_color, col, xlim, ylim):
    """ General function for the daily graphs.

    Args:
        df -- pandas df
        grouped_df -- pandas df 
        line_color -- string of the line color 
        marker_color -- string of the marker color
        col -- string for the column used (either "RH" or "DBT")
        xlim = list of a range for the x axis
        ylim = list of a range for the y axis 
    """
    month_list = ["Jan","Feb","Mar","Apr","May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    fig = make_subplots(rows = 1, cols = 12, subplot_titles = ("Jan","Feb","Mar","Apr","May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"))

    for i in range(12):
        fig.add_trace(
            go.Scatter(x = df.loc[df["month"] == i + 1, "hour"], y = df.loc[df["month"] == i + 1, col],
                        mode = "markers", marker_color = marker_color,
                        marker_size = 2, name = month_list[i], showlegend = False),
                        row = 1, col = i + 1,
        )
        fig.add_trace(
            go.Scatter(x = grouped_df.loc[grouped_df["month"] == i + 1,"hour"], 
                        y = grouped_df.loc[grouped_df["month"] == i + 1, col],
                        mode = "lines", line_color = line_color, line_width = 3, 
                        name = None, showlegend = False), row = 1, col = i + 1
        )
        fig.update_xaxes(range = xlim, row = 1, col = i + 1)
        fig.update_yaxes(range = ylim, row = 1, col = i + 1)
    
    fig.update_layout(template = template)
    return fig