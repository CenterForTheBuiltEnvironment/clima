import dash_bootstrap_components as dbc
from copy import deepcopy
from dash import dcc
from dash import html
from dash.exceptions import PreventUpdate
from my_project.utils import (
    generate_chart_name,
    generate_custom_inputs,
    generate_custom_inputs_explorer,
    generate_units,
    title_with_tooltip,
    summary_table_tmp_rh_tab,
    code_timer,
)

from my_project.global_scheme import (
    fig_config,
    dropdown_names,
    sun_cloud_tab_dropdown_names,
    more_variables_dropdown,
    sun_cloud_tab_explore_dropdown_names,
    container_row_center_full,
    container_col_center_one_of_three,
    mapping_dictionary,
)
from dash.dependencies import Input, Output, State

from my_project.tab_data_explorer.charts_data_explorer import (
    custom_heatmap,
    two_var_graph,
    three_var_graph,
)
from my_project.template_graphs import heatmap, yearly_profile, daily_profile, barchart

from app import app

explore_dropdown_names = {}
explore_dropdown_names.update(deepcopy(dropdown_names))
explore_dropdown_names.update(deepcopy(sun_cloud_tab_dropdown_names))
explore_dropdown_names.update(deepcopy(more_variables_dropdown))
explore_dropdown_names.update(deepcopy(sun_cloud_tab_explore_dropdown_names))
explore_dropdown_names.pop("None", None)


def section_one_inputs():
    """Return the inputs from section one."""
    return html.Div(
        className="container-row full-width row-center",
        children=[
            html.H4(className="text-next-to-input", children=["Select a variable: "]),
            dcc.Dropdown(
                id="sec1-var-dropdown",
                options=[
                    {"label": i, "value": explore_dropdown_names[i]}
                    for i in explore_dropdown_names
                ],
                value="DBT",
            ),
        ],
    )


def section_one():
    """Return the graphs for section one"""
    return html.Div(
        className="container-col full-width",
        children=[
            section_one_inputs(),
            html.Div(
                children=title_with_tooltip(
                    text="Yearly chart",
                    tooltip_text=None,
                    id_button="explore-yearly-chart-label",
                ),
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(id="yearly-explore", className="full-width"),
            ),
            html.Div(
                children=title_with_tooltip(
                    text="Daily chart",
                    tooltip_text=None,
                    id_button="explore-daily-chart-label",
                ),
            ),
            dcc.Loading(
                html.Div(className="full-width", id="query-daily"),
                type="circle",
            ),
            html.Div(
                children=title_with_tooltip(
                    text="Heatmap chart",
                    tooltip_text=None,
                    id_button="explore-heatmap-chart-label",
                ),
            ),
            dcc.Loading(
                html.Div(className="full-width", id="query-heatmap"),
                type="circle",
            ),
            html.Div(
                children=title_with_tooltip(
                    text="Descriptive statistics",
                    tooltip_text="count, mean, std, min, max, and percentiles",
                    id_button="table-explore",
                ),
            ),
            html.Div(
                id="table-data-explorer",
            ),
        ],
    )


