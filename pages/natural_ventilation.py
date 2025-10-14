import dash
from dash import dcc
from dash import no_update
import dash_mantine_components as dmc
from dash_extensions.enrich import Output, Input, State, callback

import numpy as np
import plotly.graph_objects as go

from config import PageUrls, DocLinks, PageInfo, UnitSystem
from pages.lib.global_scheme import (
    template,
    tight_margins,
    month_lst,
)
from pages.lib.template_graphs import filter_df_by_month_and_hour
from pages.lib.global_variables import Variables, VariableInfo
from pages.lib.global_element_ids import ElementIds
from pages.lib.global_id_buttons import IdButtons
from pages.lib.global_tab_names import TabNames
from pages.lib.utils import (
    title_with_tooltip,
    generate_chart_name,
    generate_units_degree,
    generate_units,
    generate_custom_inputs_nv,
    determine_month_and_hour_filter,
    title_with_link,
)


dash.register_page(
    __name__,
    name=PageInfo.NATURAL_VENTILATION_NAME,
    path=PageUrls.NATURAL_VENTILATION.value,
    order=PageInfo.NATURAL_VENTILATION_ORDER,
)


def layout():
    return dmc.Stack(p="md", id=ElementIds.MAIN_NV_SECTION)


@callback(
    Output(ElementIds.MAIN_NV_SECTION, "children"),
    [Input(ElementIds.ID_NATURAL_VENTILATION_SI_IP_RADIO_INPUT, "value")],
)
def update_layout(si_ip):
    if si_ip == UnitSystem.IP:
        tdb_set_min = 50
        tdb_set_max = 75
        dpt_set = 61
    else:
        tdb_set_min = 10
        tdb_set_max = 24
        dpt_set = 16

    return [
        title_with_link(
            text="Natural Ventilation Potential",
            id_button=IdButtons.NATURAL_VENTILATION_LABEL,
            doc_link=DocLinks.NATURAL_VENTILATION,
        ),
        inputs_tab(tdb_set_min, tdb_set_max, dpt_set),
        dcc.Loading(
            type="circle",
            children=dmc.Paper(
                id=ElementIds.NV_HEATMAP_CHART,
            ),
        ),
        dmc.Group(
            justify="center",
            children=[
                dmc.Switch(
                    id=ElementIds.SWITCHES_INPUT,
                    label="",
                    checked=True,
                    color="blue",
                    style={"padding": "1rem", "marginRight": "-2rem"},
                ),
                title_with_tooltip(
                    text="Normalize data",
                    tooltip_text=(
                        "If normalized is enabled it calculates the % "
                        "time otherwise it calculates the total number of hours"
                    ),
                    id_button=IdButtons.NV_NORMALIZE,
                ),
            ],
        ),
        dcc.Loading(
            type="circle",
            children=dmc.Paper(
                id=ElementIds.NV_BAR_CHART,
            ),
        ),
    ]


