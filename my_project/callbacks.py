import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from .server import app 
from .extract_df import create_df
from .template_graphs import violin, wind_rose, heatmap, daily_profile, heatmap, yearly_profile

from .tab_one.tab_one import tab_one
from .tab_two.tab_two import tab_two
from .tab_three.tab_three import tab_three
from .tab_four.tab_four import tab_four
from .tab_five.tab_five import tab_five
from .tab_six.tab_six import tab_six
from .tab_eight.tab_eight import tab_eight

from .tab_two.tab_two_graphs import world_map
from .tab_four.tab_four_graphs import polar_solar, lat_long_solar, monthly_solar, custom_sunpath, yearly_solar_radiation
from .tab_six.tab_six_graphs import custom_heatmap, custom_summary, three_var_graph, two_var_graph

month_lst = ["Jan","Feb","Mar","Apr","May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

#####################
### TAB SELECTION ###        
#####################
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):
    """ Update the contents of the page depending on what tab the user selects.
    """
    if tab == 'tab-1':
        return tab_one()
    elif tab == 'tab-2':
        return tab_two()
    elif tab == 'tab-3':
        return tab_three()
    elif tab == 'tab-4':
        return tab_four()
    elif tab == 'tab-5':
        return tab_five()
    elif tab == 'tab-6':
        return tab_six()
    elif tab == 'tab-7':
        return html.Div(
            children = [
                html.H3('Tab content 7')
            ]
        )
    elif tab == 'tab-8':
        return tab_eight()

#######################
### TAB ONE: SELECT ###        
#######################
@app.callback(
    Output('df-store', 'data'),
    Output('meta-store', 'data'),
    [Input('submit-button', 'n_clicks')],
    [State('input-url', 'value')]
)
def submit_button(n_clicks, value):
    """ Takes the input once submitted and stores it.
    """
    try:
        if n_clicks is None:
            raise PreventUpdate
        df, meta = create_df(value)
        df = df.to_json(date_format = 'iso', orient = 'split')
        return df, meta
    except:
        return None, None

@app.callback(
    Output("alert", 'is_open'),
    Output("alert", 'children'),
    Output("alert", "color"),
    Output("banner-subtitle", "children"),
    [Input('df-store', 'data')],
    [Input('submit-button', 'n_clicks')],
    [State('meta-store', 'data')]
)
def alert_display(data, n_clicks, meta):
    """ Displays the alert for the submit button. 
    """
    default = "Current Location: N/A"
    if n_clicks is None:
        return True, "To start, submit a link below!", "primary", default
    if data is None and n_clicks > 0:
        return True, "This link is not available. Please choose another one.", "warning", default
    else:
        subtitle = "Current Location: " + meta[1] + ", " + meta[3]
        return True, "Successfully loaded data. Check out the other tabs!", "success", subtitle


