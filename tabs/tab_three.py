import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from graphs import tab_three_graphs, config

def tab_three():
    return html.Div(
        className = "container-col", 
        children = [
            dcc.Graph(
                figure = tab_three_graphs.daily_dbt(),
                config = config.config()
            ), 
            dcc.Graph(
                figure = tab_three_graphs.daily_humidity(),
                config = config
            ), 
            dcc.Graph(
                figure = tab_three_graphs.monthly_dbt(),
                config = config.config()
            ), 
            dcc.Graph(
                figure = tab_three_graphs.monthly_humidity(), 
                config = config.config()
            ), 
            dcc.Graph(
                figure = tab_three_graphs.heatmap_dbt(),
                config = config.config()
            ), 
            dcc.Graph(
                figure = tab_three_graphs.heatmap_humidity(),
                config = config.config()
            )
        ]
    )