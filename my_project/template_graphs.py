from plotly.colors import n_colors
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .global_scheme import template

def create_violin(df, col, title, y_title, y_lim):
    """ General function to create a day/night violin plot. 
    """
    fig = go.Figure()
    maskDay = (df["hour"] >= 8) & (df["hour"] < 20)
    maskNight = (df["hour"] < 8) | (df["hour"] >= 20)
    data_day = df.loc[maskDay, col]
    data_night = df.loc[maskNight, col]
    fig.add_trace(go.Violin(x = df["fake_year"], y = data_day, line_color = 'rgb(200, 10, 10)', 
        name = "Day", side = 'negative'))
    fig.add_trace(go.Violin(x = df["fake_year"], y = data_night, line_color = 'rgb(0, 200, 200)', 
        name = "Night", side = 'positive'))
    fig.update_yaxes(range = y_lim)
    fig.update_traces(meanline_visible = True, orientation = 'v', width = 0.8, points = False)
    fig.update_layout(xaxis_showgrid = False, xaxis_zeroline = False, height = 1000, width = 350, 
        violingap = 0, violingroupgap = 0, violinmode = 'overlay', title = title, yaxis_title = y_title, template = template)
    return fig

def heatmap(epw_df, colors, title, data_min, data_max, z_vals, hover):
    """ General function for a heatmap graph. X axis is hour, Y axis is DOY.

    Args: 
        colors -- List of colors to use
        title -- title for the graph 
        data_min -- int for the min
        data_max -- int for the max
    """
    fig = go.Figure(
        data = go.Heatmap(
            y = epw_df["hour"], 
            x = epw_df["DOY"],
            z = z_vals, colorscale = colors,
            zmin = data_min, 
            zmax = data_max,
            hovertemplate = hover))
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