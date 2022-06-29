from dash import dcc, html
from dash_extensions.enrich import Output, Input, State
from my_project.utils import (
    generate_chart_name,
    title_with_tooltip,
    summary_table_tmp_rh_tab,
)
from my_project.template_graphs import heatmap, yearly_profile, daily_profile
from my_project.global_scheme import dropdown_names
from my_project.utils import code_timer

from app import app

var_to_plot = ["Dry bulb temperature", "Relative humidity"]


def layout_t_rh():
    return html.Div(
        className="container-col full-width",
        children=[
            html.Div(
                className="container-row full-width align-center justify-center",
                children=[
                    html.H4(
                        className="text-next-to-input", children=["Select a variable: "]
                    ),
                    dcc.Dropdown(
                        id="dropdown",
                        className="dropdown-t-rh",
                        options=[
                            {
                                "label": var,
                                "value": dropdown_names[var],
                            }
                            for var in var_to_plot
                        ],
                        value=dropdown_names[var_to_plot[0]],
                    ),
                ],
            ),
            html.Div(
                className="container-col",
                children=[
                    html.Div(
                        children=title_with_tooltip(
                            text="Yearly chart",
                            tooltip_text=None,
                            id_button="yearly-chart-label",
                        ),
                    ),
                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="yearly-chart"),
                    ),
                    html.Div(
                        children=title_with_tooltip(
                            text="Daily chart",
                            tooltip_text=None,
                            id_button="daily-chart-label",
                        ),
                    ),
                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="daily"),
                    ),
                    html.Div(
                        children=title_with_tooltip(
                            text="Heatmap chart",
                            tooltip_text=None,
                            id_button="heatmap-chart-label",
                        ),
                    ),
                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="heatmap"),
                    ),
                    html.Div(
                        children=title_with_tooltip(
                            text="Descriptive statistics",
                            tooltip_text="count, mean, std, min, max, and percentiles",
                            id_button="table-tmp-rh",
                        ),
                    ),
                    html.Div(
                        id="table-tmp-hum",
                    ),
                ],
            ),
        ],
    )


@app.callback(
    Output("yearly-chart", "children"),
    [Input("global-local-radio-input", "value"), Input("dropdown", "value")],
    [State("df-store", "data"), State("meta-store", "data")],
)
@code_timer
def update_yearly_chart(global_local, dd_value, df, meta):

    if dd_value == dropdown_names[var_to_plot[0]]:
        dbt_yearly = yearly_profile(df, "DBT", global_local)
        dbt_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

        return dcc.Graph(
            config=generate_chart_name("tdb_yearly_t_rh", meta),
            figure=dbt_yearly,
        )
    else:
        rh_yearly = yearly_profile(df, "RH", global_local)
        rh_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

        return dcc.Graph(
            config=generate_chart_name("rh_yearly_t_rh", meta),
            figure=rh_yearly,
        )


@app.callback(
    Output("daily", "children"),
    [Input("global-local-radio-input", "value"), Input("dropdown", "value")],
    [State("df-store", "data"), State("meta-store", "data")],
)
@code_timer
def update_daily(global_local, dd_value, df, meta):

    if dd_value == dropdown_names[var_to_plot[0]]:
        return dcc.Graph(
            config=generate_chart_name("tdb_daily_t_rh", meta),
            figure=daily_profile(
                df[["DBT", "hour", "UTC_time", "month_names", "day", "month"]],
                "DBT",
                global_local,
            ),
        )
    else:
        return dcc.Graph(
            config=generate_chart_name("rh_daily_t_rh", meta),
            figure=daily_profile(
                df[["RH", "hour", "UTC_time", "month_names", "day", "month"]],
                "RH",
                global_local,
            ),
        )


@app.callback(
    Output("heatmap", "children"),
    [Input("global-local-radio-input", "value"), Input("dropdown", "value")],
    [State("df-store", "data"), State("meta-store", "data")],
)
@code_timer
def update_heatmap(global_local, dd_value, df, meta):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    if dd_value == dropdown_names[var_to_plot[0]]:
        return dcc.Graph(
            config=generate_chart_name("tdb_heatmap_t_rh", meta),
            figure=heatmap(
                df[["DBT", "hour", "UTC_time", "month_names", "day"]],
                "DBT",
                global_local,
            ),
        )
    else:
        return dcc.Graph(
            config=generate_chart_name("rh_heatmap_t_rh", meta),
            figure=heatmap(
                df[["RH", "hour", "UTC_time", "month_names", "day"]],
                "RH",
                global_local,
            ),
        )


@app.callback(
    Output("table-tmp-hum", "children"),
    [Input("dropdown", "value")],
    [State("df-store", "data")],
)
@code_timer
def update_table(dd_value, df):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    return summary_table_tmp_rh_tab(
        df[["month", "hour", dd_value, "month_names"]], dd_value
    )
