import dash
from dash import dcc
import dash_mantine_components as dmc
from dash_extensions.enrich import Output, Input, State, callback
from pages.lib.global_element_ids import ElementIds

from config import PageUrls, DocLinks, PageInfo
from pages.lib.global_scheme import month_lst
from pages.lib.template_graphs import heatmap, wind_rose
from pages.lib.global_variables import Variables
from pages.lib.global_id_buttons import IdButtons
from pages.lib.global_tab_names import TabNames
from pages.lib.utils import (
    title_with_tooltip,
    generate_chart_name,
    generate_units,
    generate_custom_inputs_time,
    title_with_link,
    dropdown,
)


dash.register_page(
    __name__,
    name=PageInfo.WIND_NAME,
    path=PageUrls.WIND.value,
    order=PageInfo.WIND_ORDER,
)


def sliders():
    """Returns 2 sliders for the hour"""
    return dmc.Stack(
        id=ElementIds.SLIDER_CONTAINER,
        children=[
            dmc.Group(
                children=[
                    dmc.Title("Month Range", order=5),
                    dcc.RangeSlider(
                        id=ElementIds.MONTH_SLIDER,
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
            dmc.Group(
                children=[
                    dmc.Title("Hour Range", order=5),
                    dcc.RangeSlider(
                        id=ElementIds.HOUR_SLIDER,
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
    return dmc.Stack(
        children=[
            title_with_link(
                text="Seasonal Wind Rose",
                id_button=IdButtons.SEASONAL_WIND_ROSE_DOC,
                doc_link=DocLinks.WIND_ROSE,
            ),
            dmc.Grid(
                gutter="md",
                children=[
                    dmc.GridCol(
                        span=6,
                        children=dmc.Stack(
                            children=[
                                dcc.Loading(
                                    type="circle",
                                    children=dmc.Stack(
                                        id=ElementIds.WINTER_WIND_ROSE,
                                    ),
                                ),
                                dmc.Text(id=ElementIds.WINTER_WIND_ROSE_TEXT),
                            ],
                        ),
                    ),
                    dmc.GridCol(
                        span=6,
                        children=dmc.Stack(
                            children=[
                                dcc.Loading(
                                    type="circle",
                                    children=dmc.Stack(
                                        id=ElementIds.SPRING_WIND_ROSE,
                                    ),
                                ),
                                dmc.Text(id=ElementIds.SPRING_WIND_ROSE_TEXT),
                            ],
                        ),
                    ),
                    dmc.GridCol(
                        span=6,
                        children=dmc.Stack(
                            children=[
                                dcc.Loading(
                                    type="circle",
                                    children=dmc.Stack(
                                        id=ElementIds.SUMMER_WIND_ROSE,
                                    ),
                                ),
                                dmc.Text(id=ElementIds.SUMMER_WIND_ROSE_TEXT),
                            ],
                        ),
                    ),
                    dmc.GridCol(
                        span=6,
                        children=dmc.Stack(
                            children=[
                                dcc.Loading(
                                    type="circle",
                                    children=dmc.Stack(
                                        id=ElementIds.FALL_WIND_ROSE,
                                    ),
                                ),
                                dmc.Text(id=ElementIds.FALL_WIND_ROSE_TEXT),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )


def daily_wind_rose():
    """Return the section for the 3 daily wind rose graphs."""
    return dmc.Stack(
        id=ElementIds.WIND_DAILY_CONTAINER,
        children=[
            title_with_link(
                text="Daily Wind Rose",
                id_button=IdButtons.DAILY_ROSE_CHART,
                doc_link=DocLinks.WIND_ROSE,
            ),
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        span=4,
                        children=dmc.Stack(
                            children=[
                                dcc.Loading(
                                    type="circle",
                                    children=dmc.Stack(
                                        id=ElementIds.MORNING_WIND_ROSE,
                                    ),
                                ),
                                dmc.Text(id=ElementIds.MORNING_WIND_ROSE_TEXT),
                            ],
                        ),
                    ),
                    dmc.GridCol(
                        span=4,
                        children=dmc.Stack(
                            children=[
                                dcc.Loading(
                                    type="circle",
                                    children=dmc.Stack(
                                        id=ElementIds.NOON_WIND_ROSE,
                                    ),
                                ),
                                dmc.Text(id=ElementIds.NOON_WIND_ROSE_TEXT),
                            ],
                        ),
                    ),
                    dmc.GridCol(
                        span=4,
                        children=dmc.Stack(
                            children=[
                                dcc.Loading(
                                    type="circle",
                                    children=dmc.Stack(
                                        id=ElementIds.NIGHT_WIND_ROSE,
                                    ),
                                ),
                                dmc.Text(id=ElementIds.NIGHT_WIND_ROSE_TEXT),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )




def layout():
    """Contents in the fifth tab 'Wind'."""
    return dmc.Stack(
        p="md",
        children=[
            title_with_link(
                text="Annual Wind Rose",
                id_button=IdButtons.WIND_ROSE_LABEL,
                doc_link=DocLinks.WIND_ROSE,
            ),
            dcc.Loading(
                type="circle",
                children=dmc.Stack(id=ElementIds.WIND_ROSE),
            ),
            dcc.Loading(
                type="circle",
                children=dmc.Stack(id=ElementIds.WIND_SPEED),
            ),
            dcc.Loading(
                type="circle",
                children=dmc.Stack(id=ElementIds.WIND_DIRECTION),
            ),
            seasonal_wind_rose(),
            daily_wind_rose(),
        ],
    )


@callback(
    Output(ElementIds.WIND_ROSE, "children"),
    [
        Input(ElementIds.ID_WIND_DF_STORE, "modified_timestamp"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_WIND_DF_STORE, "data"),
        State(ElementIds.ID_WIND_META_STORE, "data"),
        State(ElementIds.ID_WIND_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_annual_wind_rose(_, global_filter_data, df, meta, si_ip):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter, get_global_filter_state
        df = apply_global_month_hour_filter(df, global_filter_data, [Variables.WIND_SPEED.col_name, Variables.WIND_DIR.col_name])

        months = [1, 12]
        hours = [1, 24]
    else:
        months = [1, 12]
        hours = [1, 24]

    skip_filter = global_filter_data and global_filter_data.get("filter_active", False)
    annual = wind_rose(df, "", months, hours, True, si_ip, skip_time_filter=skip_filter)

    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name(TabNames.ANNUAL_WIND_ROSE, meta, units),
        figure=annual,
    )


@callback(
    Output(ElementIds.WIND_SPEED, "children"),
    [
        Input(ElementIds.ID_WIND_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_WIND_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_WIND_DF_STORE, "data"),
        State(ElementIds.ID_WIND_META_STORE, "data"),
        State(ElementIds.ID_WIND_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_wind_speed(_, global_local, global_filter_data, df, meta, si_ip):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter
        df = apply_global_month_hour_filter(df, global_filter_data, Variables.WIND_SPEED.col_name)

    speed = heatmap(df, Variables.WIND_SPEED.col_name, global_local, si_ip)
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name(TabNames.WIND_SPEED, meta, units),
        figure=speed,
    )


@callback(
    Output(ElementIds.WIND_DIRECTION, "children"),
    [
        Input(ElementIds.ID_WIND_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_WIND_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_WIND_DF_STORE, "data"),
        State(ElementIds.ID_WIND_META_STORE, "data"),
        State(ElementIds.ID_WIND_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_wind_direction(_, global_local, global_filter_data, df, meta, si_ip):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter
        df = apply_global_month_hour_filter(df, global_filter_data, Variables.WIND_DIR.col_name)

    direction = heatmap(df, Variables.WIND_DIR.col_name, global_local, si_ip)
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name(TabNames.WIND_DIRECTION, meta, units),
        figure=direction,
    )




@callback(
    [
        Output(ElementIds.WINTER_WIND_ROSE, "children"),
        Output(ElementIds.SPRING_WIND_ROSE, "children"),
        Output(ElementIds.SUMMER_WIND_ROSE, "children"),
        Output(ElementIds.FALL_WIND_ROSE, "children"),
        Output(ElementIds.WINTER_WIND_ROSE_TEXT, "children"),
        Output(ElementIds.SPRING_WIND_ROSE_TEXT, "children"),
        Output(ElementIds.SUMMER_WIND_ROSE_TEXT, "children"),
        Output(ElementIds.FALL_WIND_ROSE_TEXT, "children"),
    ],
    [Input(ElementIds.ID_WIND_DF_STORE, "modified_timestamp")],
    [
        State(ElementIds.ID_WIND_DF_STORE, "data"),
        State(ElementIds.ID_WIND_META_STORE, "data"),
        State(ElementIds.ID_WIND_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_seasonal_graphs(_, df, meta, si_ip):
    hours = [1, 24]
    winter_months = [12, 2]
    spring_months = [3, 5]
    summer_months = [6, 8]
    fall_months = [9, 12]

    winter = wind_rose(df, "", winter_months, hours, False, si_ip)
    spring = wind_rose(df, "", spring_months, hours, True, si_ip)
    summer = wind_rose(df, "", summer_months, hours, False, si_ip)
    fall = wind_rose(df, "", fall_months, hours, False, si_ip)

    query_calm_wind = f"{Variables.WIND_SPEED.col_name} == 0"

    winter_df = df.loc[
        (df[Variables.MONTH.col_name] <= winter_months[1])
        | (df[Variables.MONTH.col_name] >= winter_months[0])
    ]
    winter_total_count = winter_df.shape[0]
    winter_calm_count = winter_df.query(query_calm_wind).shape[0]

    spring_df = df.loc[
        (df[Variables.MONTH.col_name] >= spring_months[0])
        & (df[Variables.MONTH.col_name] <= spring_months[1])
    ]
    spring_total_count = spring_df.shape[0]
    spring_calm_count = spring_df.query(query_calm_wind).shape[0]

    summer_df = df.loc[
        (df[Variables.MONTH.col_name] >= summer_months[0])
        & (df[Variables.MONTH.col_name] <= summer_months[1])
    ]
    summer_total_count = summer_df.shape[0]
    summer_calm_count = summer_df.query(query_calm_wind).shape[0]

    fall_df = df.loc[
        (df[Variables.MONTH.col_name] >= fall_months[0])
        & (df[Variables.MONTH.col_name] <= fall_months[1])
    ]
    fall_total_count = fall_df.shape[0]
    fall_calm_count = fall_df.query(query_calm_wind).shape[0]

    def seasonal_chart_caption(month_start, month_end, count, n_calm):
        return (
            f"Observations between the months of {month_start} and {month_end} "
            f"between 01:00 hours and 24:00 hours. "
            f"Selected observations {str(count)} of 8760, or "
            f"{str(int(100 * (count / 8760)))} %. {str(n_calm)} observations have calm winds."
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
            config=generate_chart_name(TabNames.WINTER_WIND_ROSE, meta, units),
            figure=winter,
        ),
        dcc.Graph(
            config=generate_chart_name(TabNames.SPRING_WIND_ROSE, meta, units),
            figure=spring,
        ),
        dcc.Graph(
            config=generate_chart_name(TabNames.SUMMER_WIND_ROSE, meta, units),
            figure=summer,
        ),
        dcc.Graph(
            config=generate_chart_name(TabNames.FALL_WIND_ROSE, meta, units),
            figure=fall,
        ),
        winter_text,
        spring_text,
        summer_text,
        fall_text,
    )


@callback(
    [
        Output(ElementIds.MORNING_WIND_ROSE, "children"),
        Output(ElementIds.NOON_WIND_ROSE, "children"),
        Output(ElementIds.NIGHT_WIND_ROSE, "children"),
        Output(ElementIds.MORNING_WIND_ROSE_TEXT, "children"),
        Output(ElementIds.NOON_WIND_ROSE_TEXT, "children"),
        Output(ElementIds.NIGHT_WIND_ROSE_TEXT, "children"),
    ],
    [
        Input(ElementIds.ID_WIND_DF_STORE, "modified_timestamp"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_WIND_DF_STORE, "data"),
        State(ElementIds.ID_WIND_META_STORE, "data"),
        State(ElementIds.ID_WIND_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_daily_graphs(_, global_filter_data, df, meta, si_ip):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter, get_global_filter_state
        df = apply_global_month_hour_filter(df, global_filter_data, [Variables.WIND_SPEED.col_name, Variables.WIND_DIR.col_name])

        months = [1, 12]
    else:
        months = [1, 12]

    morning_times = [6, 13]
    noon_times = [14, 21]
    night_times = [22, 5]

    morning = wind_rose(df, "", months, morning_times, False, si_ip)
    noon = wind_rose(df, "", months, noon_times, False, si_ip)
    night = wind_rose(df, "", months, night_times, True, si_ip)

    query_calm_wind = f"{Variables.WIND_SPEED.col_name} == 0"

    morning_df = df.loc[
        (df[Variables.HOUR.col_name] >= morning_times[0])
        & (df[Variables.HOUR.col_name] <= morning_times[1])
    ]
    morning_total_count = morning_df.shape[0]
    morning_calm_count = morning_df.query(query_calm_wind).shape[0]

    noon_df = df.loc[
        (df[Variables.HOUR.col_name] >= morning_times[0])
        & (df[Variables.HOUR.col_name] <= morning_times[1])
    ]
    noon_total_count = noon_df.shape[0]
    noon_calm_count = noon_df.query(query_calm_wind).shape[0]

    night_df = df.loc[
        (df[Variables.HOUR.col_name] <= night_times[1])
        | (df[Variables.HOUR.col_name] >= night_times[0])
    ]
    night_total_count = night_df.shape[0]
    night_calm_count = night_df.query(query_calm_wind).shape[0]

    def daily_chart_caption(hour_start, hour_end, count, calm_count):
        return (
            f"Observations between the months of Jan and Dec between "
            f"{str(hour_start)}:00 hours and {str(hour_end)}:00 hours. "
            f"Selected observations {count} of 8760, or "
            f"{str(int(100 * (count / 8760)))}%. {calm_count} observations have calm winds."
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
            config=generate_chart_name(TabNames.MORNING_WIND_ROSE, meta, units),
            figure=morning,
        ),
        dcc.Graph(
            config=generate_chart_name(TabNames.NOON_WIND_ROSE, meta, units),
            figure=noon,
        ),
        dcc.Graph(
            config=generate_chart_name(TabNames.NIGHT_WIND_ROSE, meta, units),
            figure=night,
        ),
        morning_text,
        noon_text,
        night_text,
    )
