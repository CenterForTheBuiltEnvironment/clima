import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.express as px

from my_project.global_scheme import template, color_dict, range_dict
from my_project.template_graphs import heatmap


#################
### WIND ROSE ###
#################

def speed_labels(bins, units):  
    """ Return nice labels for a wind speed range.
    """ 
    labels = []
    for left, right in zip(bins[:-1], bins[1:]):
        if left == bins[0]:
            labels.append('calm')
        elif np.isinf(right):
            labels.append('>{} {}'.format(left, units))
        else:
            labels.append('{} - {} {}'.format(left, right, units))
    return labels

def wind_rose(df, meta, units, month, hour):
    """ Return the wind rose figure.

    Based on:  https://gist.github.com/phobson/41b41bdd157a2bcf6e14
    """
    start_month = month[0]
    end_month = month[1]
    start_hour = hour[0]
    end_hour = hour[1]
    spd_colors = color_dict['Wspeed_color']
    spd_bins = [-1, 0.5, 1.5, 3.3, 5.5, 7.9, 10.7, 13.8, 17.1, 20.7, np.inf]
    spd_labels = speed_labels(spd_bins, units = 'm/s')
    dir_bins = np.arange(-22.5 / 2, 370, 22.5)
    dir_labels = (dir_bins[:-1] + dir_bins[1:]) / 2
    df = df.loc[(df['month'] >= start_month) & (df['month'] <= end_month)]
    df = df.loc[(df['hour'] >= start_hour) & (df['hour'] <= end_hour)]
    total_count = df.shape[0]
    calm_count = df.query("Wspeed == 0").shape[0]
    rose = (
        df.assign(
            WindSpd_bins = lambda df:
                pd.cut(df['Wspeed'], bins = spd_bins, labels = spd_labels, right = True)
            )
            .assign(WindDir_bins = lambda df:
                pd.cut(df['Wdir'], bins = dir_bins, labels = dir_labels, right = False)
            )
            .replace({'WindDir_bins': {360: 0}})
            .groupby(by = ['WindSpd_bins', 'WindDir_bins'])
            .size()
            .unstack(level = 'WindSpd_bins')
            .fillna(0)
            .assign(calm = lambda df: calm_count / df.shape[0])
            .sort_index(axis = 1)
            .applymap(lambda x: x / total_count * 100)
    )
    fig = go.Figure()
    for i, col in enumerate(rose.columns):
        fig.add_trace(
            go.Barpolar(
                r = rose[col], 
                theta = 360 - rose.index.categories,
                name = col, 
                marker_color = spd_colors[i]
            )
        )
    fig.update_traces(
        text = [
            'North', 
            'N-N-E',
            'N-E',
            'E-N-E', 
            'East',
            'E-S-E', 
            'S-E',
            'S-S-E', 
            'South',
            'S-S-W',
            'S-W',
            'W-S-W', 
            'West',
            'W-N-W', 
            'N-W',
            'N-N-W'
        ]
    )
    fig.update_layout(
        polar_angularaxis_rotation = 90,
    )
    fig.update_layout(
        autosize = False,
        width = 1200,
        height = 800,
    )
    return fig
        

################
### HEAT MAP ###
################
def wind_speed_heatmap(df, global_local):
    return heatmap(df, 'Wspeed', global_local)

def wind_direction_heatmap(df, global_local):
    return heatmap(df, 'Wdir', global_local)