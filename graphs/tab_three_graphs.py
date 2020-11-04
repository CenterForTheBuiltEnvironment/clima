import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from pythermalcomfort.models import adaptive_ashrae
from pythermalcomfort.psychrometrics import running_mean_outdoor_temperature
from pprint import pprint

from extract_df import create_df

default_url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw"
epw_df, location_name = create_df(default_url)

# Color scheme 
BlueRedYellow = ["#00b3ff", "#000082", "#ff0000", "#ffff00"]
DBT_color = BlueRedYellow
template = "ggplot2"

def daily_dbt():
    DBT_df = epw_df[['month', 'day', 'hour', 'DBT']]

    DBT_month_ave = DBT_df.groupby(['month','hour'])['DBT'].median().reset_index()
    monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    fig = make_subplots(rows = 1, cols = 12, subplot_titles = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"))

    for i in range(12):
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

    val_day=pd.DataFrame(
        {"Max":val_day_max,
        "Min":val_day_min,
        "Ave":val_day_ave}
    )
    return(val_day)


def version03():
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


DBT_day_ave=epw_df.groupby(['DOY'])['DBT'].mean().reset_index()
DBT_day_ave=DBT_day_ave['DBT'].tolist()
#pprint(len(DBT_day_ave))

n=7  #number of days for running average

hi80=[]
lo80=[]

fail=0

for i in range(len(DBT_day_ave)):
  if i<n:
    lastDays=DBT_day_ave[-n+i:]+DBT_day_ave[0:i]
  else:
    lastDays=DBT_day_ave[i-n:i]
  

  #pprint (lastDays)

  lastDays.reverse()
  lastDays=[10 if x <= 10 else x for x in lastDays]
  lastDays=[32 if x >= 32 else x for x in lastDays]

  #print (i)
  #print (lastDays)
  #print (DBT2[i])
  
  #try:
  rmt=running_mean_outdoor_temperature(lastDays, alpha=0.8)
  #print(rmt)
  
  #for interior spaces: MRT = DBT and wind speed (for interior) constant at 0.5 m/s
  if DBT_day_ave[i]>=40: 
    DBT_day_ave[i]=40
  elif DBT_day_ave[i]<=10: 
    DBT_day_ave[i]=10
  #print(rmt)
  r=adaptive_ashrae(tdb=DBT_day_ave[i], tr=DBT_day_ave[i],t_running_mean=rmt,v=0.5)

  lo80.append(r['tmp_cmf_80_low'])
  hi80.append(r['tmp_cmf_80_up'])

  


