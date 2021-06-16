import dash_core_components as dcc
import dash_html_components as html
from my_project.global_scheme import fig_config
from dash.dependencies import Input, Output, State
from my_project.utils import generate_chart_name
from my_project.template_graphs import heatmap, yearly_profile, daily_profile
import pandas as pd

from app import app, cache, TIMEOUT


def layout_t_rh():
    return html.Div(
        className="container-col",
        children=[
            html.H5("Dry Bulb Temperature"),
            dcc.Loading(
                type="circle",
                children=[html.Div(id="yearly-dbt")],
            ),
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="daily-dbt", config=fig_config),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="heatmap-dbt", config=fig_config),
                ],
            ),
            html.H5("Relative Humidity"),
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="yearly-rh", config=fig_config),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="daily-rh", config=fig_config),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="heatmap-rh", config=fig_config),
                ],
            ),
        ],
    )


# TAB THREE: TEMP AND HUMIDITY
@app.callback(
    Output("yearly-dbt", "children"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_three_db_yearly(global_local, df, meta):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    # Yearly Graphs
    dbt_yearly = yearly_profile(df, "DBT", global_local)
    dbt_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

    return dcc.Graph(
        config=generate_chart_name("t_rh", meta),
        figure=dbt_yearly,
    )


@app.callback(
    Output("daily-dbt", "figure"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_three_db_daily(global_local, df):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    dbt_daily = daily_profile(df, "DBT", global_local)
    return dbt_daily


@app.callback(
    Output("heatmap-dbt", "figure"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_three_db_heatmap(global_local, df):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    # Heatmap Graphs
    dbt_heatmap = heatmap(df, "DBT", global_local)
    return dbt_heatmap


@app.callback(
    Output("yearly-rh", "figure"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_three_rh_yearly(global_local, df):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    rh_yearly = yearly_profile(df, "RH", global_local)
    rh_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

    return rh_yearly


@app.callback(
    Output("daily-rh", "figure"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_three_rh_daily(global_local, df):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    # Daily Profile Graphs
    rh_daily = daily_profile(df, "RH", global_local)

    return rh_daily


@app.callback(
    Output("heatmap-rh", "figure"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_three_rh_heatmap(global_local, df):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    # Heatmap Graphs
    rh_heatmap = heatmap(df, "RH", global_local)

    return rh_heatmap
