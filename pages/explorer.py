import dash
from dash import dcc
import dash_mantine_components as dmc
from dash_extensions.enrich import Output, Input, State, callback
from dash.exceptions import PreventUpdate

from copy import deepcopy

from config import PageUrls, PageInfo, DocLinks, UnitSystem
from pages.lib.charts_data_explorer import (
    custom_heatmap,
    two_var_graph,
    three_var_graph,
)
from pages.lib.global_element_ids import ElementIds
from pages.lib.global_variables import Variables
from pages.lib.global_id_buttons import IdButtons
from pages.lib.global_tab_names import TabNames
from pages.lib.global_scheme import (
    fig_config,
    dropdown_names,
    sun_cloud_tab_dropdown_names,
    more_variables_dropdown,
    sun_cloud_tab_explore_dropdown_names,
)
from pages.lib.template_graphs import (
    heatmap,
    yearly_profile,
    daily_profile,
    barchart,
    filter_df_by_month_and_hour,
)

from pages.lib.utils import (
    generate_chart_name,
    generate_custom_inputs,
    generate_custom_inputs_explorer,
    generate_units,
    title_with_tooltip,
    summary_table_tmp_rh_tab,
    title_with_link,
    determine_month_and_hour_filter,
    dropdown,
)


dash.register_page(
    __name__,
    name=PageInfo.EXPLORER_NAME,
    path=PageUrls.EXPLORER.value,
    order=PageInfo.EXPLORER_ORDER,
)


explore_dropdown_names = {}
explore_dropdown_names.update(deepcopy(dropdown_names))
explore_dropdown_names.update(deepcopy(sun_cloud_tab_dropdown_names))
explore_dropdown_names.update(deepcopy(more_variables_dropdown))
explore_dropdown_names.update(deepcopy(sun_cloud_tab_explore_dropdown_names))
explore_dropdown_names.pop("None", None)


def layout():
    """Return the contents of tab six."""
    return dmc.Stack(
        p="md",
        children=[*section_one(), section_two(), section_three()],
    )


def section_one_inputs():
    """Return the inputs from section one."""
    return dmc.Group(
        mt="md",
        justify="center",
        children=[
            dmc.Title("Select a variable:", order=5),
            dropdown(
                id=ElementIds.SEC1_VAR_DROPDOWN,
                options=explore_dropdown_names,
                value="DBT",
            ),
        ],
    )


def section_one():
    """Return the graphs for section one"""
    return [
        section_one_inputs(),
        title_with_link(
            text="Yearly chart",
            id_button=IdButtons.EXPLORE_YEARLY_CHART_LABEL,
            doc_link=DocLinks.TEMP_HUMIDITY_EXPLAINED,
        ),
        dmc.Skeleton(
            visible=False, h=450, children=dmc.Paper(id=ElementIds.YEARLY_EXPLORE)
        ),
        title_with_link(
            text="Daily chart",
            id_button=IdButtons.EXPLORE_DAILY_CHART_LABEL,
            doc_link=DocLinks.TEMP_HUMIDITY_EXPLAINED,
        ),
        dmc.Skeleton(
            visible=False, h=450, children=dmc.Paper(id=ElementIds.QUERY_DAILY)
        ),
        title_with_link(
            text="Heatmap chart",
            id_button=IdButtons.EXPLORE_HEATMAP_CHART_LABEL,
            doc_link=DocLinks.TEMP_HUMIDITY_EXPLAINED,
        ),
        dmc.Skeleton(
            visible=False, h=450, children=dmc.Paper(id=ElementIds.QUERY_HEATMAP)
        ),
        title_with_tooltip(
            text="Descriptive statistics",
            tooltip_text="count, mean, std, min, max, and percentiles",
            id_button=IdButtons.TABLE_EXPLORE,
        ),
        # Results table
        dmc.Paper(id=ElementIds.TABLE_DATA_EXPLORER, p="sm"),
    ]