def inputs_tab(t_min, t_max, d_set):
    return dmc.SimpleGrid(
        cols=3,
        spacing="md",
        children=[
            dmc.Stack(
                [
                    dmc.Button(
                        "Apply filter",
                        color="blue",
                        id=ElementIds.NV_DBT_FILTER,
                        variant="link",
                        n_clicks=1,
                    ),
                    dmc.Title("Outdoor dry-bulb air temperature range", order=5),
                    dmc.Group(
                        [
                            dmc.Title("Min Value:", order=5),
                            dmc.Stack(
                                dmc.NumberInput(
                                    id=ElementIds.NV_TDB_MIN_VAL,
                                    placeholder="Enter a number for the min val",
                                    step=1,
                                    value=t_min,
                                ),
                                flex=1,
                            ),
                        ],
                    ),
                    dmc.Group(
                        [
                            dmc.Title("Max Value:", order=5),
                            dmc.Stack(
                                dmc.NumberInput(
                                    id=ElementIds.NV_TDB_MAX_VAL,
                                    placeholder="Enter a number for the max val",
                                    value=t_max,
                                    step=1,
                                ),
                                flex=1,
                            ),
                        ],
                    ),
                ]
            ),
            dmc.Stack(
                [
                    dmc.Button(
                        "Apply month and hour filter",
                        color="blue",
                        id=ElementIds.NV_MONTH_HOUR_FILTER,
                        variant="link",
                    ),
                    dmc.Group(
                        [
                            dmc.Title("Month Range", order=5),
                            dmc.Stack(
                                dcc.RangeSlider(
                                    id=ElementIds.NV_MONTH_SLIDER,
                                    min=1,
                                    max=12,
                                    step=1,
                                    value=[1, 12],
                                    marks={1: "1", 12: "12"},
                                ),
                                flex=1,
                            ),
                            dcc.Checklist(
                                options=[{"label": "Invert", "value": "invert"}],
                                value=[],
                                id=ElementIds.INVERT_MONTH_NV,
                            ),
                        ],
                    ),
                    dmc.Group(
                        [
                            dmc.Title("Hour Range", order=5),
                            dmc.Stack(
                                dcc.RangeSlider(
                                    id=ElementIds.NV_HOUR_SLIDER,
                                    min=0,
                                    max=24,
                                    step=1,
                                    value=[0, 24],
                                    marks={0: "0", 24: "24"},
                                ),
                                flex=1,
                            ),
                            dcc.Checklist(
                                options=[{"label": "Invert", "value": "invert"}],
                                value=[],
                                id=ElementIds.INVERT_HOUR_NV,
                            ),
                        ],
                    ),
                ]
            ),
            dmc.Stack(
                [
                    dmc.Button(
                        "Apply filter",
                        color="blue",
                        id=ElementIds.NV_DPT_FILTER,
                        variant="link",
                        disabled=True,
                    ),
                    dcc.Checklist(
                        options=[
                            {
                                "label": (
                                    "Avoid condensation with radiant systems: If the "
                                    "outdoor dew point temperature is below the radiant "
                                    "system surface temperature, the data point is not plot."
                                ),
                                "value": 1,
                            }
                        ],
                        value=[],
                        id=ElementIds.ENABLE_CONDENSATION,
                    ),
                    dmc.Group(
                        [
                            dmc.Title("Surface temperature:", order=5),
                            dmc.Stack(
                                dmc.NumberInput(
                                    id=ElementIds.NV_DPT_MAX_VAL,
                                    placeholder="Enter a number for the max val",
                                    value=d_set,
                                    step=1,
                                ),
                                flex=1,
                            ),
                        ],
                    ),
                ]
            ),
        ],
    )


