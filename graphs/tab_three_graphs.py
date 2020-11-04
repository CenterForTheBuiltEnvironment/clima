import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pythermalcomfort.models import adaptive_ashrae
from pythermalcomfort.psychrometrics import running_mean_outdoor_temperature
from pprint import pprint
from extract_df import create_df
import math

default_url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw"
epw_df, location_name = create_df(default_url)

# Color scheme 
BlueRedYellow = ["#00b3ff", "#000082", "#ff0000", "#ffff00"]
DBT_color = BlueRedYellow
template = "ggplot2"


#### TEMPERATURE ###

def daily_dbt():
    DBT_df = epw_df[['month', 'day', 'hour', 'DBT']]

    DBT_month_ave = DBT_df.groupby(['month','hour'])['DBT'].median().reset_index()
    monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    fig = make_subplots(rows = 1, cols = 12, subplot_titles = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"))

    for i in range(12):
        # add for loop here and change mode from marker to lines have each line for like each day or something 
        fig.add_trace(
            go.Scatter(x = DBT_df.loc[DBT_df["month"] == i + 1, "hour"], y = DBT_df.loc[DBT_df["month"] == i + 1, "DBT"],
                        mode = "markers", marker_color = "orange",
                        marker_size = 2, name = monthList[i], showlegend = False),
                        row = 1, col = i + 1,
            )
        fig.add_trace(
            go.Scatter(x = DBT_month_ave.loc[DBT_month_ave["month"] == i + 1, "hour"], y = DBT_month_ave.loc[DBT_month_ave["month"] == i + 1, "DBT"],
                        mode = "lines", line_color = "red", line_width = 3, name = None, showlegend = False),
                        row = 1, col = i + 1,
        )
        fig.update_xaxes(range = [0, 25], row = 1, col = i + 1)
        fig.update_yaxes(range = [-50, 50], row = 1, col = i + 1)
    return fig

def average_MaxMin(val):
    val_days = [val[x:x+24] for x in range(0, len(val), 24)]

    val_day_max=[]
    val_day_min=[]
    val_day_ave=[]
    for i in range(len(val_days)):
        val_day_max.append(max(val_days[i]))
        val_day_min.append(min(val_days[i]))
        val_day_ave.append(sum(val_days[i])/len(val_days[i]))

    val_day = pd.DataFrame(
        {"Max": val_day_max,
        "Min": val_day_min,
        "Ave": val_day_ave}
    )
    return val_day


def version03():

    lo80, hi80 = calculate_ashrae()

    custom_xlim = [0, 365]
    custom_ylim = [-40, 50]

    days = []

    for i in range(365):
        days.append(i)

    DBT_day = average_MaxMin(epw_df['DBT'])

    ones = [1] * 365

    trace1 = go.Bar(x = days, y = DBT_day['Max'] - DBT_day['Min'],
                    base = DBT_day['Min'],
                    marker_color = 'orange',
                    name = 'Temperature Range'
                )

    trace2 = go.Bar(x = days, y = ones, base = DBT_day['Ave'], 
                        name = 'Average Temperature',
                        marker_color = 'red',
                        )


    ## plot ashrae adaptive comfort limits (80%)
    lo80_df = pd.DataFrame({"lo80": lo80})
    hi80_df = pd.DataFrame({"hi80": hi80})


    trace3 = go.Bar(x = days, y = hi80_df["hi80"] - lo80_df["lo80"], base = lo80_df["lo80"],
                name = 'ashrae adaptive comfort (80%)',
                marker_color = "silver")
    data = [trace3, trace1,trace2]

    layout = go.Layout(
        barmode = 'overlay',
        bargap = 0
    )

    fig = go.Figure(data = data, layout = layout)
 
    fig.update_xaxes(range = custom_xlim)
    fig.update_yaxes(range = custom_ylim)

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


def calculate_ashrae():

    DBT_day_ave = epw_df.groupby(['DOY'])['DBT'].mean().reset_index()
    DBT_day_ave = DBT_day_ave['DBT'].tolist()

    n = 7  # number of days for running average
    hi80 = []
    lo80 = []
    fail = 0
    for i in range(len(DBT_day_ave)):
        if i < n:
            lastDays = DBT_day_ave[-n + i:] + DBT_day_ave[0:i]
        else:
            lastDays = DBT_day_ave[i - n:i]

        lastDays.reverse()
        lastDays = [10 if x <= 10 else x for x in lastDays]
        lastDays = [32 if x >= 32 else x for x in lastDays]
        rmt = running_mean_outdoor_temperature(lastDays, alpha = 0.8)

        if DBT_day_ave[i] >= 40: 
            DBT_day_ave[i] = 40
        elif DBT_day_ave[i] <= 10: 
            DBT_day_ave[i] = 10
        r = adaptive_ashrae(tdb = DBT_day_ave[i], tr = DBT_day_ave[i], t_running_mean = rmt, v = 0.5)

        lo80.append(r['tmp_cmf_80_low'])
        hi80.append(r['tmp_cmf_80_up'])

    return lo80, hi80

def heatmap_dbt():
    BlueRedYellow = ["#00b3ff","#000082","#ff0000","#ffff00"]
    DBT_color = BlueRedYellow
    Title = "Dry Bulb Temperatures (degC)"

    # Set maximum and minimum according to data
    dataMax = (5 * math.ceil(epw_df["DBT"].max() / 5))
    dataMin = (5 * math.floor(epw_df["DBT"].min() / 5))

    fig = go.Figure(data=go.Heatmap(y = epw_df["hour"], x = epw_df["DOY"],
                                    z = epw_df["DBT"], colorscale = DBT_color,
                                    zmin = dataMin, zmax = dataMax,
                                    hovertemplate = 'DOY: %{x}<br>hour: %{y}<br>Temp: %{z}<extra></extra>'))
    fig.update_layout(
        template = template,
        title = Title,
        xaxis_nticks = 53,
        yaxis_nticks = 13,
    )
    return fig



### HUMIDITY ###

def humidity():
    days = []
    custom_xlim = (0,365)
    custom_ylim = (-40, 50)

    for i in range(365):
        days.append(i)

    RH_day = average_MaxMin(epw_df['RH'])

    ones = [1] * 365

    trace1 = go.Bar(x = days, y = RH_day['Max'] - RH_day['Min'],
                    base = RH_day['Min'],
                    marker_color = 'dodgerblue',
                    name = 'Relative Humidity Range')
    "#00c8ff",
    trace2 = go.Bar(x = days, y = ones, base = RH_day['Ave'], 
                    name = 'Average Relative Humidity',
                    marker_color = 'blue')


    ## plot relative Humidity limits (30-70%)
    loRH = [30] * 365
    hiRH = [70] * 365
    loRH_df = pd.DataFrame({"loRH": loRH})
    hiRH_df = pd.DataFrame({"hiRH": hiRH})


    trace3 = go.Bar(x = days, y = hiRH_df["hiRH"] - loRH_df["loRH"], base = loRH_df["loRH"],
                name = 'humidity comfort band',
                marker_color = "silver")

    data = [trace3, trace1,trace2]

    layout = go.Layout(
        barmode = 'overlay',
        bargap = 0
    )

    fig = go.Figure(data = data, layout = layout)

    fig.update_xaxes(range = custom_xlim)
    fig.update_yaxes(range = (0, 100))

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

def daily_humidity():
    RH_df = epw_df[['month', 'day', 'hour', 'RH']]

    RH_month_ave = RH_df.groupby(['month','hour'])['RH'].median().reset_index()
    monthList = ["Jan","Feb","Mar","Apr","May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    fig = make_subplots(rows = 1, cols = 12, subplot_titles = ("Jan","Feb","Mar","Apr","May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"))

    for i in range(12):
        fig.add_trace(
            go.Scatter(x = RH_df.loc[RH_df["month"] == i + 1, "hour"], y = RH_df.loc[RH_df["month"] == i + 1, "RH"],
                        mode = "markers", marker_color = "skyblue",
                        marker_size = 2, name = monthList[i], showlegend = False),
                        row = 1, col = i + 1,
        )
        fig.add_trace(
            go.Scatter(x=RH_month_ave.loc[RH_month_ave["month"]==i+1,"hour"],y=RH_month_ave.loc[RH_month_ave["month"]==i+1,"RH"],
                        mode="lines",line_color="dodgerblue",line_width=3,name=None,showlegend=False),
            row=1, col=i+1,
        )
        fig.update_xaxes(range = [0, 25], row = 1, col = i + 1)
        fig.update_yaxes(range=[0, 100], row = 1, col = i + 1)
    

    fig.update_layout(template=template)

    return fig

def heatmap_humidity():
    DryHumid = ["#ffe600", "#00c8ff", "#0000ff"]
    RH_color = DryHumid
    #RH_heat=heatmap(epw_df,"RH")
    Title = "Relative Humiditys (degC)"

    ##Set maximumand minimum according to data
    """dataMax=(5*math.ceil(epw_df["RH"].max()/5))
    dataMin=(5*math.floor(epw_df["RH"].min()/5))
    print(dataMax)
    print(dataMin)"""

    ##Set Global avlues for Max and minimum
    dataMax = 100
    dataMin = 0

    fig = go.Figure(data=go.Heatmap(y = epw_df["hour"], x = epw_df["DOY"],
                                    z = epw_df["RH"], colorscale = RH_color,
                                    zmin = dataMin, zmax = dataMax,
                                    hovertemplate = 'DOY: %{x}<br>hour: %{y}<br>RH: %{z}<extra></extra>'))
    fig.update_layout(
        template = template,
        title = Title,
        xaxis_nticks = 53,
        yaxis_nticks = 13,
    )

    return fig

