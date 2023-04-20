import json
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from my_project.global_scheme import outdoor_dropdown_names, tight_margins, month_lst, container_col_center_one_of_three
from dash.dependencies import Input, Output, State
from my_project.template_graphs import heatmap, thermalStressStackedBarChart
from my_project.utils import title_with_tooltip, generate_chart_name, generate_units_degree, generate_units
import numpy as np
from app import app


def layout_outdoor_comfort():
    return html.Div(
        className="container-col",
        children=[
            html.Div(
                className="container-row full-width three-inputs-container",
                children=[
                    html.Div(
                        className=container_col_center_one_of_three,
                        children=[
                            dbc.Button(
                                "Apply month and hour filter",
                                color="primary",
                                id="month-hour-filter-outdoor-comfort",
                                className="mb-2",
                                n_clicks=0,
                            ),
                            html.Div(
                                className="container-row full-width justify-center mt-2",
                                children=[
                                    html.H6("Month Range", style={"flex": "20%"}),
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
                                    html.H6("Hour Range", style={"flex": "20%"}),
                                    html.Div(
                                        dcc.RangeSlider(
                                            id="outdoor-comfort-hour-slider",
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
                                        id="invert-hour-outdoor-comfort",
                                        labelStyle={"flex": "30%"},
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_col_center_one_of_three,
                        children=[
                            html.Div(
                                className="container-row align-center justify-center",
                                children=[
                                    html.H3(
                                        children=["Select a scenario: "],
                                    ),
                                    dcc.Dropdown(
                                        id="tab7-dropdown",
                                        style={
                                            "width": "25rem",
                                            "marginLeft": "1rem",
                                            "marginRight": "2rem",
                                        },
                                        options=[
                                            {"label": i, "value": outdoor_dropdown_names[i]}
                                            for i in outdoor_dropdown_names
                                        ],
                                        value="utci_Sun_Wind",
                                    ),
                                    html.Div(id="image-selection"),
                                ],
                            )
                        ]
                    )
                ],
            ),
            html.Div(
                children=title_with_tooltip(
                    text="UTCI heatmap chart",
                    tooltip_text=None,
                    id_button="utci-charts-label"
                )
            ),
            dcc.Loading(
                html.Div(id="utci-heatmap"),
                type="circle",
            ),
            html.Div(
                children=title_with_tooltip(
                    text="UTCI thermal stress chart",
                    tooltip_text=None,
                    id_button="utci-charts-label"
                )
            ),
            dcc.Loading(
                html.Div(id="utci-category-heatmap"),
                type="circle",
            ),
            html.Div(
                children=title_with_tooltip(
                    text="UTCI thermal stress distribution chart",
                    tooltip_text=None,
                    id_button="utci-charts-label"
                )
            ),
            dcc.Loading(
                html.Div(id="utci-summary-chart"),
                type="circle",
            ),
        ],
    )


@app.callback(
    Output("utci-heatmap", "children"),
    [
        Input("df-store", "modified_timestamp"),
        Input("tab7-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
def update_tab_utci_value(ts, var, global_local, df, meta, si_ip):
    custom_inputs = f"{var}"
    units = generate_units_degree(si_ip)
    return dcc.Graph(
        config=generate_chart_name("heatmap", meta, custom_inputs, units),
        figure=heatmap(df, var, global_local, si_ip),
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
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
def update_tab_utci_category(ts, var, global_local, df, meta, si_ip):
    utci_stress_cat = heatmap(df, var + "_categories", global_local, si_ip)
    utci_stress_cat["data"][0]["colorbar"] = dict(
        title="Thermal stress",
        titleside="top",
        tickmode="array",
        tickvals = np.linspace(-4.75, 4.75, 10),
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
        Input("df-store", "modified_timestamp"),
        Input("tab7-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [
        State("df-store", "data"),
        State("meta-store", "data"),
        State("si-ip-unit-store", "data"),
    ],
)
def update_tab_utci_summary_chart(ts, var, global_local, df, meta, si_ip):
  
    utci_summary_chart = thermalStressStackedBarChart(df, var + "_categories")
    utci_summary_chart = utci_summary_chart.update_layout(
        margin=tight_margins,
        title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
    )
    utci_summary_chart.update_xaxes(
        dict(tickmode="array", tickvals=np.arange(0, 12, 1), ticktext=month_lst)
    )
    custom_inputs = f"{var}"
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name("summary", meta, custom_inputs, units),
        figure=utci_summary_chart,
    )