from dash import dcc, html
from my_project.global_scheme import month_lst, container_row_center_full
from dash.dependencies import Input, Output, State
from my_project.template_graphs import heatmap, wind_rose
from my_project.utils import title_with_tooltip, generate_chart_name, generate_units, generate_custom_inputs_time
from my_project.utils import code_timer

from app import app


def sliders():
    """Returns 2 sliders for the hour"""
    return html.Div(
        className="container-col justify-center",
        id="slider-container",
        children=[
            html.Div(
                className="container-row each-slider",
                children=[
                    html.P("Month Range"),
                    dcc.RangeSlider(
                        id="month-slider",
                        min=1,
                        max=12,
                        step=1,
                        value=[1, 12],
                        marks={1: "1", 12: "12"},
                        tooltip={"always_visible": False, "placement": "top"},
                        allowCross=False,
                    ),
                ],
            ),
            html.Div(
                className="container-row each-slider",
                children=[
                    html.P("Hour Range"),
                    dcc.RangeSlider(
                        id="hour-slider",
                        min=1,
                        max=24,
                        step=1,
                        value=[1, 24],
                        marks={1: "1", 24: "24"},
                        tooltip={"always_visible": False, "placement": "topLeft"},
                        allowCross=False,
                    ),
                ],
            ),
        ],
    )


