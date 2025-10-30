import dash
from dash import dcc, html
import dash_mantine_components as dmc
from dash_extensions.enrich import Output, Input, State, callback

import numpy as np

from config import PageUrls, DocLinks, PageInfo
from pages.lib.global_element_ids import ElementIds
from pages.lib.global_variables import Variables
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
from pages.lib.utils import get_time_filter_from_store


dash.register_page(
    __name__,
    name=PageInfo.UTCI_NAME,
    path=PageUrls.OUTDOOR.value,
    order=PageInfo.UTCI_ORDER,
)


def inputs_outdoor_comfort():
    return dmc.Group(
        [
            dmc.Title("Select a scenario:", order=5),
            dropdown(
                id=ElementIds.OUTDOOR_DROPDOWN,
                options=outdoor_dropdown_names,
                value="utci_Sun_Wind",
                persistence=True,
                persistence_type="session",
            ),
            dmc.Paper(id=ElementIds.IMAGE_SELECTION),
        ],
        gap="xs",
        justify="center",
    )


def outdoor_comfort_chart():
    return dmc.Stack(
        children=[
            dmc.Title(id=ElementIds.OUTDOOR_COMFORT_OUTPUT, order=4),
            title_with_link(
                text="UTCI heatmap chart",
                id_button=IdButtons.UTCI_CHARTS_LABEL,
                doc_link=DocLinks.UTCI_CHART,
            ),
            dcc.Loading(
                type="circle",
                children=dmc.Paper(
                    id=ElementIds.UTCI_HEATMAP,
                ),
            ),
            title_with_link(
                text="UTCI thermal stress chart",
                id_button=IdButtons.UTCI_CHARTS_LABEL,
                doc_link=DocLinks.UTCI_CHART,
            ),
            dcc.Loading(
                type="circle",
                children=dmc.Paper(
                    id=ElementIds.UTCI_CATEGORY_HEATMAP,
                ),
            ),
            dmc.Group(
                justify="center",
                children=[
                    dmc.Switch(
                        id=ElementIds.OUTDOOR_COMFORT_SWITCHES_INPUT,
                        checked=True,
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
            dcc.Loading(
                type="circle",
                children=dmc.Paper(
                    id=ElementIds.UTCI_SUMMARY_CHART,
                    # p="sm",
                ),
            ),
        ],
    )


def layout():
    return dmc.Stack(
        p="md",
        children=[
            dcc.Loading(
                type="circle",
                children=dmc.Stack(
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
        Variables.UTCI_NOSUN_WIND_CATEGORIES.col_name,
        Variables.UTCI_NOSUN_NOWIND_CATEGORIES.col_name,
        Variables.UTCI_SUN_WIND_CATEGORIES.col_name,
        Variables.UTCI_SUN_NOWIND_CATEGORIES.col_name,
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

    # Convert column names to display names using string replacement
    display_names = []
    for col in cols_with_the_highest_number_of_zero:
        # Remove utci_ prefix and replace all underscores with spaces
        display_name = col.replace("utci_", "UTCI ")
        display_name = display_name.replace("_", " ")
        display_name = display_name.replace("categories", "Categories")
        # Fix specific words that need spaces
        display_name = display_name.replace("noSun", "No Sun")
        display_name = display_name.replace("noWind", "No Wind")
        display_name = display_name.replace("Sun", "Sun")  # Keep Sun as is
        display_name = display_name.replace("Wind", "Wind")  # Keep Wind as is
        display_names.append(display_name)

    return f"The Best Weather Condition is: {', '.join(display_names)}"


@callback(
    Output(ElementIds.UTCI_HEATMAP, "children"),
    [
        Input(ElementIds.ID_OUTDOOR_DF_STORE, "modified_timestamp"),
        Input(ElementIds.OUTDOOR_DROPDOWN, "value"),
        Input(ElementIds.ID_OUTDOOR_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_OUTDOOR_DF_STORE, "data"),
        State(ElementIds.ID_OUTDOOR_META_STORE, "data"),
        State(ElementIds.ID_OUTDOOR_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_utci_value(
    _,
    var,
    global_local,
    global_filter_data,
    df,
    meta,
    si_ip,
):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(df, global_filter_data, var)

    # Normalize filter state (handles inactive case with defaults)
    time_filter, month, hour, invert_month, invert_hour = get_time_filter_from_store(
        global_filter_data if global_filter_data else None
    )

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
    Input(ElementIds.OUTDOOR_DROPDOWN, "value"),
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
        Input(ElementIds.OUTDOOR_DROPDOWN, "value"),
        Input(ElementIds.ID_OUTDOOR_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_OUTDOOR_DF_STORE, "data"),
        State(ElementIds.ID_OUTDOOR_META_STORE, "data"),
        State(ElementIds.ID_OUTDOOR_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_utci_category(
    _,
    var,
    global_local,
    global_filter_data,
    df,
    meta,
    si_ip,
):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(
            df, global_filter_data, [var, var + "_categories"]
        )

    time_filter, month, hour, invert_month, invert_hour = get_time_filter_from_store(
        global_filter_data if global_filter_data else None
    )

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
    colorbar_index = 1 if len(utci_stress_cat["data"]) > 1 else 0

    utci_stress_cat["data"][colorbar_index]["colorbar"] = dict(
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
        Input(ElementIds.OUTDOOR_DROPDOWN, "value"),
        Input(ElementIds.OUTDOOR_COMFORT_SWITCHES_INPUT, "checked"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_OUTDOOR_DF_STORE, "data"),
        State(ElementIds.ID_OUTDOOR_META_STORE, "data"),
        State(ElementIds.ID_OUTDOOR_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_utci_summary_chart(var, normalize, global_filter_data, df, meta, si_ip):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(df, global_filter_data, var)

    # Unified filter state for both active and inactive cases
    time_filter, month, hour, invert_month, invert_hour = get_time_filter_from_store(
        global_filter_data if global_filter_data else None
    )

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
