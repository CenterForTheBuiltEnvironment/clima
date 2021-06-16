import dash_core_components as dcc
import dash_html_components as html
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
                children=[html.Div(id="daily-dbt")],
            ),
            dcc.Loading(
                type="circle",
                children=[html.Div(id="heatmap-dbt")],
            ),
            html.H5("Relative Humidity"),
            dcc.Loading(
                type="circle",
                children=[html.Div(id="yearly-rh")],
            ),
            dcc.Loading(
                type="circle",
                children=[html.Div(id="daily-rh")],
            ),
            dcc.Loading(
                type="circle",
                children=[html.Div(id="heatmap-rh")],
            ),
        ],
    )


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
        config=generate_chart_name("tmp_rh", meta),
        figure=dbt_yearly,
    )


@app.callback(
    Output("daily-dbt", "children"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_three_db_daily(global_local, df, meta):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    return dcc.Graph(
        config=generate_chart_name("tmp_rh", meta),
        figure=daily_profile(df, "DBT", global_local),
    )


@app.callback(
    Output("heatmap-dbt", "children"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_three_db_heatmap(global_local, df, meta):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    return dcc.Graph(
        config=generate_chart_name("tmp_rh", meta),
        figure=heatmap(df, "DBT", global_local),
    )


@app.callback(
    Output("yearly-rh", "children"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_three_rh_yearly(global_local, df, meta):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    rh_yearly = yearly_profile(df, "RH", global_local)
    rh_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

    return dcc.Graph(
        config=generate_chart_name("tmp_rh", meta),
        figure=rh_yearly,
    )


@app.callback(
    Output("daily-rh", "children"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_three_rh_daily(global_local, df, meta):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    return dcc.Graph(
        config=generate_chart_name("tmp_rh", meta),
        figure=daily_profile(df, "RH", global_local),
    )


@app.callback(
    Output("heatmap-rh", "children"),
    [Input("global-local-radio-input", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_three_rh_heatmap(global_local, df, meta):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    return dcc.Graph(
        config=generate_chart_name("tmp_rh", meta),
        figure=heatmap(df, "RH", global_local),
    )