def seasonal_wind_rose():
    """Return the section with the 4 seasonal wind rose graphs."""
    return html.Div(
        className="container-col",
        children=[
            html.Div(
                children=title_with_tooltip(
                    text="Seasonal Wind Rose",
                    tooltip_text=None,
                    id_button="seasonal-rose-chart",
                ),
            ),
            html.Div(
                className=container_row_center_full,
                children=[
                    html.Div(
                        className="container-col",
                        children=[
                            dcc.Loading(
                                type="circle",
                                children=html.Div(
                                    id="winter-wind-rose",
                                    className="daily-wind-graph",
                                ),
                            ),
                            html.P(
                                className="seasonal-text", id="winter-wind-rose-text"
                            ),
                        ],
                    ),
                    html.Div(
                        className="container-col",
                        children=[
                            dcc.Loading(
                                type="circle",
                                children=html.Div(
                                    id="spring-wind-rose",
                                    className="daily-wind-graph",
                                ),
                            ),
                            html.P(
                                className="seasonal-text", id="spring-wind-rose-text"
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className=container_row_center_full,
                children=[
                    html.Div(
                        className="container-col",
                        children=[
                            dcc.Loading(
                                type="circle",
                                children=html.Div(
                                    id="summer-wind-rose",
                                    className="daily-wind-graph",
                                ),
                            ),
                            html.P(
                                className="seasonal-text", id="summer-wind-rose-text"
                            ),
                        ],
                    ),
                    html.Div(
                        className="container-col",
                        children=[
                            dcc.Loading(
                                type="circle",
                                children=html.Div(
                                    id="fall-wind-rose",
                                    className="daily-wind-graph",
                                ),
                            ),
                            html.P(className="seasonal-text", id="fall-wind-rose-text"),
                        ],
                    ),
                ],
            ),
        ],
    )


def daily_wind_rose():
    """Return the section for the 3 daily wind rose graphs."""
    return html.Div(
        className="container-col full-width",
        id="tab5-daily-container",
        children=[
            html.Div(
                children=title_with_tooltip(
                    text="Daily Wind Rose",
                    tooltip_text=None,
                    id_button="daily-rose-chart",
                ),
            ),
            html.Div(
                id="daily-wind-rose-outer-container",
                className="container-row full-width",
                children=[
                    html.Div(
                        className="container-col",
                        children=[
                            html.Div(
                                dcc.Loading(
                                    type="circle",
                                    children=html.Div(
                                        className="daily-wind-graph",
                                        id="morning-wind-rose",
                                    ),
                                ),
                            ),
                            html.P(className="daily-text", id="morning-wind-rose-text"),
                        ],
                    ),
                    html.Div(
                        className="container-col",
                        children=[
                            html.Div(
                                dcc.Loading(
                                    type="circle",
                                    children=html.Div(
                                        className="daily-wind-graph",
                                        id="noon-wind-rose",
                                    ),
                                ),
                            ),
                            html.P(className="daily-text", id="noon-wind-rose-text"),
                        ],
                    ),
                    html.Div(
                        className="container-col",
                        children=[
                            html.Div(
                                dcc.Loading(
                                    type="circle",
                                    children=html.Div(
                                        className="daily-wind-graph",
                                        id="night-wind-rose",
                                    ),
                                ),
                            ),
                            html.P(className="daily-text", id="night-wind-rose-text"),
                        ],
                    ),
                ],
            ),
        ],
    )


def custom_wind_rose():
    return html.Div(
        className="container-col justify-center full-width",
        children=[
            html.Div(
                children=title_with_tooltip(
                    text="Customizable Wind Rose",
                    tooltip_text=None,
                    id_button="custom-rose-chart",
                ),
            ),
            html.Div(
                className="container-row full-width justify-center",
                id="tab5-custom-dropdown-container",
                children=[
                    html.Div(
                        className="container-col justify-center p-2 mr-2",
                        children=[
                            html.Div(
                                className=container_row_center_full,
                                children=[
                                    html.H6(
                                        style={"width": "8rem"},
                                        children=["Start Month:"],
                                    ),
                                    dcc.Dropdown(
                                        id="tab5-custom-start-month",
                                        options=[
                                            {"label": j, "value": i + 1}
                                            for i, j in enumerate(month_lst)
                                        ],
                                        value=1,
                                        style={"width": "6rem"},
                                    ),
                                ],
                            ),
                            html.Div(
                                className=container_row_center_full,
                                children=[
                                    html.H6(
                                        style={"width": "8rem"},
                                        children=["Start Hour:"],
                                    ),
                                    dcc.Dropdown(
                                        id="tab5-custom-start-hour",
                                        options=[
                                            {"label": str(i) + ":00", "value": i}
                                            for i in range(1, 25)
                                        ],
                                        value=1,
                                        style={"width": "6rem"},
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="container-col justify-center p-2 ml-2",
                        children=[
                            html.Div(
                                className=container_row_center_full,
                                children=[
                                    html.H6(
                                        style={"width": "8rem"},
                                        children=["End Month:"],
                                    ),
                                    dcc.Dropdown(
                                        id="tab5-custom-end-month",
                                        options=[
                                            {"label": j, "value": i + 1}
                                            for i, j in enumerate(month_lst)
                                        ],
                                        value=12,
                                        style={"width": "6rem"},
                                    ),
                                ],
                            ),
                            html.Div(
                                className=container_row_center_full,
                                children=[
                                    html.H6(
                                        style={"width": "8rem"},
                                        children=["End Hour:"],
                                    ),
                                    dcc.Dropdown(
                                        id="tab5-custom-end-hour",
                                        options=[
                                            {"label": str(i) + ":00", "value": i}
                                            for i in range(1, 25)
                                        ],
                                        value=24,
                                        style={"width": "6rem"},
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(id="custom-wind-rose"),
            ),
        ],
    )


def layout_wind():
    """Contents in the fifth tab 'Wind'."""
    return html.Div(
        className="container-col justify-center",
        children=[
            html.Div(
                children=title_with_tooltip(
                    text="Annual Wind Rose",
                    tooltip_text=None,
                    id_button="annual-rose-chart",
                ),
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(
                    id="wind-rose",
                ),
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(id="wind-speed"),
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(id="wind-direction"),
            ),
            seasonal_wind_rose(),
            daily_wind_rose(),
            custom_wind_rose(),
        ],
    )


# wind rose
@app.callback(
    Output("wind-rose", "children"),
    Input("df-store", "modified_timestamp"),
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
@code_timer
def update_annual_wind_rose(ts, df, meta, si_ip):
    """Update the contents of tab five. Passing in the info from the sliders and the general info (df, meta)."""

    annual = wind_rose(df, "", [1, 12], [1, 24], True, si_ip)
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name("annual_wind_rose", meta, units),
        figure=annual,
    )


# wind speed
@app.callback(
    Output("wind-speed", "children"),
    # General
    [
        Input("df-store", "modified_timestamp"),
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
@code_timer
def update_tab_wind_speed(ts, global_local, df, meta, si_ip):
    """Update the contents of tab five. Passing in the info from the sliders and the general info (df, meta)."""

    speed = heatmap(df, "wind_speed", global_local, si_ip)
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name("wind_speed", meta, units),
        figure=speed,
    )


# wind direction
@app.callback(
    Output("wind-direction", "children"),
    # General
    [
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
@code_timer
def update_tab_wind_direction(global_local, df, meta, si_ip):
    """Update the contents of tab five. Passing in the info from the sliders and the general info (df, meta)."""

    direction = heatmap(df, "wind_dir", global_local, si_ip)
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name("wind_direction", meta, units),
        figure=direction,
    )


# Custom Wind rose
@app.callback(
    Output("custom-wind-rose", "children"),
    # Custom Graph Input
    [
        Input("df-store", "modified_timestamp"),
        Input("tab5-custom-start-month", "value"),
        Input("tab5-custom-start-hour", "value"),
        Input("tab5-custom-end-month", "value"),
        Input("tab5-custom-end-hour", "value"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
@code_timer
def update_custom_wind_rose(
    ts, start_month, start_hour, end_month, end_hour, df, meta, si_ip
):
    """Update the contents of tab five. Passing in the info from the sliders and the general info (df, meta)."""

    start_hour = int(start_hour)
    end_hour = int(end_hour)
    start_month = int(start_month)
    end_month = int(end_month)

    # Wind Rose Graphs
    if start_month <= end_month:
        df = df.loc[(df["month"] >= start_month) & (df["month"] <= end_month)]
    else:
        df = df.loc[(df["month"] <= end_month) | (df["month"] >= start_month)]
    if start_hour <= end_hour:
        df = df.loc[(df["hour"] >= start_hour) & (df["hour"] <= end_hour)]
    else:
        df = df.loc[(df["hour"] <= end_hour) | (df["hour"] >= start_hour)]
    custom = wind_rose(
        df, "", [start_month, end_month], [start_hour, end_hour], True, si_ip
    )
    custom_inputs = generate_custom_inputs_time(start_month, end_month, start_hour, end_hour)
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name("custom_wind_rose", meta, custom_inputs, units),
        figure=custom,
    )


### Seasonal Graphs ###
@app.callback(
    [
        Output("winter-wind-rose", "children"),
        Output("spring-wind-rose", "children"),
        Output("summer-wind-rose", "children"),
        Output("fall-wind-rose", "children"),
        Output("winter-wind-rose-text", "children"),
        Output("spring-wind-rose-text", "children"),
        Output("summer-wind-rose-text", "children"),
        Output("fall-wind-rose-text", "children"),
    ],
    [
        Input("df-store", "modified_timestamp"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
@code_timer
def update_seasonal_graphs(ts, df, meta, si_ip):

    hours = [1, 24]
    winter_months = [12, 2]
    spring_months = [3, 5]
    summer_months = [6, 8]
    fall_months = [9, 12]

    # Wind Rose Graphs
    winter = wind_rose(df, "", winter_months, hours, False, si_ip)
    spring = wind_rose(df, "", spring_months, hours, True, si_ip)
    summer = wind_rose(df, "", summer_months, hours, False, si_ip)
    fall = wind_rose(df, "", fall_months, hours, False, si_ip)

    # Text
    winter_df = df.loc[
        (df["month"] <= winter_months[1]) | (df["month"] >= winter_months[0])
    ]
    query_calm_wind = "wind_speed == 0"
    winter_total_count = winter_df.shape[0]
    winter_calm_count = winter_df.query(query_calm_wind).shape[0]

    spring_df = df.loc[
        (df["month"] >= spring_months[0]) & (df["month"] <= spring_months[1])
    ]
    spring_total_count = spring_df.shape[0]
    spring_calm_count = spring_df.query(query_calm_wind).shape[0]

    summer_df = df.loc[
        (df["month"] >= summer_months[0]) & (df["month"] <= summer_months[1])
    ]
    summer_total_count = summer_df.shape[0]
    summer_calm_count = summer_df.query(query_calm_wind).shape[0]

    fall_df = df.loc[(df["month"] >= fall_months[0]) & (df["month"] <= fall_months[1])]
    fall_total_count = fall_df.shape[0]
    fall_calm_count = fall_df.query(query_calm_wind).shape[0]

    def seasonal_chart_caption(month_start, month_end, count, n_calm):
        return (
            f"Observations between the months of {month_start} and {month_end} "
            f"between 01:00 hours and 24:00 hours. "
            f"Selected observations {str(count)} of 8760, or "
            f"{str(int(100 * (count / 8760)))} %. {str(n_calm)} observations have "
            f"calm winds."
        )

    winter_text = seasonal_chart_caption(
        month_lst[winter_months[0] - 1],
        month_lst[winter_months[1] - 1],
        winter_total_count,
        winter_calm_count,
    )
    spring_text = seasonal_chart_caption(
        month_lst[spring_months[0] - 1],
        month_lst[spring_months[1] - 1],
        spring_total_count,
        spring_calm_count,
    )
    summer_text = seasonal_chart_caption(
        month_lst[summer_months[0] - 1],
        month_lst[summer_months[1] - 1],
        summer_total_count,
        summer_calm_count,
    )
    fall_text = seasonal_chart_caption(
        month_lst[fall_months[0] - 1],
        month_lst[fall_months[1] - 1],
        fall_total_count,
        fall_calm_count,
    )
    units = generate_units(si_ip)
    return (
        dcc.Graph(
            config=generate_chart_name("winter_wind_rose", meta, units),
            figure=winter,
        ),
        dcc.Graph(
            config=generate_chart_name("spring_wind_rose", meta, units),
            figure=spring,
        ),
        dcc.Graph(
            config=generate_chart_name("summer_wind_rose", meta, units),
            figure=summer,
        ),
        dcc.Graph(
            config=generate_chart_name("fall_wind_rose", meta, units),
            figure=fall,
        ),
        winter_text,
        spring_text,
        summer_text,
        fall_text,
    )


### Daily Graphs ###
@app.callback(
    # Daily Graphs
    [
        Output("morning-wind-rose", "children"),
        Output("noon-wind-rose", "children"),
        Output("night-wind-rose", "children"),
        Output("morning-wind-rose-text", "children"),
        Output("noon-wind-rose-text", "children"),
        Output("night-wind-rose-text", "children"),
    ],
    # General
    Input("df-store", "modified_timestamp"),
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
@code_timer
def update_daily_graphs(ts, df, meta, si_ip):
    """Update the contents of tab five. Passing in the info from the sliders and the general info (df, meta)."""

    months = [1, 12]
    morning_times = [6, 13]
    noon_times = [14, 21]
    night_times = [22, 5]

    # Wind Rose Graphs
    morning = wind_rose(df, "", months, morning_times, False, si_ip)
    noon = wind_rose(df, "", months, noon_times, False, si_ip)
    night = wind_rose(df, "", months, night_times, True, si_ip)

    # Text
    query_calm_wind = "wind_speed == 0"
    morning_df = df.loc[
        (df["hour"] >= morning_times[0]) & (df["hour"] <= morning_times[1])
    ]
    morning_total_count = morning_df.shape[0]
    morning_calm_count = morning_df.query(query_calm_wind).shape[0]

    noon_df = df.loc[
        (df["hour"] >= morning_times[0]) & (df["hour"] <= morning_times[1])
    ]
    noon_total_count = noon_df.shape[0]
    noon_calm_count = noon_df.query(query_calm_wind).shape[0]

    night_df = df.loc[(df["hour"] <= night_times[1]) | (df["hour"] >= night_times[0])]
    night_total_count = night_df.shape[0]
    night_calm_count = night_df.query(query_calm_wind).shape[0]

    def daily_chart_caption(hour_start, hour_end, count, calm_count):
        return (
            f"Observations between the months of Jan and Dec between "
            f"{str(hour_start)}:00 hours and {str(hour_end)}:00 hours. "
            f"Selected observations {count} of 8760, or "
            f"{str(int(100 * (count / 8760)))}%. {calm_count} "
            f"observations have calm winds."
        )

    morning_text = daily_chart_caption(
        morning_times[0], morning_times[1], morning_total_count, morning_calm_count
    )

    noon_text = daily_chart_caption(
        noon_times[0], noon_times[1], noon_total_count, noon_calm_count
    )

    night_text = daily_chart_caption(
        night_times[0], night_times[1], night_total_count, night_calm_count
    )
    units = generate_units(si_ip)
    return (
        dcc.Graph(
            config=generate_chart_name("morning_wind_rose", meta, units),
            figure=morning,
        ),
        dcc.Graph(
            config=generate_chart_name("noon_wind_rose", meta, units),
            figure=noon,
        ),
        dcc.Graph(
            config=generate_chart_name("night_wind_rose", meta, units),
            figure=night,
        ),
        morning_text,
        noon_text,
        night_text,
    )