def section_two_inputs():
    """Return all the input forms from section two."""
    return html.Div(
        children=[
            html.Div(
                children=title_with_tooltip(
                    text="Customizable heatmap",
                    tooltip_text=None,
                    id_button="custom-heatmap-chart-label",
                ),
            ),
            html.Div(
                className="container-row full-width three-inputs-container",
                children=[
                    html.Div(
                        className=container_col_center_one_of_three,
                        children=[
                            html.Div(
                                className=container_row_center_full,
                                children=[
                                    html.H6(
                                        children=["Variable:"],
                                        style={"flex": "30%"},
                                    ),
                                    dcc.Dropdown(
                                        id="sec2-var-dropdown",
                                        options=[
                                            {
                                                "label": i,
                                                "value": explore_dropdown_names[i],
                                            }
                                            for i in explore_dropdown_names
                                        ],
                                        value="RH",
                                        style={"flex": "70%"},
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_col_center_one_of_three,
                        children=[
                            dbc.Button(
                                "Apply month and hour filter",
                                color="primary",
                                id="sec2-time-filter-input",
                                className="mb-2",
                                n_clicks=0,
                            ),
                            html.Div(
                                className="container-row full-width justify-center mt-2",
                                children=[
                                    html.H6("Month Range", style={"flex": "20%"}),
                                    html.Div(
                                        dcc.RangeSlider(
                                            id="sec2-month-slider",
                                            min=1,
                                            max=12,
                                            step=1,
                                            value=[1, 12],
                                            marks={1: "1", 12: "12"},
                                            tooltip={
                                                "always_visible": False,
                                                "placement": "top",
                                            },
                                            allowCross=False,
                                        ),
                                        style={"flex": "50%"},
                                    ),
                                    dcc.Checklist(
                                        options=[
                                            {"label": "Invert", "value": "invert"},
                                        ],
                                        value=[],
                                        id="invert-month-explore-heatmap",
                                        labelStyle={"flex": "30%"},
                                    ),
                                ],
                            ),
                            html.Div(
                                className="container-row justify-center",
                                children=[
                                    html.H6("Hour Range", style={"flex": "20%"}),
                                    html.Div(
                                        dcc.RangeSlider(
                                            id="sec2-hour-slider",
                                            min=1,
                                            max=24,
                                            step=1,
                                            value=[1, 24],
                                            marks={1: "1", 24: "24"},
                                            tooltip={
                                                "always_visible": False,
                                                "placement": "topLeft",
                                            },
                                            allowCross=False,
                                        ),
                                        style={"flex": "50%"},
                                    ),
                                    dcc.Checklist(
                                        options=[
                                            {"label": "Invert", "value": "invert"},
                                        ],
                                        value=[],
                                        id="invert-hour-explore-heatmap",
                                        labelStyle={"flex": "30%"},
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_col_center_one_of_three,
                        children=[
                            dbc.Button(
                                "Apply filter",
                                color="primary",
                                id="sec2-data-filter-input",
                                className="mb-2",
                                n_clicks=0,
                            ),
                            html.Div(
                                className=container_row_center_full,
                                children=[
                                    html.H6(
                                        children=["Filter Variable:"],
                                        style={"flex": "30%"},
                                    ),
                                    dcc.Dropdown(
                                        id="sec2-data-filter-var",
                                        options=[
                                            {
                                                "label": i,
                                                "value": explore_dropdown_names[i],
                                            }
                                            for i in explore_dropdown_names
                                        ],
                                        value="RH",
                                        style={"flex": "70%"},
                                    ),
                                ],
                            ),
                            html.Div(
                                className=container_row_center_full,
                                children=[
                                    html.H6(
                                        children=["Min Value:"], style={"flex": "30%"}
                                    ),
                                    dbc.Input(
                                        id="sec2-min-val",
                                        placeholder="Enter a number for the min val",
                                        type="number",
                                        value=0,
                                        step=1,
                                        style={"flex": "70%"},
                                    ),
                                ],
                            ),
                            html.Div(
                                className=container_row_center_full,
                                children=[
                                    html.H6(
                                        children=["Max Value:"], style={"flex": "30%"}
                                    ),
                                    dbc.Input(
                                        id="sec2-max-val",
                                        placeholder="Enter a number for the max val",
                                        type="number",
                                        value=100,
                                        step=1,
                                        style={"flex": "70%"},
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def section_two():
    """Return the two graphs in section two."""
    return html.Div(
        id="tab6-sec2-container",
        className="container-col justify-center full-width",
        children=[
            section_two_inputs(),
            dcc.Loading(
                type="circle",
                children=html.Div(className="full-width", id="custom-heatmap"),
            ),
            dbc.Checklist(
                options=[
                    {"label": "Normalize", "value": "normal"},
                ],
                value=[],
                id="normalize",
            ),
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(
                        className="full-width", id="custom-summary", config=fig_config
                    ),
                ],
            ),
        ],
    )


def section_three_inputs():
    """"""
    return html.Div(
        className="container-row full-width three-inputs-container",
        children=[
            html.Div(
                className=container_col_center_one_of_three,
                children=[
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(style={"flex": "30%"}, children=["X Variable:"]),
                            dcc.Dropdown(
                                id="tab6-sec3-var-x-dropdown",
                                options=[
                                    {"label": i, "value": explore_dropdown_names[i]}
                                    for i in explore_dropdown_names
                                ],
                                value="DBT",
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(style={"flex": "30%"}, children=["Y Variable:"]),
                            dcc.Dropdown(
                                id="tab6-sec3-var-y-dropdown",
                                options=[
                                    {"label": i, "value": explore_dropdown_names[i]}
                                    for i in explore_dropdown_names
                                ],
                                value="RH",
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(style={"flex": "30%"}, children=["Color By:"]),
                            dcc.Dropdown(
                                id="tab6-sec3-colorby-dropdown",
                                options=[
                                    {"label": i, "value": explore_dropdown_names[i]}
                                    for i in explore_dropdown_names
                                ],
                                value="glob_hor_rad",
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className=container_col_center_one_of_three,
                children=[
                    dbc.Button(
                        "Apply month and hour filter",
                        color="primary",
                        id="tab6-sec3-time-filter-input",
                        className="mb-2",
                        n_clicks=0,
                    ),
                    html.Div(
                        className="container-row full-width justify-center",
                        children=[
                            html.H6("Month Range", style={"flex": "20%"}),
                            html.Div(
                                dcc.RangeSlider(
                                    id="tab6-sec3-query-month-slider",
                                    min=1,
                                    max=12,
                                    step=1,
                                    value=[1, 12],
                                    marks={1: "1", 12: "12"},
                                    tooltip={
                                        "always_visible": False,
                                        "placement": "top",
                                    },
                                    allowCross=False,
                                ),
                                style={"flex": "50%"},
                            ),
                            dcc.Checklist(
                                options=[
                                    {"label": "Invert", "value": "invert"},
                                ],
                                value=[],
                                id="invert-month-explore-more-charts",
                                labelStyle={"flex": "30%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className="container-row full-width justify-center",
                        children=[
                            html.H6("Hour Range", style={"flex": "20%"}),
                            html.Div(
                                dcc.RangeSlider(
                                    id="tab6-sec3-query-hour-slider",
                                    min=1,
                                    max=24,
                                    step=1,
                                    value=[1, 24],
                                    marks={1: "1", 24: "24"},
                                    tooltip={
                                        "always_visible": False,
                                        "placement": "top",
                                    },
                                    allowCross=False,
                                ),
                                style={"flex": "50%"},
                            ),
                            dcc.Checklist(
                                options=[
                                    {"label": "Invert", "value": "invert"},
                                ],
                                value=[],
                                id="invert-hour-explore-more-charts",
                                labelStyle={"flex": "30%"},
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className=container_col_center_one_of_three,
                children=[
                    dbc.Button(
                        "Apply filter",
                        color="primary",
                        id="tab6-sec3-data-filter-input",
                        className="mb-2",
                        n_clicks=0,
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(
                                children=["Filter Variable:"], style={"flex": "30%"}
                            ),
                            dcc.Dropdown(
                                id="tab6-sec3-filter-var-dropdown",
                                options=[
                                    {"label": i, "value": explore_dropdown_names[i]}
                                    for i in explore_dropdown_names
                                ],
                                value="RH",
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(children=["Min Value:"], style={"flex": "30%"}),
                            dbc.Input(
                                className="num-input",
                                id="tab6-sec3-min-val",
                                placeholder="Enter a number for the min val",
                                type="number",
                                step=1,
                                value=0,
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(children=["Max Value:"], style={"flex": "30%"}),
                            dbc.Input(
                                className="num-input",
                                id="tab6-sec3-max-val",
                                placeholder="Enter a number for the max val",
                                type="number",
                                value=100,
                                step=1,
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def section_three():
    """Return the two graphs in section three."""
    return html.Div(
        className="container-col full-width",
        children=[
            html.Div(
                children=title_with_tooltip(
                    text="More charts",
                    tooltip_text=None,
                    id_button="more-charts-label",
                ),
            ),
            section_three_inputs(),
            dcc.Loading(
                html.Div(id="three-var"),
                type="circle",
            ),
            dcc.Loading(
                html.Div(id="two-var"),
                type="circle",
            ),
        ],
    )


def layout_data_explorer():
    """Return the contents of tab six." """
    return html.Div(
        className="continer-col justify-center",
        children=[section_one(), section_two(), section_three()],
    )


@app.callback(
    Output("yearly-explore", "children"),
    # Section One
    [
        Input("df-store", "modified_timestamp"),
        Input("sec1-var-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
def update_tab_yearly(ts, var, global_local, df, meta, si_ip):
    """Update the contents of tab size. Passing in the info from the dropdown and the general info."""

    if df[var].mean() == 99990.0:
        return dbc.Alert(
            """The selected variable is not available,
            the Clima tool could not generate the yearly plot""",
            color="warning",
            className="m-4",
        )
    else:
        custom_inputs = generate_custom_inputs(var)
        units = generate_units(si_ip)
        return dcc.Graph(
            config=generate_chart_name("yearly_explore", meta, custom_inputs, units),
            figure=yearly_profile(df, var, global_local, si_ip),
        )


@app.callback(
    Output("query-daily", "children"),
    [
        Input("df-store", "modified_timestamp"),
        Input("sec1-var-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
def update_tab_daily(ts, var, global_local, df, meta, si_ip):
    """Update the contents of tab size. Passing in the info from the dropdown and the general info."""
    custom_inputs = generate_custom_inputs(var)
    units = generate_units(si_ip)
    return (
        dcc.Graph(
            config=generate_chart_name("daily_explore", meta, custom_inputs, units),
            figure=daily_profile(df, var, global_local, si_ip),
        ),
    )


@app.callback(
    Output("query-heatmap", "children"),
    [
        Input("df-store", "modified_timestamp"),
        Input("sec1-var-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
def update_tab_heatmap(ts, var, global_local, df, meta, si_ip):
    """Update the contents of tab size. Passing in the info from the dropdown and the general info."""
    custom_inputs = generate_custom_inputs(var)
    units = generate_units(si_ip)
    return (
        dcc.Graph(
            config=generate_chart_name("heatmap_explore", meta, custom_inputs, units),
            figure=heatmap(df, var, global_local, si_ip),
        ),
    )


@app.callback(
    [
        Output("custom-heatmap", "children"),
        Output("custom-summary", "style"),
        Output("custom-summary", "figure"),
        Output("normalize", "style"),
    ],
    [
        Input("df-store", "modified_timestamp"),
        Input("sec2-var-dropdown", "value"),
        Input("sec2-time-filter-input", "n_clicks"),
        Input("sec2-data-filter-input", "n_clicks"),
        Input("normalize", "value"),
        Input("global-local-radio-input", "value"),
    ],
    # General
    [
        State("df-store", "data"),
        State("sec2-month-slider", "value"),
        State("sec2-hour-slider", "value"),
        State("sec2-data-filter-var", "value"),
        State("sec2-min-val", "value"),
        State("sec2-max-val", "value"),
        State("meta-store", "data"),
        State("invert-month-explore-heatmap", "value"),
        State("invert-hour-explore-heatmap", "value"),
        State("si-ip-unit-store", "data"),
    ],
)
def update_heatmap(
    ts,
    var,
    time_filter,
    data_filter,
    normalize,
    global_local,
    df,
    month,
    hour,
    filter_var,
    min_val,
    max_val,
    meta,
    invert_month,
    invert_hour,
    si_ip,
):

    start_month, end_month = month
    if invert_month == ["invert"] and (start_month != 1 or end_month != 12):
        month = month[::-1]
    start_hour, end_hour = hour
    if invert_hour == ["invert"] and (start_hour != 1 or end_hour != 24):
        hour = hour[::-1]
    time_filter_info = [time_filter, month, hour]
    data_filter_info = [data_filter, filter_var, min_val, max_val]

    heat_map = custom_heatmap(
        df, global_local, var, time_filter_info, data_filter_info, si_ip
    )

    no_display = {"display": "none"}

    if not heat_map:
        return (
            dbc.Alert(
                "No data is available in this location under these conditions. Please "
                "either change the month and hour filters, or select a wider range for "
                "the filter variable",
                color="danger",
                style={"text-align": "center", "marginTop": "2rem"},
            ),
            no_display,
            {"data": [], "layout": {}, "frames": []},
            no_display,
        )

    if data_filter:
        custom_inputs = generate_custom_inputs_explorer(var, start_month, end_month, start_hour, end_hour, filter_var, min_val, max_val)
        units = generate_units(si_ip)
        return (
            dcc.Graph(
                config=generate_chart_name("heatmap", meta, custom_inputs, units),
                figure=heat_map,
            ),
            {},
            barchart(df, var, time_filter_info, data_filter_info, normalize, si_ip),
            {},
        )
    custom_inputs = f"{var}"
    units = "SI" if si_ip == "si" else "IP" if si_ip == "ip" else None
    return (
        dcc.Graph(
            config=generate_chart_name("heatmap", meta, custom_inputs, units),
            figure=heat_map,
        ),
        no_display,
        {"data": [], "layout": {}, "frames": []},
        no_display,
    )


@app.callback(
    [Output("three-var", "children"), Output("two-var", "children")],
    [
        Input("df-store", "modified_timestamp"),
        Input("tab6-sec3-var-x-dropdown", "value"),
        Input("tab6-sec3-var-y-dropdown", "value"),
        Input("tab6-sec3-colorby-dropdown", "value"),
        Input("tab6-sec3-time-filter-input", "n_clicks"),
        Input("tab6-sec3-data-filter-input", "n_clicks"),
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("tab6-sec3-query-month-slider", "value"),
        State("tab6-sec3-query-hour-slider", "value"),
        State("tab6-sec3-filter-var-dropdown", "value"),
        State("tab6-sec3-min-val", "value"),
        State("tab6-sec3-max-val", "value"),
        State("meta-store", "data"),
        State("invert-month-explore-more-charts", "value"),
        State("invert-hour-explore-more-charts", "value"),
        State("si-ip-unit-store", "data"),
    ],
)
@code_timer
def update_more_charts(
    ts,
    var_x,
    var_y,
    color_by,
    time_filter,
    data_filter,
    global_local,
    df,
    month,
    hour,
    data_filter_var,
    min_val,
    max_val,
    meta,
    invert_month,
    invert_hour,
    si_ip,
):
    """Update the contents of tab size. Passing in the info from the dropdown and the general info."""
    # todo: dont allow to input if apply filter not checked
    # if (min_val3 is None or max_val3 is None) and data_filter3:
    #     raise PreventUpdate

    start_month, end_month = month
    if invert_month == ["invert"] and (start_month != 1 or end_month != 12):
        month = month[::-1]
    start_hour, end_hour = hour
    if invert_hour == ["invert"] and (start_hour != 1 or end_hour != 24):
        hour = hour[::-1]
    time_filter_info = [time_filter, month, hour]
    data_filter_info = [data_filter, data_filter_var, min_val, max_val]
    if data_filter and (min_val is None or max_val is None):
        raise PreventUpdate
    else:
        two = two_var_graph(df, var_x, var_y, si_ip)
        three = three_var_graph(
            df,
            global_local,
            var_x,
            var_y,
            color_by,
            time_filter_info,
            data_filter_info,
            si_ip,
        )
        if not three:
            custom_inputs = f"{var_x}-{var_y}"
            units = generate_units(si_ip)
            return dbc.Alert(
                "No data is available in this location under these conditions. Please "
                "either change the month and hour filters, or select a wider range for "
                "the filter variable",
                color="danger",
                style={"text-align": "center", "marginTop": "2rem"},
            ), dcc.Graph(
                config=generate_chart_name("scatter", meta, custom_inputs, units),
                figure=two,
            )
        else:
            custom_inputs_three = f"{var_x}-{var_y}-{color_by}"
            custom_inputs_two = f"{var_x}-{var_y}"
            units = generate_units(si_ip)
            return dcc.Graph(
                config=generate_chart_name("scatter", meta, custom_inputs_three, units),
                figure=three,
            ), dcc.Graph(
                config=generate_chart_name("scatter", meta, custom_inputs_two, units),
                figure=two,
            )


@app.callback(
    Output("table-data-explorer", "children"),
    [Input("df-store", "modified_timestamp"), Input("sec1-var-dropdown", "value")],
    [State("df-store", "data"), State("si-ip-unit-store", "data")],
)
def update_table(ts, dd_value, df, si_ip):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    return summary_table_tmp_rh_tab(
        df[["month", "hour", dd_value, "month_names"]], dd_value, si_ip
    )
