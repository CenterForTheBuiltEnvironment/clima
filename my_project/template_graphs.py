from plotly.colors import n_colors
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from math import ceil, floor
import pandas as pd
import numpy as np

from .global_scheme import template
from my_project.global_scheme import unit_dict, range_dict, name_dict, color_dict

#######################
### VIOLIN TEMPLATE ###
#######################
def violin(df, var, global_local):
    """ Return day night violin based on the 'var' col
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
        data_max = (5 * ceil(df[var].max() / 5))
        data_min = (5 * floor(df[var].min() / 5))
        range_y = [data_min, data_max]
    colors = n_colors('rgb(0, 200, 200)', 'rgb(200, 10, 10)', 12, colortype = 'rgb')
    data_day = df.loc[mask_day, var]
    data_night = df.loc[mask_night, var]
    fig = go.Figure()
    fig.add_trace(go.Violin(x = df["fake_year"], y = data_day, line_color = 'rgb(200, 10, 10)', name = "Day", side = 'negative'))
    fig.add_trace(go.Violin(x = df["fake_year"], y = data_night, line_color = 'rgb(0, 200, 200)', name = "Night", side = 'positive'))
    fig.update_yaxes(range = range_y)
    fig.update_traces(meanline_visible = True, orientation = 'v', width = 0.8, points = False)
    fig.update_layout(xaxis_showgrid = False, xaxis_zeroline = False, height = 1000, width = 350, violingap = 0, violingroupgap = 0, violinmode = 'overlay')
    title = var_name + " (" + var_unit + ")"
    fig.update_layout(template = template, title = title)
    return fig

###############################
### YEARLY PROFILE TEMPLATE ###
###############################
def yearly_profile(df, var, global_local, lo80, hi80, lo90, hi90):
    """ Return yearly profile figure based on the 'var' col.
    """
    var_unit = unit_dict[str(var) + "_unit"]
    var_range = range_dict[str(var) + "_range"]
    var_name = name_dict[str(var) + "_name"]
    var_color = color_dict[str(var) + "_color"]
    if global_local == "global":
        # Set Global values for Max and minimum
        range_y = var_range
    else:
        # Set maximumand minimum according to data
        data_max = (5 * ceil(df[var].max() / 5))
        data_min = (5 * floor(df[var].min() / 5))
        range_y = [data_min, data_max]
    var_single_color = var_color[len(var_color) // 2]
    custom_xlim = [0, 365]
    custom_ylim = range_y
    days = [i for i in range(365)]
    # Get min, max, and mean of each day
    DBT_day = df.groupby(np.arange(len(df.index)) // 24)[var].agg(['min', 'max', 'mean'])
    ones = [1] * 365
    trace1 = go.Bar(
                x = days, 
                y = DBT_day['max'] - DBT_day['min'],
                base = DBT_day['min'],
                marker_color = var_single_color,
                marker_opacity = 0.3,
                name = var_name +' Range',
                customdata = np.stack((DBT_day['mean'], df.iloc[::24, :]['month_names'], df.iloc[::24, :]['day']), axis = -1),
                hovertemplate = ('Max: %{y:.2f} ' + var_unit + '<br>' +\
                                'Min: %{base:.2f} '+ var_unit + '<br>' +\
                                '<b>Ave : %{customdata[0]:.2f} ' + var_unit + '</b><br>' +\
                                'Month: %{customdata[1]}<br>' +\
                                'Day: %{customdata[2]}<br>'
                                )
            )
    trace2 = go.Scatter(
                x = days, 
                y = DBT_day['mean'], 
                name = 'Average ' + var_name,
                mode = 'lines',
                marker_color = var_single_color,
                marker_opacity = 1,
                customdata = np.stack((DBT_day['mean'], df.iloc[::24, :]['month_names'], df.iloc[::24, :]['day']), axis = -1),
                hovertemplate = ('<b>Ave : %{customdata[0]:.2f} '+var_unit+'</b><br>'+\
                                'Month: %{customdata[1]}<br>'+\
                                'Day: %{customdata[2]}<br>'
                                )
            )
    data = [trace1, trace2]
    if var == "DBT":
        ## plot ashrae adaptive comfort limits (80%)
        lo80_df = pd.DataFrame({"lo80": lo80})
        hi80_df = pd.DataFrame({"hi80": hi80})
        trace3 = go.Bar(
                    x = days, 
                    y = hi80_df["hi80"] - lo80_df["lo80"], 
                    base = lo80_df["lo80"],
                    name = 'ashrae adaptive comfort (80%)',
                    marker_color = "silver",
                    marker_opacity = 0.3,
                    hovertemplate = ('Max: %{y:.2f} &#8451;<br>'+ 'Min: %{base:.2f} &#8451;<br>')
                )
        ## plot ashrae adaptive comfort limits (90%)
        lo90_df = pd.DataFrame({"lo90": lo90})
        hi90_df = pd.DataFrame({"hi90": hi90})
        trace4 = go.Bar(
                    x = days, 
                    y = hi90_df["hi90"] - lo90_df["lo90"],
                    base = lo90_df["lo90"],
                    name='ashrae adaptive comfort (90%)',
                    marker_color = "silver",
                    marker_opacity = 0.3,
                    hovertemplate = ('Max: %{y:.2f} &#8451;<br>' + 'Min: %{base:.2f} &#8451;<br>')
                )
        data = [trace3, trace4, trace1, trace2]
    elif var == "RH":
        ## plot relative Humidity limits (30-70%)
        loRH = [30] * 365
        hiRH = [70] * 365
        loRH_df = pd.DataFrame({"loRH": loRH})
        hiRH_df = pd.DataFrame({"hiRH": hiRH})
        trace3 = go.Bar(
                    x = days, 
                    y = hiRH_df["hiRH"] - loRH_df["loRH"],
                    base = loRH_df["loRH"],
                    name = 'humidity comfort band',
                    marker_opacity = 0.3,
                    marker_color = "silver")
        data = [trace3, trace1, trace2]

    layout = go.Layout(
        barmode = 'overlay',
        bargap = 0
    )
    fig = go.Figure(data = data, layout = layout)
    fig.update_xaxes(range = custom_xlim)
    fig.update_yaxes(range = custom_ylim)
    fig.update_layout(
        legend = dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor = "right",
            x = 1    
        )
    )
    title = "Yearly profile of " + var_name + " (" + var_unit + ")"
    fig.update_yaxes(title_text = var_unit)
    fig.update_xaxes(title_text = "days of the year")
    fig.update_layout(template = template)
    fig.update_layout(title = title)
    return fig 

##############################
### DAILY PROFILE TEMPLATE ###
##############################
def daily_profile(df, var, global_local):
    """ Return the daily profile based on the 'var' col.
    """
    var_unit = unit_dict[str(var) + "_unit"]
    var_range = range_dict[str(var) + "_range"]
    var_name = name_dict[str(var) + "_name"]
    var_color = color_dict[str(var) + "_color"]
    if global_local == "global":
        # Set Global values for Max and minimum
        range_y = var_range
    else:
        # Set maximum and minimum according to data
        data_max = (5 * ceil(df[var].max() / 5))
        data_min = (5 * floor(df[var].min() / 5))
        range_y = [data_min, data_max]
    var_single_color = var_color[len(var_color) // 2]
    var_month_ave = df.groupby(['month','hour'])[var].median().reset_index()
    monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    fig = make_subplots(rows = 1, cols = 12, subplot_titles = ("Jan","Feb","Mar","Apr","May", "Jun", "Jul" ,"Aug", "Sep", "Oct", "Nov", "Dec"))
    for i in range(12):
        fig.add_trace(
            go.Scatter(
                x = df.loc[df["month"] == i + 1, "hour"],
                y = df.loc[df["month"] == i + 1, var],
                mode = "markers",
                marker_color = var_single_color,
                opacity = 0.5,
                marker_size = 3,
                name = monthList[i],
                showlegend = False,
                hovertemplate = ('<b>' + var + ': %{y:.2f} ' + var_unit + '</b><br>' + 'Hour: %{x}:00<br>')
            ),
            row = 1, 
            col = i + 1,
        )
        fig.add_trace(
            go.Scatter(
                x = var_month_ave.loc[var_month_ave["month"] == i + 1, "hour"], 
                y = var_month_ave.loc[var_month_ave["month"] == i + 1, var],
                mode = "lines",
                line_color = var_single_color, 
                line_width = 3,
                name = None, 
                showlegend = False,
                hovertemplate = ('<b>' + var + ': %{y:.2f} ' + var_unit + '</b><br>' + 'Hour: %{x}:00<br>')
            ),
            row = 1, 
            col = i + 1
        )
        fig.update_xaxes(range = [0, 25], row = 1, col = i + 1)
        fig.update_yaxes( range = range_y, row = 1, col = i + 1)
    title = var_name + " (" + var_unit + ")"
    fig.update_layout(template = template, title = title)
    return fig 

########################
### HEATMAP TEMPLATE ###
########################
def heatmap(df, var, global_local):
    """ General function that returns a heatmap.
    """
    var_unit = unit_dict[str(var) + "_unit"]
    var_range = range_dict[str(var) + "_range"]
    var_name = name_dict[str(var) + "_name"]
    var_color = color_dict[str(var) + "_color"]
    if global_local == "global":
        # Set Global values for Max and minimum
        range_z = var_range
    else:
        # Set maximum and minimum according to data
        data_max = (5 * ceil(df[var].max() / 5))
        data_min = (5 * floor(df[var].min() / 5))
        range_z = [data_min, data_max]
    fig = go.Figure(
            data = go.Heatmap(
                        y = df["hour"],
                        x = df["DOY"],
                        z = df[var],
                        colorscale = var_color,
                        zmin = range_z[0], 
                        zmax = range_z[1],
                        customdata = np.stack((df["month_names"], df["day"]), axis = -1),
                        hovertemplate = ('<b>'+ var+': %{z:.2f} '+ var_unit +'</b><br>'+\
                                            'Month: %{customdata[01]}<br>'+\
                                            'Day: %{customdata[1]}<br>'+\
                                            'Hour: %{y}:00<br>'),
                        colorbar = dict(title = var_unit)
                    )
        )
    title = var_name + " (" + var_unit + ")"                 
    fig.update_layout(
        template = template,
        title = title,
        xaxis_nticks = 53,
        yaxis_nticks = 13,
    )
    fig.update_yaxes(title_text = "hours of the day")
    fig.update_xaxes(title_text = "days of the year")
    return fig