########################
### TAB TWO: CLIMATE ###        
########################
@app.callback(
    Output('world-map', 'figure'),
    Output('temp-profile-graph', 'figure'),
    Output('humidity-profile-graph', 'figure'),
    Output('solar-radiation-graph', 'figure'),
    Output('wind-speed-graph', 'figure'),
    Output('tab-two-location', 'children'),
    Output('tab-two-long', 'children'),
    Output('tab-two-lat', 'children'),
    Output('tab-two-elevation', 'children'),
    [Input('df-store', 'modified_timestamp')],
    [Input('global-local-radio-input', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_two(ts, global_local, df, meta):
    """ Update the contents of tab two. Passing in the general info (df, meta).
    """
    df = pd.read_json(df, orient = 'split')
    location = "Location: " + meta[1] + " , " + meta[3]
    lon = "Longitude: " + str(meta[-3])
    lat = "Longitude: " + str(meta[-3])
    elevation = "Elevation above sea level: " + meta[-1]

    # Violin Graphs 
    dbt = violin(df, "DBT", global_local)
    rh = violin(df, "RH", global_local)
    ghrad = violin(df, "GHrad", global_local)
    wspeed = violin(df, "Wspeed", global_local)

    return world_map(df, meta), dbt, rh, ghrad, wspeed, location, lon, lat, elevation

####################################
### TAB THREE: TEMP AND HUMIDITY ###
####################################
@app.callback(
    Output('yearly-dbt', 'figure'),
    Output('daily-dbt', 'figure'),
    Output('heatmap-dbt', 'figure'),
    Output('yearly-rh', 'figure'),
    Output('daily-rh', 'figure'),
    Output('heatmap-rh', 'figure'),
    [Input('df-store', 'modified_timestamp')],
    [Input('global-local-radio-input', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_three(ts, global_local, df, meta):
    """ Update the contents of tab three. Passing in general info (df, meta).
    """
    df = pd.read_json(df, orient = 'split')

    # Yearly Graphs 
    dbt_yearly = yearly_profile(df, "DBT", global_local)
    rh_yearly = yearly_profile(df, "RH", global_local)

    # Daily Profile Graphs
    dbt_daily = daily_profile(df, "DBT", global_local)
    rh_daily = daily_profile(df, "RH", global_local)

    # Heatmap Graphs 
    dbt_heatmap = heatmap(df, "DBT", global_local)
    rh_heatmap = heatmap(df, "RH", global_local)
    
    return dbt_yearly, dbt_daily, dbt_heatmap, rh_yearly, rh_daily, rh_heatmap

#####################
### TAB FOUR: SUN ###
#####################
@app.callback(
    Output('solar-dropdown-output', 'figure'),
    Output('monthly-solar', 'figure'),
    Output('yearly-solar', 'figure'),
    Output('custom-sunpath', 'figure'),
    Output('daily-ghrad', 'figure'),
    Output('heatmap-ghrad', 'figure'),
    Output('daily-dnrad', 'figure'),
    Output('heatmap-dnrad', 'figure'),
    Output('daily-difhrad', 'figure'),
    Output('heatmap-difhrad', 'figure'),
    [Input("solar-dropdown", 'value')],
    [Input('df-store', 'modified_timestamp')],
    [Input('global-local-radio-input', 'value')],
    [Input('custom-sun-var-dropdown', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_four(solar_dropdown, ts, global_local, custom_sun_var, df, meta):
    """ Update the contents of tab four. Passing in the polar selection and the general info (df, meta).
    """
    df = pd.read_json(df, orient = 'split')

    # Heatmap Graphs
    ghrad_heatmap = heatmap(df, "GHrad", global_local)
    dnrad_heatmap = heatmap(df, "DNrad", global_local)
    difhrad_heatmap = heatmap(df, "DifHrad", global_local)

    # Daily Profiler Graphs 
    ghrad_daily = daily_profile(df, "GHrad", global_local)
    dnrad_profile = daily_profile(df, "DNrad", global_local)
    difhrad_profile = daily_profile(df, "DifHrad", global_local)

    if solar_dropdown == 'polar':
        return polar_solar(df, meta), monthly_solar(df, meta), yearly_solar_radiation(df), custom_sunpath(df, meta, global_local, custom_sun_var), \
            ghrad_daily, ghrad_heatmap, dnrad_profile, dnrad_heatmap, difhrad_profile, difhrad_heatmap
            
    else:
        return lat_long_solar(df, meta), monthly_solar(df, meta), yearly_solar_radiation(df), custom_sunpath(df, meta, global_local, custom_sun_var), \
            ghrad_daily, ghrad_heatmap, dnrad_profile, dnrad_heatmap, difhrad_profile, difhrad_heatmap

######################
### TAB FIVE: WIND ###
######################
### Annual + Custom Windrose and Heatmaps ### 
@app.callback(
    Output('wind-rose', 'figure'),
    Output('wind-speed', 'figure'),
    Output('wind-direction', 'figure'),
    Output('custom-wind-rose', 'figure'),

    # Custom Sliders
    [Input('month-slider', 'value')],
    [Input('hour-slider', 'value')],

    # General
    [Input('df-store', 'modified_timestamp')],
    [Input('global-local-radio-input', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_five(month, hour, ts, global_local, df, meta):
    """ Update the contents of tab five. Passing in the info from the sliders and the general info (df, meta).
    """
    df = pd.read_json(df, orient = 'split')

    # Heatmap Graphs
    speed = heatmap(df, 'Wspeed', global_local)
    direction = heatmap(df, 'Wdir', global_local)

    # Wind Rose Graphs
    annual = wind_rose(df, meta, "Annual Wind Rose", [1, 12], [1, 24])
    custom = wind_rose(df, meta, "", month, hour)

    return annual, speed, direction, custom

### Seasonal Graphs ###
@app.callback(
    # Graphs
    Output('winter-wind-rose', 'figure'),
    Output('spring-wind-rose', 'figure'),
    Output('summer-wind-rose', 'figure'),
    Output('fall-wind-rose', 'figure'),

    # Text 
    Output('winter-wind-rose-text', 'children'),
    Output('spring-wind-rose-text', 'children'),
    Output('summer-wind-rose-text', 'children'),
    Output('fall-wind-rose-text', 'children'),

    # General
    [Input('df-store', 'modified_timestamp')],
    [Input('global-local-radio-input', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_five_seasonal_graphs(ts, global_local, df, meta):
    """ Update the contents of tab five. Passing in the info from the sliders and the general info (df, meta).
    """
    df = pd.read_json(df, orient = 'split')

    hours = [1, 24]
    winter_months = [12, 2]
    spring_months = [3, 5]
    summer_months = [6, 8]
    fall_months = [9, 12]

    # Wind Rose Graphs
    winter = wind_rose(df, meta, "", winter_months, hours)
    spring = wind_rose(df, meta, "", spring_months, hours)
    summer = wind_rose(df, meta, "", summer_months, hours)
    fall = wind_rose(df, meta, "", fall_months, hours)

    # Text 
    winter_df = df.loc[(df['month'] <= winter_months[1]) | (df['month'] >= winter_months[0])]
    winter_total_count = winter_df.shape[0]
    winter_calm_count = winter_df.query("Wspeed == 0").shape[0]

    spring_df = df.loc[ (df['month'] >= spring_months[0]) & (df['month'] <= spring_months[1])]
    spring_total_count = spring_df.shape[0]
    spring_calm_count = spring_df.query("Wspeed == 0").shape[0]

    summer_df = df.loc[(df['month'] >= summer_months[0]) & (df['month'] <= summer_months[1])]
    summer_total_count = summer_df.shape[0]
    summer_calm_count = summer_df.query("Wspeed == 0").shape[0]

    fall_df = df.loc[(df['month'] >= fall_months[0]) & (df['month'] <= fall_months[1])]
    fall_total_count = fall_df.shape[0]
    fall_calm_count = fall_df.query("Wspeed == 0").shape[0]

    winter_text = "Observations between the months of " + month_lst[winter_months[0] - 1] + \
    " and " + month_lst[winter_months[1] - 1] + " between " + str(hours[0]) + ":00 hours and " \
    + str(hours[1])+":00 hours. Selected observations " + str(winter_total_count) + " of 8760, or " \
    + str(int(100 * (winter_total_count / 8760))) + "%. " + str(winter_calm_count) + " observations have calm winds."
    
    spring_text = "Observations between the months of " + month_lst[spring_months[0] - 1] + \
    " and " + month_lst[spring_months[1] - 1] + " between " + str(hours[0]) + ":00 hours and " \
    + str(hours[1])+":00 hours. Selected observations " + str(spring_total_count) + " of 8760, or " \
    + str(int(100 * (spring_total_count / 8760))) + "%. " + str(spring_calm_count) + " observations have calm winds."

    summer_text = "Observations between the months of " + month_lst[summer_months[0] - 1] + \
    " and " + month_lst[summer_months[1] - 1] + " between " + str(hours[0]) + ":00 hours and " \
    + str(hours[1])+":00 hours. Selected observations " + str(summer_total_count) + " of 8760, or " \
    + str(int(100 * (summer_total_count / 8760))) + "%. " + str(summer_calm_count) + " observations have calm winds."

    fall_text = "Observations between the months of " + month_lst[fall_months[0] - 1] + \
    " and " + month_lst[fall_months[1] - 1] + " between " + str(hours[0]) + ":00 hours and " \
    + str(hours[1])+":00 hours. Selected observations " + str(fall_total_count) + " of 8760, or " \
    + str(int(100 * (fall_total_count / 8760))) + "%. " + str(fall_calm_count) + " observations have calm winds."

    return winter, spring, summer, fall, winter_text, spring_text, summer_text, fall_text

### Daily Graphs ###
@app.callback(
    # Daily Graphs 
    Output('morning-wind-rose', 'figure'),
    Output('noon-wind-rose', 'figure'),
    Output('night-wind-rose', 'figure'),

    # Text 
    Output('morning-windrose-text', 'children'),
    Output('noon-windrose-text', 'children'),
    Output('night-windrose-text', 'children'),

    # General 
    [Input('df-store', 'modified_timestamp')],
    [Input('global-local-radio-input', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_five_daily_graphs(ts, global_local, df, meta):
    """ Update the contents of tab five. Passing in the info from the sliders and the general info (df, meta).
    """
    df = pd.read_json(df, orient = 'split')

    months = [1, 12]
    morning_times = [6, 13]
    noon_times = [14, 21]
    night_times = [22, 5]

    # Wind Rose Graphs
    morning = wind_rose(df, meta, "", months, morning_times)
    noon = wind_rose(df, meta, "", months, noon_times)
    night = wind_rose(df, meta, "", months, night_times)

    # Text 
    total_count = df.shape[0]
    calm_count = df.query("Wspeed == 0").shape[0]
    morning_text = "Observations between the months of " + month_lst[months[0] - 1] + \
        " and " + month_lst[months[1] - 1] + " between " + str(morning_times[0]) + ":00 hours and " \
        + str(morning_times[1])+":00 hours. Selected observations " + str(total_count) + " of 8760, or " \
        + str(int(100 * (total_count / 8760))) + "% " + str(calm_count) + " observations have calm winds."
    noon_text = "Observations between the months of " + month_lst[months[0] - 1] + \
        " and " + month_lst[months[1] - 1] + " between " + str(noon_times[0]) + ":00 hours and " \
        + str(noon_times[1])+":00 hours. Selected observations " + str(total_count) + " of 8760, or " \
        + str(int(100 * (total_count / 8760))) + "% " + str(calm_count) + " observations have calm winds."
    night_text = "Observations between the months of " + month_lst[months[0] - 1] + \
        " and " + month_lst[months[1] - 1] + " between " + str(night_times[0]) + ":00 hours and " \
        + str(night_times[1])+":00 hours. Selected observations " + str(total_count) + " of 8760, or " \
        + str(int(100 * (total_count / 8760))) + "% " + str(calm_count) + " observations have calm winds."

    return morning, noon, night, morning_text, noon_text, night_text


###########################
### TAB SIX: QUERY DATA ###
###########################

### Section One ###
@app.callback(
    Output('query-yearly', 'figure'),
    Output('query-daily', 'figure'),
    Output('query-heatmap', 'figure'),

    # Section One
    [Input('sec1-var-dropdown', 'value')],

    # General 
    [Input('df-store', 'modified_timestamp')],
    [Input('global-local-radio-input', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_six_one(var, ts, global_local, df, meta):
    """ Update the contents of tab size. Passing in the info from the dropdown and the general info.
    """
    df = pd.read_json(df, orient = 'split')
    return yearly_profile(df, var, global_local), daily_profile(df, var, global_local), \
        heatmap(df, var, global_local)

### Section Two ###
@app.callback(
    Output('custom-heatmap', 'figure'),
    # Output('custom-summary', 'figure'),

    # Section Two
    [Input('sec2-var-dropdown', 'value')],
    [Input('sec2-time-filter-input', 'value')],
    [Input('sec2-month-slider', 'value')],
    [Input('sec2-hour-slider', 'value')],
    [Input('sec2-data-filter-input', 'value')],
    [Input('sec2-data-filter-var', 'value')],
    [Input('sec2-min-val', 'value')],
    [Input('sec2-max-val', 'value')],
    [Input('normalize', 'value')],

    # General 
    [Input('df-store', 'modified_timestamp')],
    [Input('global-local-radio-input', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_six_two(var, time_filter, month, hour, data_filter, \
    filter_var, min_val, max_val, normalize, \
    ts, global_local, df, meta):
    """ Update the contents of tab size. Passing in the info from the dropdown and the general info.
    """
    df = pd.read_json(df, orient = 'split')
    time_filter_info = [time_filter, month, hour]
    data_filter_info = [data_filter, filter_var, min_val, max_val]
    # custom_summary(df, global_local, first_var, time_filter_info, data_filter_info, normalize)
    return custom_heatmap(df, global_local, var, time_filter_info, data_filter_info)

### Section Three ###
@app.callback(
    Output('three-var', 'figure'),
    Output('two-var', 'figure'),

    # Section Three
    [Input('var-x-dropdown', 'value')],
    [Input('var-y-dropdown', 'value')],
    [Input('colorby-dropdown', 'value')],
    [Input('sec3-time-filter-input', 'value')],
    [Input('sec3-query-month-slider', 'value')],
    [Input('sec3-query-hour-slider', 'value')],
    [Input('sec3-data-filter-input', 'value')],
    [Input('sec3-filter-var-dropdown', 'value')],
    [Input('sec3-min-val', 'value')],
    [Input('sec3-max-val', 'value')],

    # General 
    [Input('df-store', 'modified_timestamp')],
    [Input('global-local-radio-input', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_six_three(var_x, var_y, colorby, time_filter3, \
    month3, hour3, data_filter3, data_filter_var3, min_val3, max_val3, \
    ts, global_local, df, meta):
    """ Update the contents of tab size. Passing in the info from the dropdown and the general info.
    """
    df = pd.read_json(df, orient = 'split')
    time_filter_info3 = [time_filter3, month3, hour3]
    data_filter_info3 = [data_filter3, data_filter_var3, min_val3, max_val3]
    return three_var_graph(df, global_local, var_x, var_y, colorby, time_filter_info3, data_filter_info3), \
        two_var_graph(df, global_local, var_x, var_y, colorby, time_filter_info3, data_filter_info3)