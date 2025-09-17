import dash
from dash import dcc
import dash_mantine_components as dmc
from dash_extensions.enrich import Output, Input, State, callback

from copy import deepcopy
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pythermalcomfort import psychrometrics as psy

from config import PageUrls, DocLinks, PageInfo, UnitSystem
from pages.lib.utils import get_max_min_value
from pages.lib.global_element_ids import ElementIds
from pages.lib.global_column_names import ColNames
from pages.lib.global_id_buttons import IdButtons
from pages.lib.global_tab_names import TabNames
from pages.lib.global_scheme import (
    dropdown_names,
    sun_cloud_tab_dropdown_names,
    more_variables_dropdown,
    sun_cloud_tab_explore_dropdown_names,
    template,
    mapping_dictionary,
    tight_margins,
)
from pages.lib.template_graphs import filter_df_by_month_and_hour
from pages.lib.utils import (
    generate_chart_name,
    generate_units,
    generate_custom_inputs_psy,
    determine_month_and_hour_filter,
    title_with_link,
    dropdown,
)


dash.register_page(
    __name__,
    name=PageInfo.PSYCHROMETRIC_NAME,
    path=PageUrls.PSY_CHART.value,
    order=PageInfo.PSYCHROMETRIC_ORDER,
)


psy_dropdown_names = {
    "None": "None",
    "Frequency": "Frequency",
}
psy_dropdown_names.update(deepcopy(dropdown_names))
psy_dropdown_names.update(deepcopy(sun_cloud_tab_dropdown_names))
psy_dropdown_names.update(deepcopy(more_variables_dropdown))
psy_dropdown_names.update(deepcopy(sun_cloud_tab_explore_dropdown_names))
psy_dropdown_names.pop("Elevation", None)
psy_dropdown_names.pop("Azimuth", None)
psy_dropdown_names.pop("Saturation pressure", None)


