import dash
from dash_extensions.enrich import Output, Input, State, dcc, callback
import dash_mantine_components as dmc

from config import PageUrls, DocLinks, PageInfo
from pages.lib.global_scheme import dropdown_names
from pages.lib.template_graphs import heatmap, yearly_profile, daily_profile
from pages.lib.global_variables import Variables
from pages.lib.global_element_ids import ElementIds
from pages.lib.global_id_buttons import IdButtons
from pages.lib.global_tab_names import TabNames
from pages.lib.utils import (
    generate_chart_name,
    generate_units,
    generate_units_degree,
    title_with_tooltip,
    summary_table_tmp_rh_tab,
    title_with_link,
    dropdown,
)


dash.register_page(
    __name__,
    name=PageInfo.TEMP_RH_NAME,
    path=PageUrls.T_RH.value,
    order=PageInfo.TEMP_RH_ORDER,
)


var_to_plot = ["Dry bulb temperature", "Relative humidity"]


def layout():
    return dmc.Stack(
        p="md",
        children=[
            dmc.Center(
                [
                    dmc.Title("Select a variable:", order=5, mr="md"),
                    dropdown(
                        id=ElementIds.ID_T_RH_DROPDOWN,
                        options={var: dropdown_names[var] for var in var_to_plot},
                        value=dropdown_names[var_to_plot[0]],
                    ),
                ]
            ),
            # Yearly Chart
            title_with_link(
                text="Yearly Chart",
                id_button=IdButtons.YEARLY_CHART_LABEL,
                doc_link=DocLinks.TEMP_HUMIDITY_EXPLAINED,
            ),
            dmc.Skeleton(
                visible=False,
                h=450,
                children=dmc.Stack(id=ElementIds.YEARLY_CHART),
            ),
            # Daily chart
            title_with_link(
                text="Daily chart",
                id_button=IdButtons.DAILY_CHART_LABEL,
                doc_link=DocLinks.TEMP_HUMIDITY_EXPLAINED,
            ),
            dmc.Skeleton(
                visible=False,
                h=450,
                children=dmc.Stack(id=ElementIds.DAILY),
            ),
            # Heatmap chart
            title_with_link(
                text="Heatmap chart",
                id_button=IdButtons.HEATMAP_CHART_LABEL,
                doc_link=DocLinks.TEMP_HUMIDITY_EXPLAINED,
            ),
            dmc.Skeleton(
                visible=False,
                h=450,
                children=dmc.Stack(id=ElementIds.HEATMAP),
            ),
            # Descriptive statistics
            title_with_tooltip(
                text="Descriptive statistics",
                tooltip_text="count, mean, std, min, max, and percentiles",
                id_button=IdButtons.TABLE_TMP_RH,
            ),
            dmc.Skeleton(
                visible=False,
                h=450,
                children=dmc.Stack(id=ElementIds.TABLE_TMP_HUM),
            ),
        ],
    )


