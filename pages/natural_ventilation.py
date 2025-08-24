
import math

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Output, Input, State, callback

import numpy as np
import plotly.graph_objects as go

from config import PageUrls, DocLinks, PageInfo, UnitSystem
from pages.lib.global_scheme import (
    template,
    mapping_dictionary,
    tight_margins,
    month_lst,
    container_row_center_full,
    container_col_center_one_of_three,
)
from pages.lib.template_graphs import filter_df_by_month_and_hour
from pages.lib.global_column_names import ColNames
from pages.lib.global_elementids import ElementIds
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
    return html.Div(
        className="container-col",
        id=ElementIds.MAIN_NV_SECTION,
        children=[
            #
        ],
    )


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
        html.Div(
            children=title_with_link(
                text="Natural Ventilation Potential",
                id_button="natural-ventilation-label",
                doc_link=DocLinks.NATURAL_VENTILATION,
            ),
        ),
        inputs_tab(tdb_set_min, tdb_set_max, dpt_set),
        dcc.Loading(
            html.Div(
                id=ElementIds.NV_HEATMAP_CHART,
                style={"marginTop": "1rem"},
            ),
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
                    id=ElementIds.SWITCHES_INPUT,
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
                        id_button="nv_normalize",
                    ),
                ),
            ],
        ),
        dcc.Loading(
            html.Div(
                id=ElementIds.NV_BAR_CHART,
                style={"marginTop": "1rem"},
            ),
            type="circle",
        ),
    ]