def inputs():
    """"""
    return dmc.Stack(
        children=[
            dmc.SimpleGrid(
                cols={"base": 1, "md": 3},
                spacing="md",
                children=[
                    dmc.Flex(
                        align="center",
                        mt="md",
                        children=[
                            dmc.Text("Color By:", miw=110),
                            dmc.Stack(
                                flex=1,
                                children=dropdown(
                                    id=ElementIds.PSY_COLOR_BY_DROPDOWN,
                                    options=psy_dropdown_names,
                                    value="Frequency",
                                    persistence=True,
                                    persistence_type="session",
                                ),
                            ),
                        ],
                    ),
                    dmc.Stack(
                        children=[
                            dmc.Button(
                                "Apply month and hour filter",
                                id=ElementIds.MONTH_HOUR_FILTER,
                                variant="filled",
                                color="blue",
                                size="md",
                                fullWidth=True,
                            ),
                            dmc.Flex(
                                children=[
                                    dmc.Text("Month Range", miw=110),
                                    dmc.Stack(
                                        flex=1,
                                        children=dcc.RangeSlider(
                                            id=ElementIds.PSY_MONTH_SLIDER,
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
                                    dcc.Checklist(
                                        id=ElementIds.INVERT_MONTH_PSY,
                                        options=[
                                            {"label": "Invert", "value": "invert"}
                                        ],
                                        value=[],
                                    ),
                                ],
                            ),
                            dmc.Flex(
                                children=[
                                    dmc.Text("Hour Range", miw=110),
                                    dmc.Stack(
                                        flex=1,
                                        children=dcc.RangeSlider(
                                            id=ElementIds.PSY_HOUR_SLIDER,
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
                                    dcc.Checklist(
                                        id=ElementIds.INVERT_HOUR_PSY,
                                        options=[
                                            {"label": "Invert", "value": "invert"}
                                        ],
                                        value=[],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dmc.Stack(
                        children=[
                            dmc.Button(
                                "Apply filter",
                                id=ElementIds.DATA_FILTER,
                                variant="filled",
                                color="blue",
                                size="md",
                                fullWidth=True,
                            ),
                            dmc.Flex(
                                children=[
                                    dmc.Text("Filter Variable:", miw=130),
                                    dmc.Stack(
                                        flex=1,
                                        children=dropdown(
                                            id=ElementIds.PSY_VAR_DROPDOWN,
                                            options=dropdown_names,
                                            value=ColNames.RH,
                                        ),
                                    ),
                                ],
                            ),
                            dmc.Flex(
                                children=[
                                    dmc.Text("Min Value:", miw=130),
                                    dmc.Stack(
                                        flex=1,
                                        children=dmc.NumberInput(
                                            id=ElementIds.PSY_MIN_VAL,
                                            placeholder="Enter a number for the min val",
                                            value=0,
                                            step=1,
                                            size="md",
                                        ),
                                    ),
                                ],
                            ),
                            dmc.Flex(
                                children=[
                                    dmc.Text("Max Value:", miw=130),
                                    dmc.Stack(
                                        flex=1,
                                        children=dmc.NumberInput(
                                            id=ElementIds.PSY_MAX_VAL,
                                            placeholder="Enter a number for the max val",
                                            value=100,
                                            step=1,
                                            size="md",
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def layout():
    return dmc.Stack(
        children=[
            title_with_link(
                text="Psychrometric Chart",
                id_button=IdButtons.PSYCHROMETRIC_CHART_CHART,
                doc_link=DocLinks.PSYCHROMETRIC_CHART,
            ),
            dcc.Loading(
                type="circle",
                children=dmc.Stack(
                    children=[
                        inputs(),
                        dmc.Paper(
                            id=ElementIds.PSYCH_CHART,
                            p="sm",
                        ),
                    ],
                ),
            ),
        ],
    )


# psychrometric chart
@callback(
    Output(ElementIds.PSYCH_CHART, "children"),
    [
        Input(ElementIds.ID_PSY_CHART_DF_STORE, "modified_timestamp"),
        Input(ElementIds.PSY_COLOR_BY_DROPDOWN, "value"),
        Input(ElementIds.MONTH_HOUR_FILTER, "n_clicks"),
        Input(ElementIds.DATA_FILTER, "n_clicks"),
        Input(ElementIds.ID_PSY_CHART_GLOBAL_LOCAL_RADIO_INPUT, "value"),
    ],
    [
        State(ElementIds.ID_PSY_CHART_DF_STORE, "data"),
        State(ElementIds.PSY_MONTH_SLIDER, "value"),
        State(ElementIds.PSY_HOUR_SLIDER, "value"),
        State(ElementIds.PSY_MIN_VAL, "value"),
        State(ElementIds.PSY_MAX_VAL, "value"),
        State(ElementIds.PSY_VAR_DROPDOWN, "value"),
        State(ElementIds.ID_PSY_CHART_META_STORE, "data"),
        State(ElementIds.INVERT_MONTH_PSY, "value"),
        State(ElementIds.INVERT_HOUR_PSY, "value"),
        State(ElementIds.ID_PSY_CHART_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_psych_chart(
    ts,
    colorby_var,
    time_filter,
    data_filter,
    global_local,
    df,
    month,
    hour,
    min_val,
    max_val,
    data_filter_var,
    meta,
    invert_month,
    invert_hour,
    si_ip,
):
    start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
        month, hour, invert_month, invert_hour
    )

    df = filter_df_by_month_and_hour(
        df, time_filter, month, hour, invert_month, invert_hour, df.columns
    )

    if data_filter:
        if min_val <= max_val:
            mask = (df[data_filter_var] < min_val) | (df[data_filter_var] > max_val)
            df[mask] = None
        else:
            mask = (df[data_filter_var] >= max_val) & (df[data_filter_var] <= min_val)
            df[mask] = None

    if df.dropna(subset=[ColNames.MONTH]).shape[0] == 0:
        return (
            dmc.Alert(
                "No data is available in this location under these conditions. Please "
                "either change the month and hour filters, or select a wider range for "
                "the filter variable",
                color="danger",
                style={"text-align": "center", "marginTop": "2rem"},
            ),
        )

    var = colorby_var
    if var == "None":
        var_color = "darkorange"
    elif var == "Frequency":
        var_color = ["rgba(255,255,255,0)", "rgb(0,150,255)", "rgb(0,0,150)"]
    else:
        var_unit = mapping_dictionary[var][si_ip][ColNames.UNIT]

        var_name = mapping_dictionary[var][ColNames.NAME]

        var_color = mapping_dictionary[var][ColNames.COLOR]

    if global_local == "global":
        # Set Global values for Max and minimum
        var_range_x = mapping_dictionary[ColNames.DBT][si_ip][ColNames.RANGE]
        var_range_y = mapping_dictionary[ColNames.HR][si_ip][ColNames.RANGE]

    else:
        # Set maximum and minimum according to data
        data_max, data_min = get_max_min_value(df[ColNames.DBT])
        var_range_x = [data_min, data_max]

        data_max = round(df[ColNames.HR].max(), 4)
        data_min = round(df[ColNames.HR].min(), 4)
        var_range_y = [data_min * 1000, data_max * 1000]

    title = "Psychrometric Chart"

    if colorby_var != "None" and colorby_var != "Frequency":
        title = title + " colored by " + var_name + " (" + var_unit + ")"

    dbt_list = list(range(-60, 60, 1))
    rh_list = list(range(10, 110, 10))

    rh_df = pd.DataFrame()
    for i, rh in enumerate(rh_list):
        hr_list = np.vectorize(psy.psy_ta_rh)(dbt_list, rh)
        hr_df = pd.DataFrame.from_records(hr_list)
        name = "rh" + str(rh)
        rh_df[name] = hr_df[ColNames.HR]

    fig = go.Figure()

    # Add traces
    for i, rh in enumerate(rh_list):
        name = "rh" + str(rh)

        dbt_list_convert = list(dbt_list)
        rh_multiply = list(rh_df[name])

        for k in range(len(rh_df[name])):
            rh_multiply[k] = rh_multiply[k] * 1000

        if si_ip == UnitSystem.IP:
            for j in range(len(dbt_list)):
                dbt_list_convert[j] = dbt_list_convert[j] * 1.8 + 32

        fig.add_trace(
            go.Scatter(
                x=dbt_list_convert,
                y=rh_multiply,
                showlegend=False,
                mode="lines",
                name="",
                hovertemplate="RH " + str(rh) + "%",
                line=dict(width=1, color="lightgrey"),
            )
        )

    df_hr_multiply = list(df[ColNames.HR])
    for k in range(len(df_hr_multiply)):
        df_hr_multiply[k] = df_hr_multiply[k] * 1000
    if var == "None":
        fig.add_trace(
            go.Scatter(
                x=df[ColNames.DBT],
                y=df_hr_multiply,
                showlegend=False,
                mode="markers",
                marker=dict(
                    size=6,
                    color=var_color,
                    showscale=False,
                    opacity=0.2,
                ),
                hovertemplate=mapping_dictionary[ColNames.DBT][ColNames.NAME]
                + ": %{x:.2f}"
                + mapping_dictionary[ColNames.DBT][ColNames.NAME],
                name="",
            )
        )
    elif var == "Frequency":
        fig.add_trace(
            go.Histogram2d(
                x=df[ColNames.DBT],
                y=df_hr_multiply,
                name="",
                colorscale=var_color,
                hovertemplate="",
                autobinx=False,
                xbins=dict(start=-50, end=100, size=1),
            )
        )
        # fig.add_trace(
        #     go.Scatter(
        #         x=dbt_list,
        #         y=rh_df["rh100"],
        #         showlegend=False,
        #         mode="none",
        #         name="",
        #         fill="toself",
        #         fillcolor="#fff",
        #     )
        # )

    else:
        var_colorbar = dict(
            thickness=30,
            title=var_unit + "<br>  ",
        )

        if var_unit == "Thermal stress":
            var_colorbar["tickvals"] = [4, 3, 2, 1, 0, -1, -2, -3, -4, -5]
            var_colorbar["ticktext"] = [
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
            ]

        fig.add_trace(
            go.Scatter(
                x=df[ColNames.DBT],
                y=df_hr_multiply,
                showlegend=False,
                mode="markers",
                marker=dict(
                    size=5,
                    color=df[var],
                    showscale=True,
                    opacity=0.3,
                    colorscale=var_color,
                    colorbar=var_colorbar,
                ),
                customdata=np.stack(
                    (df[ColNames.RH], df["h"], df[var], df["t_dp"]), axis=-1
                ),
                hovertemplate=mapping_dictionary[ColNames.DBT][ColNames.NAME]
                + ": %{x:.2f}"
                + mapping_dictionary[ColNames.DBT][si_ip][ColNames.UNIT]
                + "<br>"
                + mapping_dictionary[ColNames.RH][ColNames.NAME]
                + ": %{customdata[0]:.2f}"
                + mapping_dictionary[ColNames.RH][si_ip][ColNames.UNIT]
                + "<br>"
                + mapping_dictionary["h"][ColNames.NAME]
                + ": %{customdata[1]:.2f}"
                + mapping_dictionary["h"][si_ip][ColNames.UNIT]
                + "<br>"
                + mapping_dictionary["t_dp"][ColNames.NAME]
                + ": %{customdata[3]:.2f}"
                + mapping_dictionary["t_dp"][si_ip][ColNames.UNIT]
                + "<br>"
                + "<br>"
                + var_name
                + ": %{customdata[2]:.2f}"
                + var_unit,
                name="",
            )
        )

    xtitle_name = (
        "Temperature" + "  " + mapping_dictionary[ColNames.DBT][si_ip][ColNames.UNIT]
    )
    ytitle_name = (
        "Humidity Ratio" + "  " + mapping_dictionary[ColNames.HR][si_ip][ColNames.UNIT]
    )
    fig.update_layout(template=template, margin=tight_margins)
    fig.update_xaxes(
        title_text=xtitle_name,
        range=var_range_x,
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )
    fig.update_yaxes(
        title_text=ytitle_name,
        range=var_range_y,
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )
    custom_inputs = generate_custom_inputs_psy(
        start_month,
        end_month,
        start_hour,
        end_hour,
        colorby_var,
        data_filter_var,
        min_val,
        max_val,
    )
    units = generate_units(si_ip)
    return dcc.Graph(
        config=generate_chart_name(TabNames.PSY, meta, custom_inputs, units), figure=fig
    )