@callback(
    Output(ElementIds.YEARLY_CHART, "children"),
    [
        Input(ElementIds.SHARED_DF_STORE, "modified_timestamp"),
        Input(ElementIds.SHARED_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.ID_T_RH_DROPDOWN, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.SHARED_DF_STORE, "data"),
        State(ElementIds.SHARED_META_STORE, "data"),
        State(ElementIds.SHARED_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_yearly_chart(_, global_local, dd_value, global_filter_data, df, meta, si_ip):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        target_columns = [
            Variables.DBT.col_name,
            Variables.RH.col_name,
            Variables.ADAPTIVE_CMF_80_LOW.col_name,
            Variables.ADAPTIVE_CMF_80_UP.col_name,
            Variables.ADAPTIVE_CMF_90_LOW.col_name,
            Variables.ADAPTIVE_CMF_90_UP.col_name,
            Variables.ADAPTIVE_CMF_RMT.col_name,
        ]
        df = apply_global_month_hour_filter(df, global_filter_data, target_columns)

    if dd_value == dropdown_names[var_to_plot[0]]:
        # Ensure all necessary columns are included for filtered data display
        required_cols = [
            Variables.DBT.col_name,
            Variables.UTC_TIME.col_name,
            Variables.MONTH_NAMES.col_name,
            Variables.DAY.col_name,
            Variables.DOY.col_name,
            Variables.ADAPTIVE_CMF_80_LOW.col_name,
            Variables.ADAPTIVE_CMF_80_UP.col_name,
            Variables.ADAPTIVE_CMF_90_LOW.col_name,
            Variables.ADAPTIVE_CMF_90_UP.col_name,
            Variables.ADAPTIVE_CMF_RMT.col_name,
        ]
        if "_is_filtered" in df.columns:
            required_cols.append("_is_filtered")
        if f"_{Variables.DBT.col_name}_original" in df.columns:
            required_cols.append(f"_{Variables.DBT.col_name}_original")
        dbt_yearly = yearly_profile(
            df[required_cols], Variables.DBT.col_name, global_local, si_ip
        )
        dbt_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        units = generate_units_degree(si_ip)
        return dcc.Graph(
            config=generate_chart_name(
                TabNames.DRY_BULB_TEMPERATURE_YEARLY, meta, units
            ),
            figure=dbt_yearly,
        )
    else:
        # Ensure all necessary columns are included for filtered data display
        required_cols = [
            Variables.RH.col_name,
            Variables.UTC_TIME.col_name,
            Variables.MONTH_NAMES.col_name,
            Variables.DAY.col_name,
        ]
        if "_is_filtered" in df.columns:
            required_cols.append("_is_filtered")
        if f"_{Variables.RH.col_name}_original" in df.columns:
            required_cols.append(f"_{Variables.RH.col_name}_original")
        rh_yearly = yearly_profile(
            df[required_cols], Variables.RH.col_name, global_local, si_ip
        )
        rh_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        units = generate_units(si_ip)
        return dcc.Graph(
            config=generate_chart_name(TabNames.RELATIVE_HUMIDITY_YEARLY, meta, units),
            figure=rh_yearly,
        )


@callback(
    Output(ElementIds.DAILY, "children"),
    [
        Input(ElementIds.SHARED_DF_STORE, "modified_timestamp"),
        Input(ElementIds.SHARED_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.ID_T_RH_DROPDOWN, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.SHARED_DF_STORE, "data"),
        State(ElementIds.SHARED_META_STORE, "data"),
        State(ElementIds.SHARED_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_daily(_, global_local, dd_value, global_filter_data, df, meta, si_ip):
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        target_columns = [Variables.DBT.col_name, Variables.RH.col_name]
        df = apply_global_month_hour_filter(df, global_filter_data, target_columns)

    if dd_value == dropdown_names[var_to_plot[0]]:
        # Ensure all necessary columns are included for filtered data display
        base_columns = [
            Variables.DBT.col_name,
            Variables.HOUR.col_name,
            Variables.UTC_TIME.col_name,
            Variables.MONTH_NAMES.col_name,
            Variables.DAY.col_name,
            Variables.MONTH.col_name,
        ]
        if "_is_filtered" in df.columns:
            base_columns.append("_is_filtered")
        if f"_{Variables.DBT.col_name}_original" in df.columns:
            base_columns.append(f"_{Variables.DBT.col_name}_original")
        units = generate_units_degree(si_ip)
        return dcc.Graph(
            config=generate_chart_name(
                TabNames.DRY_BULB_TEMPERATURE_DAILY, meta, units
            ),
            figure=daily_profile(
                df[base_columns],
                Variables.DBT.col_name,
                global_local,
                si_ip,
            ),
        )
    else:
        # Ensure all necessary columns are included for filtered data display
        base_columns = [
            Variables.RH.col_name,
            Variables.HOUR.col_name,
            Variables.UTC_TIME.col_name,
            Variables.MONTH_NAMES.col_name,
            Variables.DAY.col_name,
            Variables.MONTH.col_name,
        ]
        if "_is_filtered" in df.columns:
            base_columns.append("_is_filtered")
        if f"_{Variables.RH.col_name}_original" in df.columns:
            base_columns.append(f"_{Variables.RH.col_name}_original")
        units = generate_units(si_ip)
        return dcc.Graph(
            config=generate_chart_name(TabNames.RELATIVE_HUMIDITY_DAILY, meta, units),
            figure=daily_profile(
                df[base_columns],
                Variables.RH.col_name,
                global_local,
                si_ip,
            ),
        )


@callback(
    Output(ElementIds.HEATMAP, "children"),
    [
        Input(ElementIds.SHARED_DF_STORE, "modified_timestamp"),
        Input(ElementIds.SHARED_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.ID_T_RH_DROPDOWN, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.SHARED_DF_STORE, "data"),
        State(ElementIds.SHARED_META_STORE, "data"),
        State(ElementIds.SHARED_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_heatmap(_, global_local, dd_value, global_filter_data, df, meta, si_ip):
    """Update heatmap content."""
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        target_columns = [Variables.DBT.col_name, Variables.RH.col_name]
        df = apply_global_month_hour_filter(df, global_filter_data, target_columns)

    base_columns = [
        Variables.HOUR.col_name,
        Variables.UTC_TIME.col_name,
        Variables.MONTH_NAMES.col_name,
        Variables.DAY.col_name,
    ]
    if "_is_filtered" in df.columns:
        base_columns.append("_is_filtered")

    if dd_value == dropdown_names[var_to_plot[0]]:
        if f"_{Variables.DBT.col_name}_original" in df.columns:
            base_columns.append(f"_{Variables.DBT.col_name}_original")
        units = generate_units_degree(si_ip)
        return dcc.Graph(
            config=generate_chart_name(
                TabNames.DRY_BULB_TEMPERATURE_HEATMAP, meta, units
            ),
            figure=heatmap(
                df[[Variables.DBT.col_name] + base_columns],
                Variables.DBT.col_name,
                global_local,
                si_ip,
            ),
        )
    else:
        if f"_{Variables.RH.col_name}_original" in df.columns:
            base_columns.append(f"_{Variables.RH.col_name}_original")
        units = generate_units(si_ip)
        return dcc.Graph(
            config=generate_chart_name(TabNames.RELATIVE_HUMIDITY_HEATMAP, meta, units),
            figure=heatmap(
                df[[Variables.RH.col_name] + base_columns],
                Variables.RH.col_name,
                global_local,
                si_ip,
            ),
        )


@callback(
    Output(ElementIds.TABLE_TMP_HUM, "children"),
    [
        Input(ElementIds.SHARED_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_T_RH_DROPDOWN, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.SHARED_DF_STORE, "data"),
        State(ElementIds.SHARED_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_table(_, dd_value, global_filter_data, df, si_ip):
    """Update the contents of descriptive statistics table."""
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        target_columns = [Variables.DBT.col_name, Variables.RH.col_name]
        df = apply_global_month_hour_filter(df, global_filter_data, target_columns)
        # Filter out the filtered rows to avoid empty columns
        if "_is_filtered" in df.columns:
            df = df[~df["_is_filtered"]]

    return summary_table_tmp_rh_tab(
        df[
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
