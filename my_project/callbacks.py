import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from .server import app 
from .extract_df import create_df

from .tab_one.tab_one import tab_one
from .tab_two.tab_two import tab_two
from .tab_three.tab_three import tab_three
from .tab_four.tab_four import tab_four
from .tab_five.tab_five import tab_five
from .tab_six.tab_six import tab_six
from .tab_eight.tab_eight import tab_eight

from .tab_two.tab_two_graphs import world_map, dbt_violin, humidity_violin, solar_violin, wind_violin
from .tab_three.tab_three_graphs import yearly_profile_dbt, yearly_profile_rh, daily_profile_dbt, daily_profile_rh, heatmap_rh, heatmap_dbt
from .tab_four.tab_four_graphs import polar_solar, lat_long_solar, monthly_solar, custom_sunpath, yearly_solar_radiation, heatmap_ghrad, heatmap_difhrad, heatmap_dnrad, daily_profile_ghrad, daily_profile_difhrad, daily_profile_dnrad
from .tab_five.tab_five_graphs import custom_wind_rose, wind_speed_heatmap, wind_direction_heatmap

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
    return world_map(df, meta), dbt_violin(df, meta, global_local), humidity_violin(df, meta, global_local), \
        solar_violin(df, meta, global_local), wind_violin(df, meta, global_local), location, lon, lat, elevation

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
    return yearly_profile_dbt(df, global_local), daily_profile_dbt(df, global_local), \
        heatmap_dbt(df, global_local), yearly_profile_rh(df, global_local), \
        daily_profile_rh(df, global_local), heatmap_rh(df, global_local)

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
    if solar_dropdown == 'polar':
        return polar_solar(df, meta), monthly_solar(df, meta), yearly_solar_radiation(df), custom_sunpath(df, meta, global_local, custom_sun_var), \
            daily_profile_ghrad(df, global_local), heatmap_ghrad(df, global_local), \
            daily_profile_dnrad(df, global_local), heatmap_dnrad(df, global_local), \
            daily_profile_difhrad(df, global_local), heatmap_difhrad(df, global_local)
            
    else:
        return lat_long_solar(df, meta), monthly_solar(df, meta), yearly_solar_radiation(df), custom_sunpath(df, meta, global_local, custom_sun_var), \
            daily_profile_ghrad(df, global_local), heatmap_ghrad(df, global_local), \
            daily_profile_dnrad(df, global_local), heatmap_dnrad(df, global_local), \
            daily_profile_difhrad(df, global_local), heatmap_difhrad(df, global_local)

######################
### TAB FIVE: WIND ###
######################
@app.callback(
    Output('wind-rose', 'figure'),
    Output('wind-speed', 'figure'),
    Output('wind-direction', 'figure'),
    Output('winter-wind-rose', 'figure'),
    Output('spring-wind-rose', 'figure'),
    Output('summer-wind-rose', 'figure'),
    Output('fall-wind-rose', 'figure'),
    Output('morning-wind-rose', 'figure'),
    Output('noon-wind-rose', 'figure'),
    Output('night-wind-rose', 'figure'),
    Output('custom-wind-rose', 'figure'),
    [Input('month-slider', 'value')],
    [Input('hour-slider', 'value')],
    [Input('df-store', 'modified_timestamp')],
    [Input('global-local-radio-input', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_five(month, hour, ts, global_local, df, meta):
    """ Update the contents of tab five. Passing in the info from the sliders and the general info (df, meta).
    """
    df = pd.read_json(df, orient = 'split')
    return custom_wind_rose(df, meta, [1, 12], [1, 24]), wind_speed_heatmap(df, global_local), wind_direction_heatmap(df, global_local), \
        custom_wind_rose(df, meta, [12, 2], [1, 24]), custom_wind_rose(df, meta, [3, 5], [1, 24]), custom_wind_rose(df, meta, [6, 8], [1, 24]), custom_wind_rose(df, meta, [9, 12], [1, 24]), \
        custom_wind_rose(df, meta, [1, 12], [6, 13]), custom_wind_rose(df, meta, [1, 12], [14, 21]), custom_wind_rose(df, meta, [1, 12], [22, 5]), \
        custom_wind_rose(df, meta, month, hour)

###########################
### TAB SIX: QUERY DATA ###
###########################
# @app.callback(
#     Output('', 'figure'),
#     Output('', 'figure'),
#     Output('', 'figure'),
#     [Input('query-var-dropdown', 'modified_timestamp')],
#     [Input('df-store', 'modified_timestamp')],
#     [Input('units-radio-input', 'value')],
#     [Input('global-local-radio-input', 'value')],
#     [State('df-store', 'data')],
#     [State('meta-store', 'data')]
# )
# def update_tab_six(var, ts, units, global_local, df, meta):
#     """ Update the contents of tab size. Passing in the info from the dropdown and the general info.
#     """
#     return 