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
from .tab_eight.tab_eight import tab_eight

from .tab_two.tab_two_graphs import world_map, dbt_violin, humidity_violin, solar_violin, wind_violin
from .tab_three.tab_three_graphs import daily_dbt, daily_humidity, monthly_dbt, monthly_humidity, heatmap_dbt, heatmap_humidity
from .tab_four.tab_four_graphs import polar_solar, lat_long_solar, monthly_solar, horizontal_solar, diffuse_solar, direct_solar, cloud_cover
from .tab_five.tab_five_graphs import wind_rose

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
        return html.Div(
            children = [
                html.H3('Tab content 6')
            ]
        )
    elif tab == 'tab-7':
        return html.Div(
            children = [
                html.H3('Tab content 7')
            ]
        )
    elif tab == 'tab-8':
        return tab_eight()

##############################
### TAB ONE: SUBMIT BUTTON ###        
##############################

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
    [Input('df-store', 'data')],
    [Input('submit-button', 'n_clicks')]
)
def alert_display(data, n_clicks):
    """ Displays the alert for the submit button. 
    """
    if n_clicks is None:
        return True, "To start, submit a link below!", "primary"
    if data is None and n_clicks > 0:
        return True, "This link is not available. Please choose another one.", "warning"
    else:
        return True, "Successfully loaded data. Check out the other tabs!", "success"


################################
### UPDATE INFO TO TABS ###        
################################

### TAB TWO ###
@app.callback(
    Output('world-map', 'figure'),
    Output('temp-profile-graph', 'figure'),
    Output('humidity-profile-graph', 'figure'),
    Output('solar-radiation-graph', 'figure'),
    Output('wind-speed-graph', 'figure'),
    [Input('df-store', 'modified_timestamp')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_two(ts, df, meta):
    """ Update the contents of tab two. Passing in the general info (df, meta).
    """
    df = pd.read_json(df, orient = 'split')
    return world_map(df, meta), dbt_violin(df, meta), humidity_violin(df, meta), \
        solar_violin(df, meta), wind_violin(df, meta)

### TAB THREE ###
@app.callback(
    Output('daily-dbt', 'figure'),
    Output('daily-humidity', 'figure'),
    Output('monthly-dbt-3', 'figure'),
    Output('monthly-humidity', 'figure'),
    Output('heatmap-dbt', 'figure'),
    Output('heatmap-humidity', 'figure'),
    [Input('df-store', 'modified_timestamp')],
    [Input('units-radio-input', 'value')],
    [Input('global-local-radio-input', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_three(ts, units, global_local, df, meta):
    """ Update the contents of tab three. Passing in general info (df, meta).
    """
    df = pd.read_json(df, orient = 'split')
    return daily_dbt(df, meta, units), daily_humidity(df, meta, units), \
        monthly_dbt(df, meta, units, global_local), monthly_humidity(df, meta, units, global_local), \
        heatmap_dbt(df, meta, units, global_local), heatmap_humidity(df, meta, units, global_local)

### TAB FOUR ###
@app.callback(
    Output('solar-dropdown-output', 'figure'),
    Output('monthly-solar', 'figure'),
    Output('horizontal-solar', 'figure'),
    Output('diffuse-solar', 'figure'),
    Output('direct-solar', 'figure'),
    Output('cloud-cover', 'figure'),
    [Input("solar-dropdown", 'value')],
    [Input('df-store', 'modified_timestamp')],
    [Input('units-radio-input', 'value')],
    [Input('global-local-radio-input', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_four(solar_dropdown, ts, units, global_local, df, meta):
    """ Update the contents of tab four. Passing in the polar selection and the general info (df, meta).
    """
    df = pd.read_json(df, orient = 'split')
    if solar_dropdown == 'polar':
        return polar_solar(df, meta, units), monthly_solar(df, meta, units), \
            horizontal_solar(df, meta, units), diffuse_solar(df, meta, units), \
            direct_solar(df, meta, units), cloud_cover(df, meta, units)
    else:
        return lat_long_solar(df, meta, units), monthly_solar(df, meta, units), \
            horizontal_solar(df, meta, units), diffuse_solar(df, meta, units), \
            direct_solar(df, meta, units), cloud_cover(df, meta, units)

### TAB FIVE ###
@app.callback(
    Output('wind-rose', 'figure'),
    [Input('month-slider', 'value')],
    [Input('hour-slider', 'value')],
    [Input('df-store', 'modified_timestamp')],
    [Input('units-radio-input', 'value')],
    [Input('global-local-radio-input', 'value')],
    [State('df-store', 'data')],
    [State('meta-store', 'data')]
)
def update_tab_five(month, hour, ts, units, global_local, df, meta):
    """ Update the contents of tab five. Passing in the info from the sliders and the general info (df, meta).
    """
    df = pd.read_json(df, orient = 'split')
    return wind_rose(df, meta, units, month, hour)