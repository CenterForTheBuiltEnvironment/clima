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

def calculate_ashrae(epw_df):
    """ Helper function used in the montly_dbt(). 
    """
    DBT_day_ave = epw_df.groupby(['DOY'])['DBT'].mean().reset_index()
    DBT_day_ave = DBT_day_ave['DBT'].tolist()
    n = 7  #number of days for running average
    cmf55 = []
    hi80 = []
    lo80 = []
    hi90 = []
    lo90 = []
    fail = 0
    for i in range(len(DBT_day_ave)):
        if i < n:
            lastDays = DBT_day_ave[-n + i:] + DBT_day_ave[0:i]
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


#########################
### DAILY FUNCTIONS ###
#########################
def daily(epw_df, x, col, marker_colors, names, xlim, ylim, lo, hi):
    """ General function for a monthly graph.

    Args:
        x -- list of the x values 
        col -- string (either "RH" or "DBT")
        marker_colors -- list of marker colors for each trace 
        names -- list of names for each trace
        xlim -- tuple of the x axes limits
        ylim -- tuple of the y axes limits
        lo -- list of values 
        hi -- list of values 
    """
    marker_color_one = marker_colors[0]
    marker_color_two = marker_colors[1]
    marker_color_three = marker_colors[2]

    name_one = names[0]
    name_two = names[1]
    name_three = names[2]

    # Get min, max, and mean of each day
    day_df = epw_df.groupby(np.arange(len(epw_df.index)) // 24)[col].agg(['min', 'max', 'mean'])

    ones = [1] * 365

    trace1 = go.Bar(x = x, y = day_df['max'] - day_df['min'],
                    base = day_df['min'],
                    marker_color = marker_color_one,
                    name = name_one,
                    customdata = np.stack((day_df['mean'], epw_df.iloc[::24, :]['month_names'], epw_df.iloc[::24, :]['day']), axis =- 1),
                    hovertemplate = ('Max: %{y:.2f} &#8451;<br>'+\
                                'Min: %{base:.2f} &#8451;<br>'+\
                                '<b>Mean : %{customdata[0]:.2f} &#8451;</b><br>'+\
                                'Month: %{customdata[1]}<br>'+\
                                'Day: %{customdata[2]}<br>'))

    trace2 = go.Bar(x = x, y = ones, base = day_df['mean'], 
                    name = name_two,
                    marker_color = marker_color_two,
                    customdata = np.stack((day_df['mean'], epw_df.iloc[::24, :]['month_names'], epw_df.iloc[::24, :]['day']), axis =- 1),
                    hovertemplate = ('<b>Mean : %{customdata[0]:.2f} &#8451;</b><br>'+\
                                'Month: %{customdata[1]}<br>'+\
                                'Day: %{customdata[2]}<br>'))

    lo_df = pd.DataFrame({"lo": lo})
    hi_df = pd.DataFrame({"hi": hi})

    ## plot ashrae adaptive comfort limits (80%)
    trace3 = go.Bar(x = x, y = hi_df["hi"] - lo_df["lo"], 
                    base = lo_df["lo"],
                    name = name_three,
                    marker_color = marker_color_three,
                    hovertemplate = ('Max: %{y:.2f} &#8451;<br>'+\
                    'Min: %{base:.2f} &#8451;<br>'))

    # ## plot ashrae adaptive comfort limits (90%)
    # lo90_df = pd.DataFrame({"lo90": lo90})
    # hi90_df = pd.DataFrame({"hi90": hi90})

    # trace4=go.Bar(x = days, y = hi90_df["hi90"] - lo90_df["lo90"], base = lo90_df["lo90"],
    #             name = name_four,
    #             marker_color = "silver",
    #             hovertemplate = ('Max: %{y:.2f} &#8451;<br>'+\
    #                                 'Min: %{base:.2f} &#8451;<br>')
    #             )

    data = [trace3, trace1, trace2]
    layout = go.Layout(
        barmode = 'overlay',
        bargap = 0
    )
    fig = go.Figure(data = data, layout = layout)
    fig.update_traces(opacity = 0.6)
    fig.update_layout(legend = dict(
        orientation = "h",
        yanchor = "bottom",
        y = 1.02,
        xanchor = "right",
        x = 1    
    ))
    fig.update_layout(template = template)
    return fig

def daily_dbt(epw_df, meta):
    """ Returns the graph for the monthly dbt.
    """
    # x = [i for i in range(365)]
    # col = "DBT"
    # marker_colors = ['orange', 'red', "silver"]
    # names = ['Temperature Range', 'Average Temperature', 'Ashrae Adaptive Comfort (80%)']
    # xlim = (0, 365)
    # ylim = (-40, 50)
    # lo, hi = calculate_ashrae(epw_df)
    # return daily(epw_df, x, col, marker_colors, names, xlim, ylim, lo, hi)
    days = [i for i in range(365)]
    DBT_day = epw_df.groupby(np.arange(len(epw_df.index)) // 24)["DBT"].agg(['min', 'max', 'mean'])
    ones = [1]*365
    trace1 = go.Bar(x = days, y = DBT_day['max'] - DBT_day['min'],
                    base = DBT_day['min'],
                    marker_color = 'orange',
                    name = 'Temperature Range',
                    customdata = np.stack((DBT_day['mean'], epw_df.iloc[::24, :]['month_names'], epw_df.iloc[::24, :]['day']), axis = -1),
                    hovertemplate = ('Max: %{y:.2f} &#8451;<br>'+\
                                    'Min: %{base:.2f} &#8451;<br>'+\
                                    '<b>Ave : %{customdata[0]:.2f} &#8451;</b><br>'+\
                                    'Month: %{customdata[1]}<br>'+\
                                    'Day: %{customdata[2]}<br>')
                )
    trace2 = go.Bar(x = days, y = ones, base = DBT_day['mean'], 
                name = 'Average Temperature',
                marker_color = 'red',
                customdata = np.stack((DBT_day['mean'], epw_df.iloc[::24, :]['month_names'], epw_df.iloc[::24, :]['day']), axis = -1),
                hovertemplate = ('<b>Ave : %{customdata[0]:.2f} &#8451;</b><br>'+\
                                    'Month: %{customdata[1]}<br>'+\
                                    'Day: %{customdata[2]}<br>')
                    )
    ## plot ashrae adaptive comfort limits (80%)
    lo80, hi80, lo90, hi90 = calculate_ashrae(epw_df)
    lo80_df = pd.DataFrame({"lo80": lo80})
    hi80_df = pd.DataFrame({"hi80": hi80})
    trace3 = go.Bar(x = days, y = hi80_df["hi80"] - lo80_df["lo80"], base = lo80_df["lo80"],
                name = 'ashrae adaptive comfort (80%)',
                marker_color = "silver",
                hovertemplate = ('Max: %{y:.2f} &#8451;<br>'+\
                                    'Min: %{base:.2f} &#8451;<br>')
                )
    ## plot ashrae adaptive comfort limits (90%)
    lo90_df = pd.DataFrame({"lo90": lo90})
    hi90_df = pd.DataFrame({"hi90": hi90})
    trace4 = go.Bar(x = days, y = hi90_df["hi90"] - lo90_df["lo90"], base = lo90_df["lo90"],
                name = 'ashrae adaptive comfort (90%)',
                marker_color = "silver",
                hovertemplate = ('Max: %{y:.2f} &#8451;<br>'+\
                                    'Min: %{base:.2f} &#8451;<br>')
                )
    data = [trace3, trace4, trace1, trace2]
    layout = go.Layout(
        barmode = 'overlay',
        bargap = 0
    )
    fig = go.Figure(data = data, layout = layout)
    fig.update_xaxes(range = [0, 365])
    # fig.update_yaxes(range = [-40, 50])
    fig.update_traces(opacity = 0.6)
    fig.update_layout(legend = dict(
        orientation = "h",
        yanchor = "bottom",
        y = 1.02,
        xanchor = "right",
        x = 1    
    ))
    fig.update_layout(template = template)
    return fig

def daily_humidity(epw_df, meta):
    """ Returns the graph for the monthly humidity 
    """
    x = [i for i in range(365)]
    col = "RH"
    marker_colors = ['dodgerblue', 'blue', "silver"]
    names = ['Relative Humidity Range', 'Average Relative Humidity', 'Humidity Comfort Band']
    xlim = (0, 365)
    ylim = (0, 100)
    lo = [30] * 365
    hi = [70] * 365
    return daily(epw_df, x, col, marker_colors, names, xlim, ylim, lo, hi)

#########################
### MONTHLY FUNCTIONS ###
#########################

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
        # fig.update_xaxes(range = xlim, row = 1, col = i + 1)
        # fig.update_yaxes(range = ylim, row = 1, col = i + 1)
    
    fig.update_layout(template = template)
    return fig

def monthly_dbt3(epw_df, meta):
    """ Return the daily graph for the DBT
    """
    df = epw_df[['month', 'day', 'hour', 'DBT']]
    grouped_df = df.groupby(['month','hour'])['DBT'].median().reset_index()
    line_color = "red"
    marker_color = "orange"
    col = "DBT"
    xlim = [0, 25]
    ylim = [-50, 50]
    return monthly(df, grouped_df, line_color, marker_color, col, xlim, ylim)

def monthly_humidity(epw_df, meta):
    """ Return the daily graph for humidity.
    """
    df = epw_df[['month', 'day', 'hour', 'RH']]
    grouped_df = df.groupby(['month','hour'])['RH'].median().reset_index()
    line_color = "dodgerblue"
    marker_color = "skyblue"
    col = "RH"
    xlim = [0, 25]
    ylim = [0, 100]
    return monthly(df, grouped_df, line_color, marker_color, col, xlim, ylim)

#########################
### HEATMAP FUNCTIONS ### 
#########################

def heatmap(epw_df, colors, title, data_min, data_max, z_vals):
    """ General function for a heatmap graph. X axis is hour, Y axis is DOY.

    Args: 
        colors -- List of colors to use
        title -- title for the graph 
        data_min -- int for the min
        data_max -- int for the max
    """

    fig = go.Figure(data = go.Heatmap(y = epw_df["hour"], x = epw_df["DOY"],
                    z = z_vals, colorscale = colors,
                    zmin = data_min, zmax = data_max,
                    hovertemplate = 'DOY: %{x}<br>hour: %{y}<br>RH: %{z}<extra></extra>'))
    fig.update_layout(
        template = template,
        title = title,
        xaxis_nticks = 53,
        yaxis_nticks = 13,
    )
    return fig

def heatmap_dbt(epw_df, meta):
    """ Return a figure of the heatmap for DBT
    """
    colors = ["#00b3ff","#000082","#ff0000","#ffff00"]
    title = "Dry Bulb Temperatures (degC)"
    data_max = (5 * math.ceil(epw_df["DBT"].max() / 5))
    data_min = (5 * math.floor(epw_df["DBT"].min() / 5))
    z_vals = epw_df["DBT"]
    return heatmap(epw_df, colors, title, data_min, data_max, z_vals)

def heatmap_humidity(epw_df, meta):
    """ Return a figure of the heatmap for humidity. 
    """
    colors = ["#ffe600", "#00c8ff", "#0000ff"]
    title = "Relative Humiditys (degC)"
    data_max = 100
    data_min = 0
    z_vals = epw_df["RH"]
    return heatmap(epw_df, colors, title, data_min, data_max, z_vals)