def section_two_inputs():
    """Return all the input forms from section two."""
    return dmc.Stack(
        p="md",
        children=[
            title_with_tooltip(
                text="Customizable heatmap",
                tooltip_text=None,
                id_button=IdButtons.CUSTOM_HEATMAP_CHART_LABEL,
            ),
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        dmc.Group(
                            [
                                dmc.Title("Variable:", order=5),
                                dropdown(
                                    id=ElementIds.SEC2_VAR_DROPDOWN,
                                    options=explore_dropdown_names,
                                    value=Variables.RH.col_name,
                                ),
                            ],
                            align="flex-start",
                        ),
                        span=4,
                    ),
                    dmc.GridCol(
                        dmc.Stack(
                            children=[
                                dmc.Button(
                                    "Apply filter",
                                    id=ElementIds.SEC2_DATA_FILTER_INPUT,
                                    color="blue",
                                    w="50%",
                                ),
                                dmc.Group(
                                    [
                                        dmc.Title("Filter Variable:", order=5),
                                        dropdown(
                                            id=ElementIds.SEC2_DATA_FILTER_VAR,
                                            options=explore_dropdown_names,
                                            value=Variables.RH.col_name,
                                        ),
                                    ],
                                ),
                                dmc.Group(
                                    [
                                        dmc.Title("Min Value:", order=5),
                                        dmc.NumberInput(
                                            id=ElementIds.SEC2_MIN_VAL,
                                            placeholder="Enter a number for the min val",
                                            value=0,
                                        ),
                                    ],
                                ),
                                dmc.Group(
                                    [
                                        dmc.Title("Max Value:", order=5),
                                        dmc.NumberInput(
                                            id=ElementIds.SEC2_MAX_VAL,
                                            placeholder="Enter a number for the max val",
                                            value=100,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        span=8,
                    ),
                ],
            ),
        ],
    )


def section_two():
    """Return the two graphs in section two."""
    return dmc.Stack(
        id=ElementIds.EXPLORER_SEC2_CONTAINER,
        children=[
            section_two_inputs(),
            dcc.Loading(
                type="circle",
                children=dmc.Paper(
                    id=ElementIds.CUSTOM_HEATMAP,
                    p="sm",
                ),
            ),
            dmc.Group(
                children=[
                    dmc.CheckboxGroup(
                        id=ElementIds.NORMALIZE,
                        value=[],
                        children=[
                            dmc.Checkbox(label="Normalize", value="normal"),
                        ],
                    ),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=dmc.Paper(
                    children=dcc.Graph(
                        id=ElementIds.CUSTOM_SUMMARY,
                        config=fig_config,
                    ),
                ),
            ),
        ],
    )


def section_three_inputs():
    return dmc.Grid(
        children=[
            dmc.GridCol(
                dmc.Stack(
                    [
                        dmc.Group(
                            [
                                dmc.Title("X Variable:", order=5),
                                dropdown(
                                    id=ElementIds.EXPLORER_SEC3_VAR_X_DROPDOWN,
                                    options=explore_dropdown_names,
                                    value="DBT",
                                ),
                            ],
                        ),
                        dmc.Group(
                            [
                                dmc.Title("Y Variable:", order=5),
                                dropdown(
                                    id=ElementIds.EXPLORER_SEC3_VAR_Y_DROPDOWN,
                                    options=explore_dropdown_names,
                                    value=Variables.RH.col_name,
                                ),
                            ],
                        ),
                        dmc.Group(
                            [
                                dmc.Title("Color By:", order=5),
                                dropdown(
                                    id=ElementIds.EXPLORER_SEC3_COLORBY_DROPDOWN,
                                    options=explore_dropdown_names,
                                    value="glob_hor_rad",
                                ),
                            ],
                        ),
                    ],
                ),
                span=4,
            ),
            dmc.GridCol(
                dmc.Stack(
                    [
                        dmc.Button(
                            "Apply filter",
                            id=ElementIds.EXPLORER_SEC3_DATA_FILTER_INPUT,
                            color="blue",
                            w="45%",
                        ),
                        dmc.Group(
                            [
                                dmc.Title("Filter Variable:", order=5),
                                dropdown(
                                    id=ElementIds.EXPLORER_SEC3_FILTER_VAR_DROPDOWN,
                                    options=explore_dropdown_names,
                                    value=Variables.RH.col_name,
                                ),
                            ],
                        ),
                        dmc.Group(
                            [
                                dmc.Title("Min Value:", order=5),
                                dmc.NumberInput(
                                    id=ElementIds.EXPLORER_SEC3_MIN_VAL,
                                    placeholder="Enter a number for the min val",
                                    value=0,
                                ),
                            ],
                        ),
                        dmc.Group(
                            [
                                dmc.Title("Max Value:", order=5),
                                dmc.NumberInput(
                                    id=ElementIds.EXPLORER_SEC3_MAX_VAL,
                                    placeholder="Enter a number for the max val",
                                    value=100,
                                ),
                            ],
                        ),
                    ],
                ),
                span=8,
            ),
        ],
    )


def section_three():
    """Return the two graphs in section three."""
    return dmc.Stack(
        children=[
            title_with_tooltip(
                text="More charts",
                tooltip_text=None,
                id_button=IdButtons.MORE_CHARTS_LABEL,
            ),
            section_three_inputs(),
            dcc.Loading(
                type="circle",
                children=dmc.Paper(
                    id=ElementIds.THREE_VAR,
                ),
            ),
            dcc.Loading(
                type="circle",
                children=dmc.Paper(
                    id=ElementIds.TWO_VAR,
                ),
            ),
        ],
    )


@callback(
    Output(ElementIds.YEARLY_EXPLORE, "children"),
    # Section One
    [
        Input(ElementIds.ID_EXPLORER_DF_STORE, "modified_timestamp"),
        Input(ElementIds.SEC1_VAR_DROPDOWN, "value"),
        Input(ElementIds.ID_EXPLORER_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_EXPLORER_DF_STORE, "data"),
        State(ElementIds.ID_EXPLORER_META_STORE, "data"),
        State(ElementIds.ID_EXPLORER_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_yearly(_, var, global_local, global_filter_data, df, meta, si_ip):
    """Update the contents of tab size. Passing in the info from the dropdown and the general info."""

    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        target_columns = [
            var,
            Variables.ADAPTIVE_CMF_80_LOW.col_name,
            Variables.ADAPTIVE_CMF_80_UP.col_name,
            Variables.ADAPTIVE_CMF_90_LOW.col_name,
            Variables.ADAPTIVE_CMF_90_UP.col_name,
            Variables.ADAPTIVE_CMF_RMT.col_name,
        ]
        df = apply_global_month_hour_filter(df, global_filter_data, target_columns)

    if df[var].mean() == 99990.0:
        return dmc.Alert(
            """The selected variable is not available,
            the Clima tool could not generate the yearly plot""",
            color="warning",
            className="m-4",
        )
    else:
        custom_inputs = generate_custom_inputs(var)
        units = generate_units(si_ip)
        return dcc.Graph(
            config=generate_chart_name(
                TabNames.YEARLY_EXPLORE, meta, custom_inputs, units
            ),
            figure=yearly_profile(df, var, global_local, si_ip),
        )


@callback(
    Output(ElementIds.QUERY_DAILY, "children"),
    [
        Input(ElementIds.ID_EXPLORER_DF_STORE, "modified_timestamp"),
        Input(ElementIds.SEC1_VAR_DROPDOWN, "value"),
        Input(ElementIds.ID_EXPLORER_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_EXPLORER_DF_STORE, "data"),
        State(ElementIds.ID_EXPLORER_META_STORE, "data"),
        State(ElementIds.ID_EXPLORER_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_daily(_, var, global_local, global_filter_data, df, meta, si_ip):
    """Update the contents of tab size. Passing in the info from the dropdown and the general info."""
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(df, global_filter_data)

    custom_inputs = generate_custom_inputs(var)
    units = generate_units(si_ip)
    return (
        dcc.Graph(
            config=generate_chart_name(
                TabNames.DAILY_EXPLORE, meta, custom_inputs, units
            ),
            figure=daily_profile(df, var, global_local, si_ip),
        ),
    )


@callback(
    Output(ElementIds.QUERY_HEATMAP, "children"),
    [
        Input(ElementIds.ID_EXPLORER_DF_STORE, "modified_timestamp"),
        Input(ElementIds.SEC1_VAR_DROPDOWN, "value"),
        Input(ElementIds.ID_EXPLORER_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_EXPLORER_DF_STORE, "data"),
        State(ElementIds.ID_EXPLORER_META_STORE, "data"),
        State(ElementIds.ID_EXPLORER_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_heatmap(_, var, global_local, global_filter_data, df, meta, si_ip):
    """Update the contents of tab size. Passing in the info from the dropdown and the general info."""
    """Update the contents of tab size. Passing in the info from the dropdown and the general info."""
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(df, global_filter_data)

    custom_inputs = generate_custom_inputs(var)
    units = generate_units(si_ip)
    return (
        dcc.Graph(
            config=generate_chart_name(
                TabNames.HEATMAP_EXPLORE, meta, custom_inputs, units
            ),
            figure=heatmap(df, var, global_local, si_ip),
        ),
    )


@callback(
    [
        Output(ElementIds.CUSTOM_HEATMAP, "children"),
        Output(ElementIds.CUSTOM_SUMMARY, "style"),
        Output(ElementIds.CUSTOM_SUMMARY, "figure"),
        Output(ElementIds.NORMALIZE, "style"),
    ],
    [
        Input(ElementIds.ID_EXPLORER_DF_STORE, "modified_timestamp"),
        Input(ElementIds.SEC2_VAR_DROPDOWN, "value"),
        Input(ElementIds.SEC2_DATA_FILTER_INPUT, "n_clicks"),
        Input(ElementIds.NORMALIZE, "value"),
        Input(ElementIds.ID_EXPLORER_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    # General
    [
        State(ElementIds.ID_EXPLORER_DF_STORE, "data"),
        State(ElementIds.SEC2_DATA_FILTER_VAR, "value"),
        State(ElementIds.SEC2_MIN_VAL, "value"),
        State(ElementIds.SEC2_MAX_VAL, "value"),
        State(ElementIds.ID_EXPLORER_META_STORE, "data"),
        State(ElementIds.ID_EXPLORER_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_heatmap(
    _,
    var,
    data_filter,
    normalize,
    global_local,
    global_filter_data,
    df,
    filter_var,
    min_val,
    max_val,
    meta,
    si_ip,
):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import (
            apply_global_month_hour_filter,
            get_global_filter_state,
        )

        df = apply_global_month_hour_filter(df, global_filter_data, var)

        filter_state = get_global_filter_state(global_filter_data)
        month_range = filter_state["month_range"]
        hour_range = filter_state["hour_range"]
        invert_month_global = filter_state["invert_month"]
        invert_hour_global = filter_state["invert_hour"]

        start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
            month_range, hour_range, invert_month_global, invert_hour_global
        )
    else:
        # Use default values when global filter is not active
        start_month, end_month, start_hour, end_hour = 1, 12, 0, 24

    data_filter_info = [data_filter, filter_var, min_val, max_val]
    month = [start_month, end_month]
    hour = [start_hour, end_hour]
    time_filter_info = [True, month, hour]

    heat_map = custom_heatmap(
        df, global_local, var, time_filter_info, data_filter_info, si_ip
    )

    no_display = {"display": "none"}

    if not heat_map:
        return (
            dmc.Alert(
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
        custom_inputs = generate_custom_inputs_explorer(
            var,
            start_month,
            end_month,
            start_hour,
            end_hour,
            filter_var,
            min_val,
            max_val,
        )
        units = generate_units(si_ip)
        return (
            dcc.Graph(
                config=generate_chart_name(
                    TabNames.HEATMAP, meta, custom_inputs, units
                ),
                figure=heat_map,
            ),
            {},
            barchart(df, var, time_filter_info, data_filter_info, normalize, si_ip),
            {},
        )
    custom_inputs = f"{var}"

    units = UnitSystem.SI.upper()
    if si_ip == UnitSystem.IP:
        units = UnitSystem.IP.upper()

    return (
        dcc.Graph(
            config=generate_chart_name(TabNames.HEATMAP, meta, custom_inputs, units),
            figure=heat_map,
        ),
        no_display,
        {"data": [], "layout": {}, "frames": []},
        no_display,
    )


@callback(
    [Output(ElementIds.THREE_VAR, "children"), Output(ElementIds.TWO_VAR, "children")],
    [
        Input(ElementIds.ID_EXPLORER_DF_STORE, "modified_timestamp"),
        Input(ElementIds.EXPLORER_SEC3_VAR_X_DROPDOWN, "value"),
        Input(ElementIds.EXPLORER_SEC3_VAR_Y_DROPDOWN, "value"),
        Input(ElementIds.EXPLORER_SEC3_COLORBY_DROPDOWN, "value"),
        Input(ElementIds.EXPLORER_SEC3_DATA_FILTER_INPUT, "n_clicks"),
        Input(ElementIds.ID_EXPLORER_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_EXPLORER_DF_STORE, "data"),
        State(ElementIds.EXPLORER_SEC3_FILTER_VAR_DROPDOWN, "value"),
        State(ElementIds.EXPLORER_SEC3_MIN_VAL, "value"),
        State(ElementIds.EXPLORER_SEC3_MAX_VAL, "value"),
        State(ElementIds.ID_EXPLORER_META_STORE, "data"),
        State(ElementIds.ID_EXPLORER_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_more_charts(
    _,
    var_x,
    var_y,
    color_by,
    data_filter,
    global_local,
    global_filter_data,
    df,
    data_filter_var,
    min_val,
    max_val,
    meta,
    si_ip,
):
    """Update the contents of tab size. Passing in the info from the dropdown and the general info."""
    # todo: dont allow to input if apply filter not checked
    # if (min_val3 is None or max_val3 is None) and data_filter3:
    #     raise PreventUpdate

    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(df, global_filter_data)
    else:
        # Use local filtering when global filter is not active
        df = filter_df_by_month_and_hour(df, True, [1, 12], [0, 24], [], [], df.columns)

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
            data_filter_info,
            si_ip,
        )
        if not three:
            custom_inputs = f"{var_x}-{var_y}"
            units = generate_units(si_ip)
            return dmc.Alert(
                "No data is available in this location under these conditions. Please "
                "either change the month and hour filters, or select a wider range for "
                "the filter variable",
                color="danger",
                style={"text-align": "center", "marginTop": "2rem"},
            ), dcc.Graph(
                config=generate_chart_name(
                    TabNames.SCATTER, meta, custom_inputs, units
                ),
                figure=two,
            )
        else:
            custom_inputs_three = f"{var_x}-{var_y}-{color_by}"
            custom_inputs_two = f"{var_x}-{var_y}"
            units = generate_units(si_ip)
            return dcc.Graph(
                config=generate_chart_name(
                    TabNames.SCATTER, meta, custom_inputs_three, units
                ),
                figure=three,
            ), dcc.Graph(
                config=generate_chart_name(
                    TabNames.SCATTER, meta, custom_inputs_two, units
                ),
                figure=two,
            )


@callback(
    Output(ElementIds.TABLE_DATA_EXPLORER, "children"),
    [
        Input(ElementIds.ID_EXPLORER_DF_STORE, "modified_timestamp"),
        Input(ElementIds.SEC1_VAR_DROPDOWN, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_EXPLORER_DF_STORE, "data"),
        State(ElementIds.ID_EXPLORER_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_table(
    _,
    dd_value,
    global_filter_data,
    df,
    si_ip,
):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        filtered_df = apply_global_month_hour_filter(df, global_filter_data)
        # Filter out the filtered rows to avoid empty columns
        if "_is_filtered" in filtered_df.columns:
            filtered_df = filtered_df[~filtered_df["_is_filtered"]]
    else:
        # Use default values when global filter is not active
        filtered_df = df

    return summary_table_tmp_rh_tab(
        filtered_df[
            [
                Variables.MONTH.col_name,
                Variables.HOUR.col_name,
                dd_value,
                Variables.MONTH_NAMES.col_name,
            ]
        ],
        dd_value,
        si_ip,
    )