def inputs_tab(t_min, t_max, d_set):
    return html.Div(
        className="container-row full-width three-inputs-container",
        children=[
            html.Div(
                className=container_col_center_one_of_three,
                children=[
                    dbc.Button(
                        "Apply filter",
                        color="primary",
                        id=ElementIds.NV_DBT_FILTER,
                        className="mb-2",
                        n_clicks=1,
                    ),
                    html.H6("Outdoor dry-bulb air temperature range"),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(children=["Min Value:"], style={"flex": "30%"}),
                            dbc.Input(
                                id=ElementIds.NV_TDB_MIN_VAL,
                                placeholder="Enter a number for the min val",
                                type="number",
                                step=1,
                                value=t_min,
                                style={"flex": "70%"},
                            ),
                        ],
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(children=["Max Value:"], style={"flex": "30%"}),
                            dbc.Input(
                                id=ElementIds.NV_TDB_MAX_VAL,
                                placeholder="Enter a number for the max val",
                                type="number",
                                value=t_max,
                                step=1,
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
                        id=ElementIds.NV_MONTH_HOUR_FILTER,
                        className="mb-2",
                        n_clicks=0,
                    ),
                    html.Div(
                        className="container-row full-width justify-center mt-2",
                        children=[
                            html.H6("Month Range", style={"flex": "20%"}),
                            html.Div(
                                dcc.RangeSlider(
                                    id=ElementIds.NV_MONTH_SLIDER,
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
                                id=ElementIds.INVERT_MONTH_NV,
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
                                    id=ElementIds.NV_HOUR_SLIDER,
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
                                id=ElementIds.INVERT_HOUR_NV,
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
                        id=ElementIds.NV_DPT_FILTER,
                        className="mb-2",
                        n_clicks=0,
                        disabled=True,
                    ),
                    dbc.Checklist(
                        options=[
                            {
                                "label": (
                                    "Avoid condensation with radiant systems: If the"
                                    " outdoor dew point temperature is below the"
                                    " radiant system surface temperature, the data"
                                    " point is not plot."
                                ),
                                "value": 1,
                            },
                        ],
                        value=[],
                        id=ElementIds.ENABLE_CONDENSATION,
                    ),
                    html.Div(
                        className=container_row_center_full,
                        children=[
                            html.H6(
                                children=["Surface temperature:"],
                                style={"marginRight": "1rem"},
                            ),
                            dbc.Input(
                                id=ElementIds.NV_DPT_MAX_VAL,
                                placeholder="Enter a number for the max val",
                                type="number",
                                value=d_set,
                                step=1,
                                style={"flex": "1"},
                            ),
                        ],
                    ),
                ],
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
    # enable or disable button apply filter DPT
    dpt_data_filter = enable_dew_point_data_filter(condensation_enabled)

    start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
        month, hour, invert_month, invert_hour
    )

    var = ColNames.DBT
    filter_var = ColNames.DPT

    if dbt_data_filter and (min_dbt_val <= max_dbt_val):
        df.loc[(df[var] < min_dbt_val) | (df[var] > max_dbt_val), var] = None

    if dpt_data_filter:
        df.loc[(df[filter_var] < -200) | (df[filter_var] > max_dpt_val), var] = None

        if df.dropna(subset=[ColNames.MONTH]).shape[0] == 0:
            return (
                dbc.Alert(
                    "Natural ventilation is not available in this location under these"
                    " conditions. Please either select a different outdoor dry-bulb air"
                    " temperature range, change the month and hour filter, or increase"
                    " thedew-point temperature.",
                    color="danger",
                    style={"text-align": "center", "marginTop": "2rem"},
                ),
            )

    df = filter_df_by_month_and_hour(
        df, time_filter, month, hour, invert_month, invert_hour, var
    )

    var_unit = mapping_dictionary[var][si_ip]["unit"]

    filter_unit = mapping_dictionary[filter_var][si_ip]["unit"]

    var_range = mapping_dictionary[var][si_ip]["range"]

    var_name = mapping_dictionary[var]["name"]

    filter_name = mapping_dictionary[filter_var]["name"]

    var_color = mapping_dictionary[var]["color"]

    if global_local == "global":
        range_z = var_range
    else:
        data_max = 5 * math.ceil(df[var].max() / 5)
        data_min = 5 * math.floor(df[var].min() / 5)
        range_z = [data_min, data_max]

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
            y=df[ColNames.HOUR] - 0.5,  # Offset by 0.5 to center the hour labels
            x=df[ColNames.UTC_TIME].dt.date,
            z=df[var],
            colorscale=var_color,
            zmin=range_z[0],
            zmax=range_z[1],
            connectgaps=False,
            hoverongaps=False,
            customdata=np.stack((df[ColNames.MONTH_NAMES], df[ColNames.DAY]), axis=-1),
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
        config=generate_chart_name("heatmap", meta, custom_inputs, units),
        figure=fig,
    )


@callback(
    Output(ElementIds.NV_BAR_CHART, "children"),
    [
        Input(ElementIds.ID_NATURAL_VENTILATION_DF_STORE, "modified_timestamp"),
        Input(ElementIds.NV_MONTH_HOUR_FILTER, "n_clicks"),
        Input(ElementIds.NV_DBT_FILTER, "n_clicks"),
        Input(ElementIds.NV_DPT_FILTER, "n_clicks"),
        Input(ElementIds.SWITCHES_INPUT, "value"),
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

    var = "DBT"
    filter_var = "DPT"

    var_unit = mapping_dictionary[var][si_ip]["unit"]
    filter_unit = mapping_dictionary[filter_var][si_ip]["unit"]

    var_name = mapping_dictionary[var]["name"]

    filter_name = mapping_dictionary[filter_var]["name"]

    color_in = "dodgerblue"

    df[ColNames.NV_ALLOWED] = 1

    df = filter_df_by_month_and_hour(
        df, time_filter, month, hour, invert_month, invert_hour, "nv_allowed"
    )

    # this should be the total after filtering by time
    tot_month_hours = (
        df.groupby(df[ColNames.UTC_TIME].dt.month)[ColNames.NV_ALLOWED].sum().values
    )

    if dbt_data_filter and (min_dbt_val <= max_dbt_val):
        df.loc[(df[var] < min_dbt_val) | (df[var] > max_dbt_val), ColNames.NV_ALLOWED] = 0

    if dpt_data_filter:
        df.loc[(df[filter_var] > max_dpt_val), ColNames.NV_ALLOWED] = 0

    n_hours_nv_allowed = (
        df.dropna(subset=ColNames.NV_ALLOWED)
        .groupby(df[ColNames.UTC_TIME].dt.month)[ColNames.NV_ALLOWED]
        .sum()
        .values
    )

    per_time_nv_allowed = np.round(100 * (n_hours_nv_allowed / tot_month_hours))

    if len(normalize) == 0:
        fig = go.Figure(
            go.Bar(
                x=df[ColNames.MONTH_NAMES].unique(),
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
            x=df[ColNames.MONTH_NAMES].unique(),
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
        config=generate_chart_name("barchart", meta, custom_inputs, units),
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