@callback(
    Output(ElementIds.NV_HEATMAP_CHART, "children"),
    [
        Input(ElementIds.ID_NATURAL_VENTILATION_DF_STORE, "modified_timestamp"),
        Input(ElementIds.NV_MONTH_HOUR_FILTER, "n_clicks"),
        Input(ElementIds.NV_DBT_FILTER, "n_clicks"),
        Input(ElementIds.NV_DPT_FILTER, "n_clicks"),
        Input(ElementIds.ID_NATURAL_VENTILATION_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.ENABLE_CONDENSATION, "value"),
    ],
    [
        State(ElementIds.ID_NATURAL_VENTILATION_DF_STORE, "data"),
        State(ElementIds.NV_MONTH_SLIDER, "value"),
        State(ElementIds.NV_HOUR_SLIDER, "value"),
        State(ElementIds.NV_TDB_MIN_VAL, "value"),
        State(ElementIds.NV_TDB_MAX_VAL, "value"),
        State(ElementIds.NV_DPT_MAX_VAL, "value"),
        State(ElementIds.ID_NATURAL_VENTILATION_META_STORE, "data"),
        State(ElementIds.INVERT_MONTH_NV, "value"),
        State(ElementIds.INVERT_HOUR_NV, "value"),
        State(ElementIds.ID_NATURAL_VENTILATION_SI_IP_UNIT_STORE, "data"),
    ],
)
def nv_heatmap(
    ts,
    time_filter,
    dbt_data_filter,
    click_dpt_filter,
    global_local,
    condensation_enabled,
    df,
    month,
    hour,
    min_dbt_val,
    max_dbt_val,
    max_dpt_val,
    meta,
    invert_month,
    invert_hour,
    si_ip,
):
    if df is None:
        return no_update
    # enable or disable button apply filter DPT
    dpt_data_filter = enable_dew_point_data_filter(condensation_enabled)

    start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
        month, hour, invert_month, invert_hour
    )

    var = Variables.DBT.col_name
    filter_var = Variables.DPT.col_name

    if dbt_data_filter and (min_dbt_val <= max_dbt_val):
        df.loc[(df[var] < min_dbt_val) | (df[var] > max_dbt_val), var] = None

    if dpt_data_filter:
        df.loc[(df[filter_var] < -200) | (df[filter_var] > max_dpt_val), var] = None

        if df.dropna(subset=[Variables.MONTH.col_name]).shape[0] == 0:
            return (
                dmc.Alert(
                    title="Notice",
                    color="red",
                    children=(
                        "Natural ventilation is not available in this location under these "
                        "conditions. Please either select a different outdoor dry-bulb air "
                        "temperature range, change the month and hour filter, or increase "
                        "the dew-point temperature."
                    ),
                    style={"text-align": "center", "marginTop": "2rem"},
                ),
            )

    df = filter_df_by_month_and_hour(
        df, time_filter, month, hour, invert_month, invert_hour, var
    )

    variable = VariableInfo.from_col_name(var)
    filter = VariableInfo.from_col_name(filter_var)

    var_unit = variable.get_unit(si_ip)

    filter_unit = filter.get_unit(si_ip)

    var_name = variable.get_name()

    filter_name = filter.get_name()

    var_color = variable.get_color()

    if si_ip == UnitSystem.IP:
        range_z = [32.0, 86.0]
    else:
        range_z = [0.0, 30.0]

    title = (
        f"Hours when the {var_name} is in the range {min_dbt_val} to"
        f" {max_dbt_val} {var_unit}"
    )

    if time_filter:
        title += (
            f" between the months of {month_lst[start_month - 1]} and "
            f"{month_lst[end_month - 1]}<br>and between the hours {start_hour}"
            f":00 and {end_hour}:00"
        )
    if dpt_data_filter:
        title += f" and when the {filter_name} is below {max_dpt_val} {filter_unit}."

    fig = go.Figure(
        data=go.Heatmap(
            y=df[Variables.HOUR.col_name]
            - 0.5,  # Offset by 0.5 to center the hour labels
            x=df[Variables.UTC_TIME.col_name].dt.date,
            z=df[var],
            colorscale=var_color,
            zmin=range_z[0],
            zmax=range_z[1],
            connectgaps=False,
            hoverongaps=False,
            customdata=np.stack(
                (df[Variables.MONTH_NAMES.col_name], df[Variables.DAY.col_name]),
                axis=-1,
            ),
            hovertemplate=(
                "<b>"
                + var
                + ": %{z:.2f} "
                + var_unit
                + "</b><br>"
                + "Month: %{customdata[0]}<br>"
                + "Day: %{customdata[1]}<br>"
                + "Hour: %{y}:00<br>"
            ),
            colorbar=dict(title=var_unit),
            name="",
        )
    )

    fig.update_layout(
        template=template,
        title=title,
        yaxis_nticks=13,
        yaxis=dict(range=(0, 24)),
        margin=tight_margins.copy().update({"t": 55}),
    )

    fig.update_xaxes(
        dtick="M1",
        tickformat="%b",
        ticklabelmode="period",
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
        title_text="Day",
    )
    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
        title_text="Hour",
    )
    custom_inputs = generate_custom_inputs_nv(
        start_month, end_month, start_hour, end_hour, min_dbt_val, max_dbt_val
    )
    units = generate_units_degree(si_ip)
    return dcc.Graph(
        config=generate_chart_name(TabNames.HEATMAP, meta, custom_inputs, units),
        figure=fig,
    )


