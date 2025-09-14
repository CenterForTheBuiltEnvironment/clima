import dash
from dash import dcc, html
import dash_mantine_components as dmc
from dash_extensions.enrich import Output, Input, State, callback

import numpy as np

from config import PageUrls, DocLinks, PageInfo
from pages.lib.global_element_ids import ElementIds
from pages.lib.global_column_names import ColNames
from pages.lib.global_id_buttons import IdButtons
from pages.lib.global_tab_names import TabNames
from pages.lib.global_scheme import (
    outdoor_dropdown_names,
)
from pages.lib.template_graphs import (
    heatmap_with_filter,
    thermal_stress_stacked_barchart,
)
from pages.lib.utils import (
    dropdown,
    generate_chart_name,
    generate_units_degree,
    generate_units,
    title_with_link,
    title_with_tooltip,
)


dash.register_page(
    __name__,
    name=PageInfo.UTCI_NAME,
    path=PageUrls.OUTDOOR.value,
    order=PageInfo.UTCI_ORDER,
)


def inputs_outdoor_comfort():
    return dmc.Grid(
        gutter="md",
        children=[
            dmc.GridCol(
                span=6,
                children=dmc.Grid(
                    gutter="sm",
                    align="center",
                    children=[
                        dmc.GridCol(span=3, children=dmc.Text("Select a scenario:")),
                        dmc.GridCol(
                            span=6,
                            children=dropdown(
                                id=ElementIds.TAB7_DROPDOWN,
                                options=outdoor_dropdown_names,
                                value="utci_Sun_Wind",
                                persistence=True,
                                persistence_type="session",
                            ),
                        ),
                        dmc.GridCol(
                            span=3,
                            children=dmc.Paper(id=ElementIds.IMAGE_SELECTION),
                        ),
                    ],
                ),
            ),
            dmc.GridCol(
                span=6,
                children=dmc.Stack(
                    gap="sm",
                    children=[
                        dmc.Button(
                            "Apply month and hour filter",
                            id=ElementIds.MONTH_HOUR_FILTER_OUTDOOR_COMFORT,
                            variant="filled",
                            color="blue",
                            size="md",
                            radius="md",
                            w="100%",
                        ),
                        dmc.Grid(
                            gutter="sm",
                            align="center",
                            children=[
                                dmc.GridCol(span=2, children=dmc.Text("Month Range")),
                                dmc.GridCol(
                                    span=7,
                                    children=dcc.RangeSlider(
                                        id=ElementIds.OUTDOOR_COMFORT_MONTH_SLIDER,
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
                                ),
                                dmc.GridCol(
                                    span=3,
                                    children=dcc.Checklist(
                                        id=ElementIds.INVERT_MONTH_OUTDOOR_COMFORT,
                                        options=[
                                            {"label": "Invert", "value": "invert"}
                                        ],
                                        value=[],
                                    ),
                                ),
                            ],
                        ),
                        dmc.Grid(
                            gutter="sm",
                            align="center",
                            children=[
                                dmc.GridCol(span=2, children=dmc.Text("Hour Range")),
                                dmc.GridCol(
                                    span=7,
                                    children=dcc.RangeSlider(
                                        id=ElementIds.OUTDOOR_COMFORT_HOUR_SLIDER,
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
                                ),
                                dmc.GridCol(
                                    span=3,
                                    children=dcc.Checklist(
                                        id=ElementIds.INVERT_HOUR_OUTDOOR_COMFORT,
                                        options=[
                                            {"label": "Invert", "value": "invert"}
                                        ],
                                        value=[],
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )


def outdoor_comfort_chart():
    return dmc.Stack(
        w="100%",
        gap="md",
        children=[
            dmc.Paper(
                id=ElementIds.OUTDOOR_COMFORT_OUTPUT,
                radius="md",
                p="sm",
                w="100%",
            ),
            # UTCI heatmap chart
            title_with_link(
                text="UTCI heatmap chart",
                id_button=IdButtons.UTCI_CHARTS_LABEL,
                doc_link=DocLinks.UTCI_CHART,
            ),
            dcc.Loading(
                type="circle",
                children=dmc.Paper(
                    id=ElementIds.UTCI_HEATMAP,
                    radius="md",
                    p="sm",
                    w="100%",
                    h=400,
                ),
            ),
            # UTCI thermal stress chart
            title_with_link(
                text="UTCI thermal stress chart",
                id_button=IdButtons.UTCI_CHARTS_LABEL,
                doc_link=DocLinks.UTCI_CHART,
            ),
            dcc.Loading(
                type="circle",
                children=dmc.Paper(
                    id=ElementIds.UTCI_CATEGORY_HEATMAP,
                    radius="md",
                    p="sm",
                    w="100%",
                    h=400,
                ),
            ),
            # Normalize data
            dmc.Group(
                align="center",
                justify="center",
                gap="sm",
                children=[
                    dmc.Switch(
                        id=ElementIds.OUTDOOR_COMFORT_SWITCHES_INPUT,
                        label="",
                        checked=True,
                        size="md",
                        color="blue",
                    ),
                    title_with_tooltip(
                        text="Normalize data",
                        tooltip_text=(
                            "If normalized is enabled it calculates the % time "
                            "otherwise it calculates the total number of hours"
                        ),
                        id_button=IdButtons.OUTDOOR_COMFORT_NORMALIZE,
                    ),
                ],
            ),
            # Summary chart
            dcc.Loading(
                type="circle",
                children=dmc.Paper(
                    id=ElementIds.UTCI_SUMMARY_CHART,
                    radius="md",
                    p="sm",
                    w="100%",
                ),
            ),
        ],
    )


def layout():
    return dmc.Stack(
        w="100%",
        gap="md",
        children=[
            dcc.Loading(
                type="circle",
                children=dmc.Stack(
                    w="100%",
                    gap="md",
                    children=[
                        inputs_outdoor_comfort(),
                        outdoor_comfort_chart(),
                    ],
                ),
            ),
        ],
    )


@callback(
    Output(ElementIds.OUTDOOR_COMFORT_OUTPUT, "children"),
    [
        Input(ElementIds.ID_OUTDOOR_DF_STORE, "modified_timestamp"),
    ],
    [
        State(ElementIds.ID_OUTDOOR_DF_STORE, "data"),
    ],
)
def update_outdoor_comfort_output(_, df):
    """
    Find the column(s) with the highest number of zero values.

    Args:
        _: Unused callback input.
        df: DataFrame-like object containing UTCI category columns.

    Returns
    -------
    str
        Description of the best weather condition(s).
    """
    cols = [
        ColNames.UTCI_NOSUN_WIND_CATEGORIES,
        ColNames.UTCI_NOSUN_NOWIND_CATEGORIES,
        ColNames.UTCI_SUN_WIND_CATEGORIES,
        ColNames.UTCI_SUN_NOWIND_CATEGORIES,
    ]
    cols_with_the_highest_number_of_zero = []
    highest_count = 0
    for col in cols:
        try:
            count = df[col].value_counts()[0]
        except (KeyError, TypeError):
            # KeyError: 0 not in value_counts; TypeError: df[col] is not valid
            continue
        if count > highest_count:
            highest_count = count
            cols_with_the_highest_number_of_zero.clear()
            cols_with_the_highest_number_of_zero.append(col)
        elif count == highest_count:
            cols_with_the_highest_number_of_zero.append(col)
    return f"The Best Weather Condition is: {', '.join(cols_with_the_highest_number_of_zero)}"


@callback(
    Output(ElementIds.UTCI_HEATMAP, "children"),
    [
        Input(ElementIds.ID_OUTDOOR_DF_STORE, "modified_timestamp"),
        Input(ElementIds.TAB7_DROPDOWN, "value"),
        Input(ElementIds.ID_OUTDOOR_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.MONTH_HOUR_FILTER_OUTDOOR_COMFORT, "n_clicks"),
    ],
    [
        State(ElementIds.ID_OUTDOOR_DF_STORE, "data"),
        State(ElementIds.ID_OUTDOOR_META_STORE, "data"),
        State(ElementIds.ID_OUTDOOR_SI_IP_UNIT_STORE, "data"),
        State(ElementIds.OUTDOOR_COMFORT_MONTH_SLIDER, "value"),
        State(ElementIds.OUTDOOR_COMFORT_HOUR_SLIDER, "value"),
        State(ElementIds.INVERT_MONTH_OUTDOOR_COMFORT, "value"),
        State(ElementIds.INVERT_HOUR_OUTDOOR_COMFORT, "value"),
    ],
)
def update_tab_utci_value(
    _,
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
        config=generate_chart_name(TabNames.HEATMAP, meta, custom_inputs, units),
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


@callback(
    Output(ElementIds.IMAGE_SELECTION, "children"),
    Input(ElementIds.TAB7_DROPDOWN, "value"),
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


@callback(
    Output(ElementIds.UTCI_CATEGORY_HEATMAP, "children"),
    [
        Input(ElementIds.ID_OUTDOOR_DF_STORE, "modified_timestamp"),
        Input(ElementIds.TAB7_DROPDOWN, "value"),
        Input(ElementIds.ID_OUTDOOR_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.MONTH_HOUR_FILTER_OUTDOOR_COMFORT, "n_clicks"),
    ],
    [
        State(ElementIds.ID_OUTDOOR_DF_STORE, "data"),
        State(ElementIds.ID_OUTDOOR_META_STORE, "data"),
        State(ElementIds.ID_OUTDOOR_SI_IP_UNIT_STORE, "data"),
        State(ElementIds.OUTDOOR_COMFORT_MONTH_SLIDER, "value"),
        State(ElementIds.OUTDOOR_COMFORT_HOUR_SLIDER, "value"),
        State(ElementIds.INVERT_MONTH_OUTDOOR_COMFORT, "value"),
        State(ElementIds.INVERT_HOUR_OUTDOOR_COMFORT, "value"),
    ],
)
def update_tab_utci_category(
    _,
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
        config=generate_chart_name(
            TabNames.HEATMAP_CATEGORY, meta, custom_inputs, units
        ),
        figure=utci_stress_cat,
    )


@callback(
    Output(ElementIds.UTCI_SUMMARY_CHART, "children"),
    [
        Input(ElementIds.TAB7_DROPDOWN, "value"),
        Input(ElementIds.MONTH_HOUR_FILTER_OUTDOOR_COMFORT, "n_clicks"),
        Input(ElementIds.OUTDOOR_COMFORT_SWITCHES_INPUT, "checked"),
    ],
    [
        State(ElementIds.ID_OUTDOOR_DF_STORE, "data"),
        State(ElementIds.OUTDOOR_COMFORT_MONTH_SLIDER, "value"),
        State(ElementIds.OUTDOOR_COMFORT_HOUR_SLIDER, "value"),
        State(ElementIds.ID_OUTDOOR_META_STORE, "data"),
        State(ElementIds.INVERT_MONTH_OUTDOOR_COMFORT, "value"),
        State(ElementIds.INVERT_HOUR_OUTDOOR_COMFORT, "value"),
        State(ElementIds.ID_OUTDOOR_SI_IP_UNIT_STORE, "data"),
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
        config=generate_chart_name(TabNames.SUMMARY, meta, custom_inputs, units),
        figure=utci_summary_chart,
    )
