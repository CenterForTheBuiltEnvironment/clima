import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from my_project.utils import generate_chart_name, code_timer
from my_project.template_graphs import heatmap, yearly_profile, daily_profile
import pandas as pd

from app import app, cache, TIMEOUT


def layout_t_rh():
    return html.Div(
        className="container-col full-width",
        children=[
            html.Div(
                className="container-row full-width text-dropdown-container",
                children=[
                    html.H6(className="text-next-to-input", children=["Variable: "]),
                    dcc.Dropdown(
                        id="dropdown",
                        className="dropdown-t-rh",
                        options=[
                            {"label": "Dry Bulb Temperature", "value": "dd_tdb"},
                            {"label": "Relative Humidity", "value": "dd_rh"},
                        ],
                        value="dd_tdb",
                    ),
                ],
            ),
            html.Div(
                className="container-col",
                children=[
                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="yearly"),
                    ),
                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="daily"),
                    ),
                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="heatmap"),
                    ),
                ],
            ),
        ],
    )


@app.callback(
    Output("yearly", "children"),
    [Input("global-local-radio-input", "value")],
    [Input("dropdown", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
@code_timer
def update_yearly(global_local, dd_value, df, meta):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")

    if dd_value == "dd_tdb":
        dbt_yearly = yearly_profile(df, "DBT", global_local)
        dbt_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

        return dcc.Graph(
            config=generate_chart_name("tmp_rh", meta),
            figure=dbt_yearly,
        )
    else:
        rh_yearly = yearly_profile(df, "RH", global_local)
        rh_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

        return dcc.Graph(
            config=generate_chart_name("tmp_rh", meta),
            figure=rh_yearly,
        )


@app.callback(
    Output("daily", "children"),
    [Input("global-local-radio-input", "value")],
    [Input("dropdown", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
@code_timer
def update_tab_three_db_daily(global_local, dd_value, df, meta):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")

    if dd_value == "dd_tdb":
        return dcc.Graph(
            config=generate_chart_name("tmp_rh", meta),
            figure=daily_profile(df, "DBT", global_local),
        )
    else:
        return dcc.Graph(
            config=generate_chart_name("tmp_rh", meta),
            figure=daily_profile(df, "RH", global_local),
        )


@app.callback(
    Output("heatmap", "children"),
    [Input("global-local-radio-input", "value")],
    [Input("dropdown", "value")],
    [State("df-store", "data")],
    [State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
@code_timer
def update_tab_three_db_heatmap(global_local, dd_value, df, meta):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    if dd_value == "dd_tdb":
        return dcc.Graph(
            config=generate_chart_name("tmp_rh", meta),
            figure=heatmap(df, "DBT", global_local),
        )
    else:
        return dcc.Graph(
            config=generate_chart_name("tmp_rh", meta),
            figure=heatmap(df, "RH", global_local),
        )
