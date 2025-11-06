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
from pages.lib.utils import get_max_min_value, separate_filtered_data
from pages.lib.global_element_ids import ElementIds
from pages.lib.global_variables import Variables, VariableInfo
from pages.lib.global_id_buttons import IdButtons
from pages.lib.global_tab_names import TabNames
from pages.lib.global_scheme import (
    dropdown_names,
    sun_cloud_tab_dropdown_names,
    more_variables_dropdown,
    sun_cloud_tab_explore_dropdown_names,
    template,
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


def _safe_get_column(df, column_name, default_value=0):
    if column_name in df.columns:
        return df[column_name]
    else:
        return [default_value] * len(df)


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
    return dmc.Grid(
        justify="center",
        children=[
            dmc.GridCol(
                [
                    dmc.Title("Color By:", order=5),
                    dropdown(
                        id=ElementIds.PSY_COLOR_BY_DROPDOWN,
                        options=psy_dropdown_names,
                        value="Frequency",
                        persistence=True,
                        persistence_type="session",
                    ),
                ],
                span={"base": 12, "md": 4},
            ),
            dmc.GridCol(
                dmc.Stack(
                    [
                        dmc.Group(
                            [
                                dmc.Title("Filter Variable:", order=5),
                                dropdown(
                                    id=ElementIds.PSY_VAR_DROPDOWN,
                                    options=dropdown_names,
                                    value=Variables.RH.col_name,
                                ),
                            ],
                        ),
                        dmc.Group(
                            [
                                dmc.Title("Min Value:", order=5),
                                dmc.NumberInput(
                                    id=ElementIds.PSY_MIN_VAL,
                                    placeholder="Enter a number for the min val",
                                    value=0,
                                    step=1,
                                ),
                            ],
                        ),
                        dmc.Group(
                            [
                                dmc.Title("Max Value:", order=5),
                                dmc.NumberInput(
                                    id=ElementIds.PSY_MAX_VAL,
                                    placeholder="Enter a number for the max val",
                                    value=100,
                                    step=1,
                                ),
                            ],
                        ),
                        dmc.Button(
                            "Apply filter",
                            id=ElementIds.DATA_FILTER,
                            color="blue",
                            w="50%",
                        ),
                    ],
                ),
                span={"base": 12, "md": 4},
            ),
        ],
    )


def layout():
    return dmc.Stack(
        p="md",
        children=[
            title_with_link(
                text="Psychrometric Chart",
                id_button=IdButtons.PSYCHROMETRIC_CHART_CHART,
                doc_link=DocLinks.PSYCHROMETRIC_CHART,
            ),
            inputs(),
            dmc.Skeleton(
                visible=False,
                h=450,
                id=ElementIds.PSYCH_CHART,
            ),
        ],
    )


@callback(
    Output(ElementIds.PSYCH_CHART, "children"),
    [
        Input(ElementIds.ID_PSY_CHART_DF_STORE, "modified_timestamp"),
        Input(ElementIds.PSY_COLOR_BY_DROPDOWN, "value"),
        Input(ElementIds.DATA_FILTER, "n_clicks"),
        Input(ElementIds.ID_PSY_CHART_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_PSY_CHART_DF_STORE, "data"),
        State(ElementIds.PSY_MIN_VAL, "value"),
        State(ElementIds.PSY_MAX_VAL, "value"),
        State(ElementIds.PSY_VAR_DROPDOWN, "value"),
        State(ElementIds.ID_PSY_CHART_META_STORE, "data"),
        State(ElementIds.ID_PSY_CHART_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_psych_chart(
    ts,
    colorby_var,
    data_filter,
    global_local,
    global_filter_data,
    df,
    min_val,
    max_val,
    data_filter_var,
    meta,
    si_ip,
):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import (
            apply_global_month_hour_filter,
            get_global_filter_state,
        )

        # Determine which columns to filter - need DBT and HR at minimum, plus colorby_var if it's not None/Frequency
        target_columns = [Variables.DBT.col_name, Variables.HR.col_name]
        if colorby_var not in ["None", "Frequency"]:
            target_columns.append(colorby_var)
        if data_filter and data_filter_var:
            target_columns.append(data_filter_var)

        df = apply_global_month_hour_filter(df, global_filter_data, target_columns)

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

        # Use local filtering when global filter is not active
        df = filter_df_by_month_and_hour(df, True, [1, 12], [0, 24], [], [], df.columns)

    if data_filter:
        if min_val <= max_val:
            mask = (df[data_filter_var] < min_val) | (df[data_filter_var] > max_val)
            df[mask] = None
        else:
            mask = (df[data_filter_var] >= max_val) & (df[data_filter_var] <= min_val)
            df[mask] = None

    if df.dropna(subset=[Variables.MONTH.col_name]).shape[0] == 0:
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
        var_unit = VariableInfo.from_col_name(var).get_unit(si_ip)

        var_name = VariableInfo.from_col_name(var).get_name()

        var_color = VariableInfo.from_col_name(var).get_color()

    if global_local == "global":
        # Set Global values for Max and minimum
        variable_x = VariableInfo.from_col_name(Variables.DBT.col_name)
        variable_y = VariableInfo.from_col_name(Variables.HR.col_name)

        var_range_x = variable_x.get_range(si_ip)
        var_range_y = variable_y.get_range(si_ip)

    else:
        # Set maximum and minimum according to data
        data_max, data_min = get_max_min_value(df[Variables.DBT.col_name])
        var_range_x = [data_min, data_max]

        data_max = round(df[Variables.HR.col_name].max(), 4)
        data_min = round(df[Variables.HR.col_name].min(), 4)
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
        rh_df[name] = hr_df[Variables.HR.col_name]

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

    # Separate filtered and unfiltered data using utility function
    # Note: psy-chart needs to check multiple original columns (DBT, HR, and var)
    filter_info = separate_filtered_data(df, Variables.DBT.col_name)
    df_unfiltered = filter_info["df_unfiltered"]

    # Process HR for unfiltered data
    df_unfiltered_hr_multiply = list(df_unfiltered[Variables.HR.col_name])
    for k in range(len(df_unfiltered_hr_multiply)):
        df_unfiltered_hr_multiply[k] = df_unfiltered_hr_multiply[k] * 1000

    # Filtered data traces removed - no gray filtering effect for psychrometric chart

    # Add unfiltered data traces (normal colors)
    if len(df_unfiltered) > 0:
        if var == "None":
            fig.add_trace(
                go.Scatter(
                    x=df_unfiltered[Variables.DBT.col_name],
                    y=df_unfiltered_hr_multiply,
                    showlegend=False,
                    mode="markers",
                    marker=dict(
                        size=6,
                        color=var_color,
                        showscale=False,
                        opacity=0.2,
                    ),
                    hovertemplate=VariableInfo.from_col_name(
                        Variables.DBT.col_name
                    ).get_name()
                    + ": %{x:.2f}"
                    + VariableInfo.from_col_name(Variables.DBT.col_name).get_unit(
                        si_ip
                    ),
                    name="",
                )
            )
        elif var == "Frequency":
            fig.add_trace(
                go.Histogram2d(
                    x=df_unfiltered[Variables.DBT.col_name],
                    y=df_unfiltered_hr_multiply,
                    name="",
                    colorscale=var_color,
                    hovertemplate="",
                    autobinx=False,
                    xbins=dict(start=-50, end=100, size=1),
                )
            )
            # Filtered data removed - no gray filtering effect for psychrometric chart

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
                    x=df_unfiltered[Variables.DBT.col_name],
                    y=df_unfiltered_hr_multiply,
                    showlegend=False,
                    mode="markers",
                    marker=dict(
                        size=5,
                        color=df_unfiltered[var],
                        showscale=True,
                        opacity=0.3,
                        colorscale=var_color,
                        colorbar=var_colorbar,
                    ),
                    customdata=np.stack(
                        (
                            df_unfiltered[Variables.RH.col_name],
                            df_unfiltered["h"],
                            df_unfiltered[var],
                            df_unfiltered["t_dp"],
                        ),
                        axis=-1,
                    ),
                    hovertemplate=VariableInfo.from_col_name(
                        Variables.DBT.col_name
                    ).get_name()
                    + ": %{x:.2f}"
                    + VariableInfo.from_col_name(Variables.DBT.col_name).get_unit(si_ip)
                    + "<br>"
                    + VariableInfo.from_col_name(Variables.RH.col_name).get_name()
                    + ": %{customdata[0]:.2f}"
                    + VariableInfo.from_col_name(Variables.RH.col_name).get_unit(si_ip)
                    + "<br>"
                    + VariableInfo.from_col_name("h").get_name()
                    + ": %{customdata[1]:.2f}"
                    + VariableInfo.from_col_name("h").get_unit(si_ip)
                    + "<br>"
                    + VariableInfo.from_col_name("t_dp").get_name()
                    + ": %{customdata[3]:.2f}"
                    + VariableInfo.from_col_name("t_dp").get_unit(si_ip)
                    + "<br>"
                    + "<br>"
                    + var_name
                    + ": %{customdata[2]:.2f}"
                    + var_unit,
                    name="",
                )
            )

    xtitle_name = (
        "Temperature"
        + "  "
        + VariableInfo.from_col_name(Variables.DBT.col_name).get_unit(si_ip)
    )
    ytitle_name = (
        "Humidity Ratio"
        + "  "
        + VariableInfo.from_col_name(Variables.HR.col_name).get_unit(si_ip)
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
