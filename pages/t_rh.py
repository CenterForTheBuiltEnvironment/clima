import dash
from dash_extensions.enrich import Output, Input, State, dcc, callback
import dash_mantine_components as dmc

from config import PageUrls, DocLinks, PageInfo
from pages.lib.global_scheme import dropdown_names
from pages.lib.template_graphs import heatmap, yearly_profile, daily_profile
from pages.lib.global_column_names import ColNames
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
    return dmc.Container(
        fluid=True,
        p="md",
        children=[
            dmc.Group(
                justify="center",
                align="center",
                wrap="nowrap",
                children=[
                    dmc.Title("Select a variable:", order=5),
                    dropdown(
                        id=ElementIds.ID_T_RH_DROPDOWN,
                        options={var: dropdown_names[var] for var in var_to_plot},
                        value=dropdown_names[var_to_plot[0]],
                        style={"width": "14rem"},
                    ),
                ],
            ),
            dmc.Stack(
                mt="md",
                children=[
                    # Yearly Chart
                    title_with_link(
                        text="Yearly Chart",
                        id_button=IdButtons.YEARLY_CHART_LABEL,
                        doc_link=DocLinks.TEMP_HUMIDITY_EXPLAINED,
                    ),
                    dcc.Loading(
                        type="circle",
                        children=dmc.Stack(id=ElementIds.YEARLY_CHART),
                    ),
                    # Daily chart
                    title_with_link(
                        text="Daily chart",
                        id_button=IdButtons.DAILY_CHART_LABEL,
                        doc_link=DocLinks.TEMP_HUMIDITY_EXPLAINED,
                    ),
                    dcc.Loading(
                        type="circle",
                        children=dmc.Stack(id=ElementIds.DAILY),
                    ),
                    # Heatmap chart
                    title_with_link(
                        text="Heatmap chart",
                        id_button=IdButtons.HEATMAP_CHART_LABEL,
                        doc_link=DocLinks.TEMP_HUMIDITY_EXPLAINED,
                    ),
                    dcc.Loading(
                        type="circle",
                        children=dmc.Stack(id=ElementIds.HEATMAP),
                    ),
                    # Descriptive statistics
                    title_with_tooltip(
                        text="Descriptive statistics",
                        tooltip_text="count, mean, std, min, max, and percentiles",
                        id_button=IdButtons.TABLE_TMP_RH,
                    ),
                    dmc.Stack(id=ElementIds.TABLE_TMP_HUM),
                ],
            ),
        ],
    )


@callback(
    Output(ElementIds.YEARLY_CHART, "children"),
    [
        Input(ElementIds.ID_T_RH_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_T_RH_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.ID_T_RH_DROPDOWN, "value"),
    ],
    [
        State(ElementIds.ID_T_RH_DF_STORE, "data"),
        State(ElementIds.ID_T_RH_META_STORE, "data"),
        State(ElementIds.ID_T_RH_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_yearly_chart(_, global_local, dd_value, df, meta, si_ip):
    if dd_value == dropdown_names[var_to_plot[0]]:
        dbt_yearly = yearly_profile(df, ColNames.DBT, global_local, si_ip)
        dbt_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        units = generate_units_degree(si_ip)
        return dcc.Graph(
            config=generate_chart_name(
                TabNames.DRY_BULB_TEMPERATURE_YEARLY, meta, units
            ),
            figure=dbt_yearly,
        )
    else:
        rh_yearly = yearly_profile(df, ColNames.RH, global_local, si_ip)
        rh_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        units = generate_units(si_ip)
        return dcc.Graph(
            config=generate_chart_name(TabNames.RELATIVE_HUMIDITY_YEARLY, meta, units),
            figure=rh_yearly,
        )


@callback(
    Output(ElementIds.DAILY, "children"),
    [
        Input(ElementIds.ID_T_RH_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_T_RH_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.ID_T_RH_DROPDOWN, "value"),
    ],
    [
        State(ElementIds.ID_T_RH_DF_STORE, "data"),
        State(ElementIds.ID_T_RH_META_STORE, "data"),
        State(ElementIds.ID_T_RH_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_daily(_, global_local, dd_value, df, meta, si_ip):
    if dd_value == dropdown_names[var_to_plot[0]]:
        units = generate_units_degree(si_ip)
        return dcc.Graph(
            config=generate_chart_name(
                TabNames.DRY_BULB_TEMPERATURE_DAILY, meta, units
            ),
            figure=daily_profile(
                df[
                    [
                        ColNames.DBT,
                        ColNames.HOUR,
                        ColNames.UTC_TIME,
                        ColNames.MONTH_NAMES,
                        ColNames.DAY,
                        ColNames.MONTH,
                    ]
                ],
                ColNames.DBT,
                global_local,
                si_ip,
            ),
        )
    else:
        units = generate_units(si_ip)
        return dcc.Graph(
            config=generate_chart_name(TabNames.RELATIVE_HUMIDITY_DAILY, meta, units),
            figure=daily_profile(
                df[
                    [
                        ColNames.RH,
                        ColNames.HOUR,
                        ColNames.UTC_TIME,
                        ColNames.MONTH_NAMES,
                        ColNames.DAY,
                        ColNames.MONTH,
                    ]
                ],
                ColNames.RH,
                global_local,
                si_ip,
            ),
        )


@callback(
    Output(ElementIds.HEATMAP, "children"),
    [
        Input(ElementIds.ID_T_RH_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_T_RH_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.ID_T_RH_DROPDOWN, "value"),
    ],
    [
        State(ElementIds.ID_T_RH_DF_STORE, "data"),
        State(ElementIds.ID_T_RH_META_STORE, "data"),
        State(ElementIds.ID_T_RH_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_heatmap(_, global_local, dd_value, df, meta, si_ip):
    """Update heatmap content."""
    if dd_value == dropdown_names[var_to_plot[0]]:
        units = generate_units_degree(si_ip)
        return dcc.Graph(
            config=generate_chart_name(
                TabNames.DRY_BULB_TEMPERATURE_HEATMAP, meta, units
            ),
            figure=heatmap(
                df[
                    [
                        ColNames.DBT,
                        ColNames.HOUR,
                        ColNames.UTC_TIME,
                        ColNames.MONTH_NAMES,
                        ColNames.DAY,
                    ]
                ],
                ColNames.DBT,
                global_local,
                si_ip,
            ),
        )
    else:
        units = generate_units(si_ip)
        return dcc.Graph(
            config=generate_chart_name(TabNames.RELATIVE_HUMIDITY_HEATMAP, meta, units),
            figure=heatmap(
                df[
                    [
                        ColNames.RH,
                        ColNames.HOUR,
                        ColNames.UTC_TIME,
                        ColNames.MONTH_NAMES,
                        ColNames.DAY,
                    ]
                ],
                ColNames.RH,
                global_local,
                si_ip,
            ),
        )


@callback(
    Output(ElementIds.TABLE_TMP_HUM, "children"),
    [
        Input(ElementIds.ID_T_RH_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_T_RH_DROPDOWN, "value"),
    ],
    [
        State(ElementIds.ID_T_RH_DF_STORE, "data"),
        State(ElementIds.ID_T_RH_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_table(_, dd_value, df, si_ip):
    """Update the contents of descriptive statistics table."""
    return summary_table_tmp_rh_tab(
        df[[ColNames.MONTH, ColNames.HOUR, dd_value, ColNames.MONTH_NAMES]],
        dd_value,
        si_ip,
    )
