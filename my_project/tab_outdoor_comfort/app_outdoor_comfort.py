from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from my_project.global_scheme import (
    outdoor_dropdown_names,
    tight_margins,
    month_lst,
    container_row_center_full,
    container_col_center_one_of_three,
)
from dash.dependencies import Input, Output, State

from my_project.template_graphs import (
    heatmap_with_filter,
    thermal_stress_stacked_barchart,
)
from my_project.utils import (
    generate_chart_name,
    generate_units_degree,
    generate_units,
    title_with_link,
    title_with_tooltip,
)


import numpy as np
from app import app


def inputs_outdoor_comfort():
    return dbc.Row(
        className="container-row full-width three-inputs-container",
        children=[
            dbc.Col(
                md=6,
                sm=12,
                children=[
                    html.Div(
                        className="container-row center-block",
                        children=[
                            html.H4(
                                children=["Select a scenario:"],
                                style={"flex": "30%"},
                            ),
                            dcc.Dropdown(
                                id="tab7-dropdown",
                                style={
                                    "flex": "60%",
                                },
                                options=[
                                    {
                                        "label": i,
                                        "value": outdoor_dropdown_names[i],
                                    }
                                    for i in outdoor_dropdown_names
                                ],
                                value="utci_Sun_Wind",
                            ),
                            html.Div(id="image-selection", style={"flex": "10%"}),
                        ],
                    ),
                ],
            ),
            dbc.Col(
                md=6,
                sm=12,
                children=[
                    dbc.Button(
                        "Apply month and hour filter",
                        color="primary",
                        style={
                            "width": "100%",
                        },
                        id="month-hour-filter-outdoor-comfort",
                        className="mb-2",
                        n_clicks=0,
                    ),
                    html.Div(
                        className="container-row full-width justify-center mt-2",
                        children=[
                            html.H6("Month Range", style={"flex": "5%"}),
                            html.Div(
                                dcc.RangeSlider(
                                    id="outdoor-comfort-month-slider",
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
                                id="invert-month-outdoor-comfort",
                                labelStyle={"flex": "30%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className="container-row align-center justify-center",
                        children=[
                            html.H6("Hour Range", style={"flex": "5%"}),
                            html.Div(
                                dcc.RangeSlider(
                                    id="outdoor-comfort-hour-slider",
                                    min=0,
                                    max=24,
                                    step=1,
                                    value=[0, 24],
                                    marks={0: "0", 24: "24"},
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
                                id="invert-hour-outdoor-comfort",
                                labelStyle={"flex": "30%"},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def outdoor_comfort_chart():
    return html.Div(
        children=[
            html.Div(id="outdoor-comfort-output"),
            html.Div(
                children=title_with_link(
                    text="UTCI heatmap chart",
                    id_button="utci-charts-label",
                    doc_link="https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/outdoor-comfort/utci-explained",
                )
            ),
            dcc.Loading(
                html.Div(id="utci-heatmap"),
                type="circle",
            ),
            html.Div(
                children=title_with_link(
                    text="UTCI thermal stress chart",
                    id_button="utci-charts-label",
                    doc_link="https://cbe-berkeley.gitbook.io/clima/documentation/tabs-explained/outdoor-comfort/utci-explained",
                )
            ),
            dcc.Loading(
                html.Div(id="utci-category-heatmap"),
                type="circle",
            ),
            html.Div(
                className="container-row align-center justify-center",
                children=[
                    dbc.Checklist(
                        options=[
                            {"label": "", "value": 1},
                        ],
                        value=[1],
                        id="outdoor-comfort-switches-input",
                        switch=True,
                        style={
                            "padding": "1rem",
                            "marginTop": "1rem",
                            "marginRight": "-2rem",
                        },
                    ),
                    html.Div(
                        children=title_with_tooltip(
                            text="Normalize data",
                            tooltip_text=(
                                "If normalized is enabled it calculates the % "
                                "time otherwise it calculates the total number of hours"
                            ),
                            id_button="outdoor-comfort-normalize",
                        ),
                    ),
                ],
            ),
            dcc.Loading(
                html.Div(id="utci-summary-chart"),
                type="circle",
            ),
        ],
    )


def layout_outdoor_comfort():
    return (
        dcc.Loading(
            type="circle",
            children=html.Div(
                className="container-col",
                children=[inputs_outdoor_comfort(), outdoor_comfort_chart()],
            ),
        ),
    )


@app.callback(
    Output("outdoor-comfort-output", "children"),
    [
        Input("df-store", "modified_timestamp"),
    ],
    [
        State("df-store", "data"),
    ],
)
def update_outdoor_comfort_output(ts, df):
    cols = [
        "utci_noSun_Wind_categories",
        "utci_noSun_noWind_categories",
        "utci_Sun_Wind_categories",
        "utci_Sun_noWind_categories",
    ]
    colsWithTheHighestNumberOfZero = []
    highestCount = 0
    for col in cols:
        try:
            count = df[col].value_counts()[0]  # this can cause error if there is no 0
            if count > highestCount:
                highestCount = count
                colsWithTheHighestNumberOfZero.clear()
                colsWithTheHighestNumberOfZero.append(col)
            elif count == highestCount:
                colsWithTheHighestNumberOfZero.append(col)
        except:
            continue
    return f"The Best Weather Condition is: {', '.join(colsWithTheHighestNumberOfZero)}"


@app.callback(
    Output("utci-heatmap", "children"),
    [
        Input("df-store", "modified_timestamp"),
        Input("tab7-dropdown", "value"),
        Input("global-local-radio-input", "value"),
        Input("month-hour-filter-outdoor-comfort", "n_clicks"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
        State("outdoor-comfort-month-slider", "value"),
        State("outdoor-comfort-hour-slider", "value"),
        State("invert-month-outdoor-comfort", "value"),
        State("invert-hour-outdoor-comfort", "value"),
    ],
)
def update_tab_utci_value(
    ts,
    var,
    global_local,
    time_filter,
    df,
    meta,
    si_ip,
    month,
    hour,
    invert_month,
    invert_hour,
):
    custom_inputs = f"{var}"
    units = generate_units_degree(si_ip)
    return dcc.Graph(
        config=generate_chart_name("heatmap", meta, custom_inputs, units),
        figure=heatmap_with_filter(
            df,
            var,
            global_local,
            si_ip,
            time_filter,
            month,
            hour,
            invert_month,
            invert_hour,
            "UTCI heatmap",
        ),
    )


@app.callback(
    Output("image-selection", "children"),
    Input("tab7-dropdown", "value"),
)
def change_image_based_on_selection(value):
    if value == "utci_Sun_Wind":
        source = "./assets/img/sun_and_wind.png"
    elif value == "utci_Sun_noWind":
        source = "./assets/img/sun_no_wind.png"
    elif value == "utci_noSun_Wind":
        source = "./assets/img/no_sun_and_wind.png"
    else:
        source = "./assets/img/no_sun_no_wind.png"

    return html.Img(src=source, height=50)


@app.callback(
    Output("utci-category-heatmap", "children"),
    [
        Input("df-store", "modified_timestamp"),
        Input("tab7-dropdown", "value"),
        Input("global-local-radio-input", "value"),
        Input("month-hour-filter-outdoor-comfort", "n_clicks"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
        State("outdoor-comfort-month-slider", "value"),
        State("outdoor-comfort-hour-slider", "value"),
        State("invert-month-outdoor-comfort", "value"),
        State("invert-hour-outdoor-comfort", "value"),
    ],
)
def update_tab_utci_category(
    ts,
    var,
    global_local,
    time_filter,
    df,
    meta,
    si_ip,
    month,
    hour,
    invert_month,
    invert_hour,
):
    utci_stress_cat = heatmap_with_filter(
        df,
        var + "_categories",
        global_local,
        si_ip,
        time_filter,
        month,
        hour,
        invert_month,
        invert_hour,
        "UTCI thermal stress",
    )
    utci_stress_cat["data"][0]["colorbar"] = dict(
        title="Thermal stress",
        titleside="top",
        tickmode="array",
        tickvals=np.linspace(4.75, -4.75, 10),
        ticktext=[
            "extreme heat stress",
            "very strong heat stress",
            "strong heat stress",
            "moderate heat stress",
            "no thermal stress",
            "slight cold stress",
            "moderate cold stress",
            "strong cold stress",
            "very strong cold stress",
            "extreme cold stress",
        ],
        ticks="outside",
    )
    custom_inputs = f"{var}"
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name("heatmap_category", meta, custom_inputs, units),
        figure=utci_stress_cat,
    )


@app.callback(
    Output("utci-summary-chart", "children"),
    [
        Input("tab7-dropdown", "value"),
        Input("month-hour-filter-outdoor-comfort", "n_clicks"),
        Input("outdoor-comfort-switches-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("outdoor-comfort-month-slider", "value"),
        State("outdoor-comfort-hour-slider", "value"),
        State("meta-store", "data"),
        State("invert-month-outdoor-comfort", "value"),
        State("invert-hour-outdoor-comfort", "value"),
        State("si-ip-unit-store", "data"),
    ],
)
def update_tab_utci_summary_chart(
    var, time_filter, normalize, df, month, hour, meta, invert_month, invert_hour, si_ip
):
    utci_summary_chart = thermal_stress_stacked_barchart(
        df,
        var + "_categories",
        time_filter,
        month,
        hour,
        invert_month,
        invert_hour,
        normalize,
        "UTCI thermal stress distribution",
    )
    custom_inputs = f"{var}"
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name("summary", meta, custom_inputs, units),
        figure=utci_summary_chart,
    )