@callback(
    Output(ElementIds.NV_BAR_CHART, "children"),
    [
        Input(ElementIds.ID_NATURAL_VENTILATION_DF_STORE, "modified_timestamp"),
        Input(ElementIds.NV_MONTH_HOUR_FILTER, "n_clicks"),
        Input(ElementIds.NV_DBT_FILTER, "n_clicks"),
        Input(ElementIds.NV_DPT_FILTER, "n_clicks"),
        Input(ElementIds.ID_NATURAL_VENTILATION_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.SWITCHES_INPUT, "checked"),
        Input(ElementIds.ENABLE_CONDENSATION, "value"),
    ],
    [
        State(ElementIds.ID_NATURAL_VENTILATION_DF_STORE, "data"),
        State(ElementIds.NV_MONTH_SLIDER, "value"),
        State(ElementIds.NV_HOUR_SLIDER, "value"),
        State(ElementIds.NV_TDB_MIN_VAL, "value"),
        State(ElementIds.NV_TDB_MAX_VAL, "value"),
        State(ElementIds.NV_DPT_MAX_VAL, "value"),
        State(ElementIds.ID_NATURAL_VENTILATION_META_STORE, "data"),
        State(ElementIds.INVERT_MONTH_NV, "value"),
        State(ElementIds.INVERT_HOUR_NV, "value"),
        State(ElementIds.ID_NATURAL_VENTILATION_SI_IP_UNIT_STORE, "data"),
    ],
)
def nv_bar_chart(
    ts,
    time_filter,
    dbt_data_filter,
    click_dpt_filter,
    global_local,
    normalize,
    condensation_enabled,
    df,
    month,
    hour,
    min_dbt_val,
    max_dbt_val,
    max_dpt_val,
    meta,
    invert_month,
    invert_hour,
    si_ip,
):
    # enable or disable button apply filter DPT
    dpt_data_filter = enable_dew_point_data_filter(condensation_enabled)

    start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
        month, hour, invert_month, invert_hour
    )

    var = Variables.DBT.col_name
    filter_var = Variables.DPT.col_name

    variable = VariableInfo.from_col_name(var)
    filter = VariableInfo.from_col_name(filter_var)

    var_unit = variable.get_unit(si_ip)
    filter_unit = filter.get_unit(si_ip)

    var_name = variable.get_name()

    filter_name = filter.get_name()

    color_in = "dodgerblue"

    df[Variables.NV_ALLOWED.col_name] = 1

    df = filter_df_by_month_and_hour(
        df, time_filter, month, hour, invert_month, invert_hour, "nv_allowed"
    )

    # this should be the total after filtering by time
    tot_month_hours = (
        df.groupby(df[Variables.UTC_TIME.col_name].dt.month)[
            Variables.NV_ALLOWED.col_name
        ]
        .sum()
        .values
    )

    if dbt_data_filter and (min_dbt_val <= max_dbt_val):
        df.loc[
            (df[var] < min_dbt_val) | (df[var] > max_dbt_val),
            Variables.NV_ALLOWED.col_name,
        ] = 0

    if dpt_data_filter:
        df.loc[(df[filter_var] > max_dpt_val), Variables.NV_ALLOWED.col_name] = 0

    n_hours_nv_allowed = (
        df.dropna(subset=Variables.NV_ALLOWED.col_name)
        .groupby(df[Variables.UTC_TIME.col_name].dt.month)[
            Variables.NV_ALLOWED.col_name
        ]
        .sum()
        .values
    )

    per_time_nv_allowed = np.round(100 * (n_hours_nv_allowed / tot_month_hours))

    if not normalize:
        fig = go.Figure(
            go.Bar(
                x=df[Variables.MONTH_NAMES.col_name].unique(),
                y=n_hours_nv_allowed,
                name="",
                marker_color=color_in,
                customdata=np.stack((n_hours_nv_allowed, per_time_nv_allowed), axis=-1),
                hovertemplate=(
                    "natural ventilation possible for: <br>%{customdata[0]} hrs or"
                    " <br>%{customdata[1]}% of selected time<br>"
                ),
            )
        )

        title = (
            f"Number of hours the {var_name}"
            + f" is in the range {min_dbt_val}"
            + " to "
            + f" {max_dbt_val} {var_unit}"
        )
        fig.update_yaxes(title_text="hours", range=[0, 744])

    else:
        trace1 = go.Bar(
            x=df[Variables.MONTH_NAMES.col_name].unique(),
            y=per_time_nv_allowed,
            name="",
            marker_color=color_in,
            customdata=np.stack((n_hours_nv_allowed, per_time_nv_allowed), axis=-1),
            hovertemplate=(
                "natural ventilation possible for: <br>%{customdata[0]} hrs or <br>%{"
                "customdata[1]}% of selected time<br>"
            ),
        )

        fig = go.Figure(data=trace1)

        title = (
            f"Percentage of hours the {var_name}"
            + f" is in the range {min_dbt_val}"
            + f" to {max_dbt_val}"
            + f" {var_unit}"
        )
        fig.update_yaxes(title_text="Percentage (%)", range=[0, 100])

    if time_filter:
        title += (
            f" between the months of {month_lst[start_month - 1]} and "
            f"{month_lst[end_month - 1]} and between<br>the hours {start_hour}"
            f":00 and {end_hour}:00"
        )
    if dpt_data_filter:
        title += f" when the {filter_name} is below {max_dpt_val} {filter_unit}."

    fig.update_layout(
        template=template,
        title=title,
        barnorm="",
        dragmode=False,
        margin=tight_margins.copy().update({"t": 55}),
    )

    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    custom_inputs = generate_custom_inputs_nv(
        start_month, end_month, start_hour, end_hour, min_dbt_val, max_dbt_val
    )
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name(TabNames.BARCHART, meta, custom_inputs, units),
        figure=fig,
    )


@callback(
    Output(ElementIds.NV_DPT_FILTER, "disabled"),
    Input(ElementIds.ENABLE_CONDENSATION, "value"),
)
def enable_disable_button_data_filter(state_checklist):
    if len(state_checklist) == 1:
        return False
    else:
        return True


def enable_dew_point_data_filter(condensation_enabled):
    if len(condensation_enabled) == 1:
        return True
    else:
        return False
