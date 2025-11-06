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
    return dmc.Stack(
        p="md",
        children=dmc.Skeleton(  # needed to avoid empty layout on load
            visible=True,
            height="100vh",
        ),
        id=ElementIds.MAIN_NV_SECTION,
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
        title_with_link(
            text="Natural Ventilation Potential",
            id_button=IdButtons.NATURAL_VENTILATION_LABEL,
            doc_link=DocLinks.NATURAL_VENTILATION,
        ),
        inputs_tab(tdb_set_min, tdb_set_max, dpt_set),
        dmc.Skeleton(
            visible=False,
            h=450,
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
        dmc.Skeleton(
            visible=False,
            h=450,
            children=dmc.Paper(
                id=ElementIds.NV_BAR_CHART,
            ),
        ),
    ]


def inputs_tab(t_min, t_max, d_set):
    return dmc.Grid(
        justify="center",
        children=[
            dmc.GridCol(
                dmc.Stack(
                    [
                        dmc.Title("Outdoor dry-bulb air temperature range", order=5),
                        dmc.Group(
                            [
                                dmc.Title("Min Value:", order=5),
                                dmc.NumberInput(
                                    id=ElementIds.NV_TDB_MIN_VAL,
                                    placeholder="Enter a number for the min val",
                                    step=1,
                                    value=t_min,
                                ),
                            ],
                        ),
                        dmc.Group(
                            [
                                dmc.Title("Max Value:", order=5),
                                dmc.NumberInput(
                                    id=ElementIds.NV_TDB_MAX_VAL,
                                    placeholder="Enter a number for the max val",
                                    value=t_max,
                                    step=1,
                                ),
                            ],
                        ),
                        dmc.Button(
                            "Apply filter",
                            color="blue",
                            id=ElementIds.NV_DBT_FILTER,
                            variant="link",
                            n_clicks=1,
                            w="80%",
                        ),
                    ]
                ),
                span={"base": 12, "md": 4},
            ),
            dmc.GridCol(
                dmc.Stack(
                    [
                        dmc.Group(
                            [
                                dmc.Title("Surface temperature:", order=5),
                                dmc.NumberInput(
                                    id=ElementIds.NV_DPT_MAX_VAL,
                                    placeholder="Enter a number for the max val",
                                    value=d_set,
                                    step=1,
                                ),
                            ],
                        ),
                        dmc.Checkbox(
                            id=ElementIds.ENABLE_CONDENSATION,
                            label=(
                                "Avoid condensation with radiant systems: If the "
                                "outdoor dew point temperature is below the radiant "
                                "system surface temperature, the data point is not plot."
                            ),
                            checked=False,
                            size="sm",
                            w="70%",
                        ),
                        dmc.Button(
                            "Apply filter",
                            color="blue",
                            id=ElementIds.NV_DPT_FILTER,
                            variant="link",
                            disabled=True,
                            w="70%",
                        ),
                    ]
                ),
                span={"base": 12, "md": 5},
            ),
        ],
    )


@callback(
    Output(ElementIds.NV_HEATMAP_CHART, "children"),
    [
        Input(ElementIds.ID_NATURAL_VENTILATION_DF_STORE, "modified_timestamp"),
        Input(ElementIds.NV_DBT_FILTER, "n_clicks"),
        Input(ElementIds.NV_DPT_FILTER, "n_clicks"),
        Input(ElementIds.ID_NATURAL_VENTILATION_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.ENABLE_CONDENSATION, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_NATURAL_VENTILATION_DF_STORE, "data"),
        State(ElementIds.NV_TDB_MIN_VAL, "value"),
        State(ElementIds.NV_TDB_MAX_VAL, "value"),
        State(ElementIds.NV_DPT_MAX_VAL, "value"),
        State(ElementIds.ID_NATURAL_VENTILATION_META_STORE, "data"),
        State(ElementIds.ID_NATURAL_VENTILATION_SI_IP_UNIT_STORE, "data"),
    ],
)
def nv_heatmap(
    ts,
    dbt_data_filter,
    click_dpt_filter,
    global_local,
    condensation_enabled,
    global_filter_data,
    df,
    min_dbt_val,
    max_dbt_val,
    max_dpt_val,
    meta,
    si_ip,
):
    if df is None:
        return no_update
    # enable or disable button apply filter DPT
    dpt_data_filter = enable_dew_point_data_filter(condensation_enabled)

    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import (
            apply_global_month_hour_filter,
            get_global_filter_state,
        )

        # Ensure DBT and DPT are included for filtering
        target_columns = [Variables.DBT.col_name, Variables.DPT.col_name]
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

    # Title will be updated based on global filter state
    if global_filter_data and global_filter_data.get("filter_active", False):
        title += (
            f" between the months of {month_lst[start_month - 1]} and "
            f"{month_lst[end_month - 1]}<br>and between the hours {start_hour}"
            f":00 and {end_hour}:00"
        )
    if dpt_data_filter:
        title += f" and when the {filter_name} is below {max_dpt_val} {filter_unit}."

    # Check if there's a filter marker
    has_filter_marker = "_is_filtered" in df.columns
    filtered_mask = None
    if has_filter_marker:
        filtered_mask = df["_is_filtered"]

    # Get original values if available
    original_var_col = f"_{var}_original"
    use_original_for_filtered = has_filter_marker and original_var_col in df.columns

    fig = go.Figure()

    # Add filtered data trace (gray) if any filtered data exists
    # Only show gray where there is actual data (not None), not in blank areas
    if has_filter_marker and filtered_mask is not None and filtered_mask.any():
        if use_original_for_filtered:
            # Use original DBT values for filtered data
            filtered_values = df[original_var_col].copy()
            # Apply DBT filter to original values to check if they're in range
            if dbt_data_filter and (min_dbt_val <= max_dbt_val):
                # Only show gray where original DBT is in range
                in_range_mask = (filtered_values >= min_dbt_val) & (
                    filtered_values <= max_dbt_val
                )
                # Also check if DPT filter applies
                if dpt_data_filter:
                    original_filter_var_col = f"_{filter_var}_original"
                    if original_filter_var_col in df.columns:
                        dpt_values = df[original_filter_var_col]
                        in_range_mask = (
                            in_range_mask
                            & (dpt_values >= -200)
                            & (dpt_values <= max_dpt_val)
                        )
                    else:
                        dpt_values = df[filter_var]
                        in_range_mask = (
                            in_range_mask
                            & (dpt_values >= -200)
                            & (dpt_values <= max_dpt_val)
                        )
                filtered_values[~in_range_mask] = None
        else:
            filtered_values = df[var].copy()

        # Only show gray for filtered data points
        filtered_values[~filtered_mask] = None

        # Only add trace if there are any valid filtered values
        if filtered_values.notna().any():
            fig.add_trace(
                go.Heatmap(
                    y=df[Variables.HOUR.col_name] - 0.5,
                    x=df[Variables.UTC_TIME.col_name].dt.date,
                    z=filtered_values,
                    colorscale=[[0, "lightgray"], [1, "gray"]],
                    zmin=range_z[0],
                    zmax=range_z[1],
                    showscale=False,
                    connectgaps=False,
                    hoverongaps=False,
                    customdata=np.stack(
                        (
                            df[Variables.MONTH_NAMES.col_name],
                            df[Variables.DAY.col_name],
                        ),
                        axis=-1,
                    ),
                    hovertemplate=(
                        "<b>Filtered Data</b><br>"
                        + var
                        + ": %{z:.2f} "
                        + var_unit
                        + "</b><br>"
                        + "Month: %{customdata[0]}<br>"
                        + "Day: %{customdata[1]}<br>"
                        + "Hour: %{y}:00<br>"
                    ),
                    name="filtered",
                )
            )

        # Add unfiltered data trace (normal color)
        base_values = df[var].copy()
        base_values[filtered_mask] = None

        fig.add_trace(
            go.Heatmap(
                y=df[Variables.HOUR.col_name] - 0.5,
                x=df[Variables.UTC_TIME.col_name].dt.date,
                z=base_values,
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
    else:
        # No filtered data, use normal heatmap
        fig.add_trace(
            go.Heatmap(
                y=df[Variables.HOUR.col_name] - 0.5,
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
        Input(ElementIds.NV_DBT_FILTER, "n_clicks"),
        Input(ElementIds.NV_DPT_FILTER, "n_clicks"),
        Input(ElementIds.ID_NATURAL_VENTILATION_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.SWITCHES_INPUT, "checked"),
        Input(ElementIds.ENABLE_CONDENSATION, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_NATURAL_VENTILATION_DF_STORE, "data"),
        State(ElementIds.NV_TDB_MIN_VAL, "value"),
        State(ElementIds.NV_TDB_MAX_VAL, "value"),
        State(ElementIds.NV_DPT_MAX_VAL, "value"),
        State(ElementIds.ID_NATURAL_VENTILATION_META_STORE, "data"),
        State(ElementIds.ID_NATURAL_VENTILATION_SI_IP_UNIT_STORE, "data"),
    ],
)
def nv_bar_chart(
    ts,
    dbt_data_filter,
    click_dpt_filter,
    global_local,
    normalize,
    condensation_enabled,
    global_filter_data,
    df,
    min_dbt_val,
    max_dbt_val,
    max_dpt_val,
    meta,
    si_ip,
):
    # enable or disable button apply filter DPT
    dpt_data_filter = enable_dew_point_data_filter(condensation_enabled)

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

    # Store original data info before applying global filter (to know which months originally had data)
    if global_filter_data and global_filter_data.get("filter_active", False):
        # Create a copy to check which months have data after DBT/DPT filtering (but before global filter)
        df_temp = df.copy()
        df_temp[Variables.NV_ALLOWED.col_name] = 1

        # Apply DBT/DPT filters to the temporary copy
        if dbt_data_filter and (min_dbt_val <= max_dbt_val):
            df_temp.loc[
                (df_temp[var] < min_dbt_val) | (df_temp[var] > max_dbt_val),
                Variables.NV_ALLOWED.col_name,
            ] = 0

        if dpt_data_filter:
            df_temp.loc[
                (df_temp[filter_var] > max_dpt_val), Variables.NV_ALLOWED.col_name
            ] = 0

        # Check which months have data (NV_ALLOWED > 0) after DBT/DPT filtering
        months_with_nv = df_temp[df_temp[Variables.NV_ALLOWED.col_name] > 0]
        if len(months_with_nv) > 0:
            set(months_with_nv[Variables.UTC_TIME.col_name].dt.month.unique())

    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import (
            apply_global_month_hour_filter,
            get_global_filter_state,
        )

        # Include DBT and DPT in target_columns to preserve original values for filtered data
        # Note: Do NOT include NV_ALLOWED in target_columns, as it will be set to None by time_filtering
        # for filtered months, which would break the calculation of n_hours_nv_allowed_filtered
        df = apply_global_month_hour_filter(
            df, global_filter_data, [Variables.DBT.col_name, Variables.DPT.col_name]
        )

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

    # Check if there's a filter marker
    has_filter_marker = "_is_filtered" in df.columns
    filtered_mask = None
    if has_filter_marker:
        filtered_mask = df["_is_filtered"]

    # Separate filtered and unfiltered data
    if has_filter_marker and filtered_mask is not None:
        df_unfiltered = df[~filtered_mask].copy()
        df_filtered = df[filtered_mask].copy() if filtered_mask.any() else None
    else:
        df_unfiltered = df
        df_filtered = None

    # Calculate total hours per month (for both filtered and unfiltered) - ensure all 12 months are included
    # This should be calculated BEFORE applying DBT/DPT filters, as it represents total hours in the selected time range
    tot_month_hours_unfiltered = np.zeros(12)
    tot_unfiltered_grouped = df_unfiltered.groupby(
        df_unfiltered[Variables.UTC_TIME.col_name].dt.month
    )[Variables.NV_ALLOWED.col_name].sum()
    for month_idx in range(1, 13):
        if month_idx in tot_unfiltered_grouped.index:
            tot_month_hours_unfiltered[month_idx - 1] = tot_unfiltered_grouped[
                month_idx
            ]

    # Calculate total filtered hours BEFORE applying DBT/DPT filters
    # This represents all hours that were filtered by the global month/hour filter
    # Simply count the number of rows in df_filtered for each month (each row = 1 hour)
    tot_month_hours_filtered = np.zeros(12)
    if df_filtered is not None and len(df_filtered) > 0:
        # Count rows per month (each row represents 1 hour)
        # This is the most reliable way as it doesn't depend on NV_ALLOWED being set
        tot_filtered_grouped = df_filtered.groupby(
            df_filtered[Variables.UTC_TIME.col_name].dt.month
        ).size()
        for month_idx in range(1, 13):
            if month_idx in tot_filtered_grouped.index:
                tot_month_hours_filtered[month_idx - 1] = tot_filtered_grouped[
                    month_idx
                ]

    # Apply DBT and DPT filters to unfiltered data
    if dbt_data_filter and (min_dbt_val <= max_dbt_val):
        df_unfiltered.loc[
            (df_unfiltered[var] < min_dbt_val) | (df_unfiltered[var] > max_dbt_val),
            Variables.NV_ALLOWED.col_name,
        ] = 0

    if dpt_data_filter:
        df_unfiltered.loc[
            (df_unfiltered[filter_var] > max_dpt_val), Variables.NV_ALLOWED.col_name
        ] = 0

    # Apply DBT and DPT filters to filtered data (using original values if available)
    if df_filtered is not None and len(df_filtered) > 0:
        original_var_col = f"_{var}_original"
        original_filter_var_col = f"_{filter_var}_original"
        use_original_var = original_var_col in df_filtered.columns
        use_original_filter_var = original_filter_var_col in df_filtered.columns

        if dbt_data_filter and (min_dbt_val <= max_dbt_val):
            filter_var_to_use = original_var_col if use_original_var else var
            df_filtered.loc[
                (df_filtered[filter_var_to_use] < min_dbt_val)
                | (df_filtered[filter_var_to_use] > max_dbt_val),
                Variables.NV_ALLOWED.col_name,
            ] = 0

        if dpt_data_filter:
            filter_var_to_use = (
                original_filter_var_col if use_original_filter_var else filter_var
            )
            df_filtered.loc[
                (df_filtered[filter_var_to_use] > max_dpt_val),
                Variables.NV_ALLOWED.col_name,
            ] = 0

    # Calculate hours for unfiltered data - ensure all 12 months are included
    n_hours_nv_allowed_unfiltered = np.zeros(12)
    n_hours_unfiltered_grouped = (
        df_unfiltered.dropna(subset=Variables.NV_ALLOWED.col_name)
        .groupby(df_unfiltered[Variables.UTC_TIME.col_name].dt.month)[
            Variables.NV_ALLOWED.col_name
        ]
        .sum()
    )
    for month_idx in range(1, 13):
        if month_idx in n_hours_unfiltered_grouped.index:
            n_hours_nv_allowed_unfiltered[month_idx - 1] = n_hours_unfiltered_grouped[
                month_idx
            ]

    # Calculate hours for filtered data - ensure all 12 months are included
    n_hours_nv_allowed_filtered = np.zeros(12)
    if df_filtered is not None and len(df_filtered) > 0:
        n_hours_filtered_grouped = (
            df_filtered.dropna(subset=Variables.NV_ALLOWED.col_name)
            .groupby(df_filtered[Variables.UTC_TIME.col_name].dt.month)[
                Variables.NV_ALLOWED.col_name
            ]
            .sum()
        )
        for month_idx in range(1, 13):
            if month_idx in n_hours_filtered_grouped.index:
                n_hours_nv_allowed_filtered[month_idx - 1] = n_hours_filtered_grouped[
                    month_idx
                ]

    # Calculate percentages - handle division by zero
    per_time_nv_allowed_unfiltered = np.zeros(12)
    for i in range(12):
        if tot_month_hours_unfiltered[i] > 0:
            per_time_nv_allowed_unfiltered[i] = np.round(
                100 * (n_hours_nv_allowed_unfiltered[i] / tot_month_hours_unfiltered[i])
            )

    per_time_nv_allowed_filtered = np.zeros(12)
    # Calculate percentages for all months where filtered hours exist
    # Even if nv_allowed is 0, we should still show the gray bar (with 0% value)
    for i in range(12):
        if tot_month_hours_filtered[i] > 0:
            per_time_nv_allowed_filtered[i] = np.round(
                100 * (n_hours_nv_allowed_filtered[i] / tot_month_hours_filtered[i])
            )

    month_names = month_lst  # Use month_lst to ensure all 12 months are included
    traces = []

    # Add filtered data traces (gray) if any filtered data exists
    # For normalize mode: Show gray bars for months that have data but are outside the global filter range
    # For non-normalize mode: Show gray bars for all filtered months
    has_filtered_data = False
    if has_filter_marker and filtered_mask is not None and filtered_mask.any():
        # Show gray bars if there are any filtered hours in any month
        has_filtered_data = np.any(tot_month_hours_filtered > 0)

    if has_filtered_data:
        if not normalize:
            trace_filtered = go.Bar(
                x=month_names,
                y=n_hours_nv_allowed_filtered,
                name="Natural Ventilation (Filtered)",
                marker_color="gray",
                customdata=np.stack(
                    (n_hours_nv_allowed_filtered, per_time_nv_allowed_filtered), axis=-1
                ),
                hovertemplate=(
                    "<b>Filtered Data</b><br>natural ventilation possible for: <br>%{customdata[0]} hrs or"
                    " <br>%{customdata[1]}% of selected time<br>"
                ),
            )
            traces.append(trace_filtered)
        else:
            # For normalize mode: Show gray bars for months outside the global filter range
            # Use actual percentage values, but for 0% values, use a minimal visible height (0.1%)
            # so users can see that these months have filtered data
            per_time_display_filtered = per_time_nv_allowed_filtered.copy()

            # Set None for months without filtered data (so they don't show gray bars)
            # For months with filtered data but 0% NV, use 0.1% for minimal visibility
            for i in range(12):
                if tot_month_hours_filtered[i] == 0:
                    per_time_display_filtered[i] = None
                elif per_time_nv_allowed_filtered[i] == 0:
                    # Use 0.1% for months with filtered data but 0% NV (very small but visible)
                    per_time_display_filtered[i] = 0.1

            trace_filtered = go.Bar(
                x=month_names,
                y=per_time_display_filtered,
                name="Natural Ventilation (Filtered)",
                marker_color="gray",
                marker_line_color="gray",
                marker_line_width=1,
                customdata=np.stack(
                    (
                        n_hours_nv_allowed_filtered,
                        per_time_nv_allowed_filtered,
                        tot_month_hours_filtered,
                    ),
                    axis=-1,
                ),
                hovertemplate=(
                    "<b>Filtered Data</b><br>natural ventilation possible for: <br>%{customdata[0]} hrs or <br>%{"
                    "customdata[1]:.2f}% of filtered time range<br>Total filtered hours: %{customdata[2]:.0f}<br>"
                ),
                base=0,
                opacity=0.8,
            )
            traces.append(trace_filtered)

    # Add unfiltered data traces (normal colors)
    if not normalize:
        trace_unfiltered = go.Bar(
            x=month_names,
            y=n_hours_nv_allowed_unfiltered,
            name="Natural Ventilation",
            marker_color=color_in,
            customdata=np.stack(
                (n_hours_nv_allowed_unfiltered, per_time_nv_allowed_unfiltered), axis=-1
            ),
            hovertemplate=(
                "natural ventilation possible for: <br>%{customdata[0]} hrs or"
                " <br>%{customdata[1]}% of selected time<br>"
            ),
        )
        traces.append(trace_unfiltered)

        title = (
            f"Number of hours the {var_name}"
            + f" is in the range {min_dbt_val}"
            + " to "
            + f" {max_dbt_val} {var_unit}"
        )
    else:
        trace_unfiltered = go.Bar(
            x=month_names,
            y=per_time_nv_allowed_unfiltered,
            name="Natural Ventilation",
            marker_color=color_in,
            customdata=np.stack(
                (n_hours_nv_allowed_unfiltered, per_time_nv_allowed_unfiltered), axis=-1
            ),
            hovertemplate=(
                "natural ventilation possible for: <br>%{customdata[0]} hrs or <br>%{"
                "customdata[1]}% of selected time<br>"
            ),
        )
        traces.append(trace_unfiltered)

        title = (
            f"Percentage of hours the {var_name}"
            + f" is in the range {min_dbt_val}"
            + f" to {max_dbt_val}"
            + f" {var_unit}"
        )

    fig = go.Figure(data=traces)

    if not normalize:
        fig.update_yaxes(title_text="hours", range=[0, 744])
    else:
        fig.update_yaxes(title_text="Percentage (%)", range=[0, 100])

    if global_filter_data and global_filter_data.get("filter_active", False):
        title += (
            f" between the months of {month_lst[start_month - 1]} and "
            f"{month_lst[end_month - 1]} and between<br>the hours {start_hour}"
            f":00 and {end_hour}:00"
        )
    if dpt_data_filter:
        title += f" when the {filter_name} is below {max_dpt_val} {filter_unit}."

    # Use barmode="relative" to show filtered and unfiltered bars side by side
    # Only use relative mode if we have filtered data (non-normalize mode only)
    fig.update_layout(
        template=template,
        title=title,
        barnorm="",
        dragmode=False,
        margin=tight_margins.copy().update({"t": 55}),
        barmode="relative" if has_filtered_data else "group",
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
    Input(ElementIds.ENABLE_CONDENSATION, "checked"),
)
def enable_disable_button_data_filter(state_checkbox):
    if state_checkbox:
        return False
    else:
        return True


def enable_dew_point_data_filter(condensation_enabled):
    if condensation_enabled:
        return True
    else:
        return False
