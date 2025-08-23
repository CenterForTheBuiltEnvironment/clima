import dash
from dash_extensions.enrich import Output, Input, State, dcc, html, callback
from pages.components import ElementIds, Text, IdButtons, Type, ComponentProperty
from config import PageUrls, DocLinks, PageInfo
from pages.lib.global_scheme import dropdown_names
from pages.lib.template_graphs import heatmap, yearly_profile, daily_profile
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
    return html.Div(
        className="container-col full-width",
        children=[
            html.Div(
                className="container-row full-width align-center justify-center",
                children=[
                    html.H4(
                        className="text-next-to-input", children=["Select a variable: "]
                    ),
                    dropdown(
                        id=ElementIds.DROPDOWN,
                        className="dropdown-t-rh",
                        options={var: dropdown_names[var] for var in var_to_plot},
                        value=dropdown_names[var_to_plot[0]],
                    ),
                ],
            ),
            html.Div(
                className="container-col",
                children=[
                    html.Div(
                        children=title_with_link(
                            text=Text.YEARLY_CHART,
                            id_button="yearly-chart-label",
                            doc_link=DocLinks.TEMP_HUMIDITY_EXPLAINED,
                        ),
                    ),
                    dcc.Loading(
                        type=Type.CIRCLE,
                        children=html.Div(id=ElementIds.YEARLY_CHART),
                    ),
                    html.Div(
                        children=title_with_link(
                            text=Text.DAILY_CHART,
                            id_button=IdButtons.DAILY_CHART_LABEL,
                            doc_link=DocLinks.TEMP_HUMIDITY_EXPLAINED,
                        ),
                    ),
                    dcc.Loading(
                        type=Type.CIRCLE,
                        children=html.Div(id=ElementIds.DAILY),
                    ),
                    html.Div(
                        children=title_with_link(
                            text=Text.HEATMAP_CHART,
                            id_button="heatmap-chart-label",
                            doc_link=DocLinks.TEMP_HUMIDITY_EXPLAINED,
                        ),
                    ),
                    dcc.Loading(
                        type=Type.CIRCLE,
                        children=html.Div(id=ElementIds.HEATMAP),
                    ),
                    html.Div(
                        children=title_with_tooltip(
                            text=Text.DESCRIPTIVE_STATISTICS,
                            tooltip_text="count, mean, std, min, max, and percentiles",
                            id_button="table-tmp-rh",
                        ),
                    ),
                    html.Div(
                        id=ElementIds.TABLE_TMP_HUM,
                    ),
                ],
            ),
        ],
    )


@callback(
    Output(ElementIds.YEARLY_CHART, ComponentProperty.CHILDREN),
    [
        Input(ElementIds.DF_STORE, ComponentProperty.MODIFIED_TIMESTAMP),
        Input(ElementIds.GLOBAL_LOCAL_RADIO_INPUT, ComponentProperty.VALUE),
        Input(ElementIds.DROPDOWN, ComponentProperty.VALUE),
    ],
    [
        State(ElementIds.DF_STORE, ComponentProperty.DATA),
        State(ElementIds.META_STORE, ComponentProperty.DATA),
        State(ElementIds.SI_IP_UNIT_STORE, ComponentProperty.DATA),
    ],
)
def update_yearly_chart(_, global_local, dd_value, df, meta, si_ip):
    if dd_value == dropdown_names[var_to_plot[0]]:
        dbt_yearly = yearly_profile(df, "DBT", global_local, si_ip)
        dbt_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        units = generate_units_degree(si_ip)
        return dcc.Graph(
            config=generate_chart_name("DryBulbTemperature_yearly", meta, units),
            figure=dbt_yearly,
        )
    else:
        rh_yearly = yearly_profile(df, "RH", global_local, si_ip)
        rh_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        units = generate_units(si_ip)
        return dcc.Graph(
            config=generate_chart_name("RelativeHumidity_yearly", meta, units),
            figure=rh_yearly,
        )


@callback(
    Output(ElementIds.DAILY, ComponentProperty.CHILDREN),
    [
        Input(ElementIds.DF_STORE, ComponentProperty.MODIFIED_TIMESTAMP),
        Input(ElementIds.GLOBAL_LOCAL_RADIO_INPUT, ComponentProperty.VALUE),
        Input(ElementIds.DROPDOWN, ComponentProperty.VALUE),
    ],
    [
        State(ElementIds.DF_STORE, ComponentProperty.DATA),
        State(ElementIds.META_STORE, ComponentProperty.DATA),
        State(ElementIds.SI_IP_UNIT_STORE, ComponentProperty.DATA),
    ],
)
def update_daily(_, global_local, dd_value, df, meta, si_ip):
    if dd_value == dropdown_names[var_to_plot[0]]:
        units = generate_units_degree(si_ip)
        return dcc.Graph(
            config=generate_chart_name("DryBulbTemperature_daily", meta, units),
            figure=daily_profile(
                df[["DBT", "hour", "UTC_time", "month_names", "day", "month"]],
                "DBT",
                global_local,
                si_ip,
            ),
        )
    else:
        units = generate_units(si_ip)
        return dcc.Graph(
            config=generate_chart_name("RelativeHumidity_daily", meta, units),
            figure=daily_profile(
                df[["RH", "hour", "UTC_time", "month_names", "day", "month"]],
                "RH",
                global_local,
                si_ip,
            ),
        )


@callback(
    [Output(ElementIds.HEATMAP, ComponentProperty.CHILDREN)],
    [
        Input(ElementIds.DF_STORE, ComponentProperty.MODIFIED_TIMESTAMP),
        Input(ElementIds.GLOBAL_LOCAL_RADIO_INPUT, ComponentProperty.VALUE),
        Input(ElementIds.DROPDOWN, ComponentProperty.VALUE),
    ],
    [
        State(ElementIds.DF_STORE, ComponentProperty.DATA),
        State(ElementIds.META_STORE, ComponentProperty.DATA),
        State(ElementIds.SI_IP_UNIT_STORE, ComponentProperty.DATA),
    ],
)
def update_heatmap(_, global_local, dd_value, df, meta, si_ip):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    if dd_value == dropdown_names[var_to_plot[0]]:
        units = generate_units_degree(si_ip)
        return dcc.Graph(
            config=generate_chart_name("DryBulbTemperature_heatmap", meta, units),
            figure=heatmap(
                df[["DBT", "hour", "UTC_time", "month_names", "day"]],
                "DBT",
                global_local,
                si_ip,
            ),
        )
    else:
        units = generate_units(si_ip)
        return dcc.Graph(
            config=generate_chart_name("RelativeHumidity_heatmap", meta, units),
            figure=heatmap(
                df[["RH", "hour", "UTC_time", "month_names", "day"]],
                "RH",
                global_local,
                si_ip,
            ),
        )


@callback(
    Output(ElementIds.TABLE_TMP_HUM, ComponentProperty.CHILDREN),
    [
        Input(ElementIds.DF_STORE, ComponentProperty.MODIFIED_TIMESTAMP),
        Input(ElementIds.DROPDOWN, ComponentProperty.VALUE),
    ],
    [State(ElementIds.DF_STORE, ComponentProperty.DATA), State(ElementIds.SI_IP_UNIT_STORE, ComponentProperty.DATA)],
)
def update_table(_, dd_value, df, si_ip):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    return summary_table_tmp_rh_tab(
        df[["month", "hour", dd_value, "month_names"]], dd_value, si_ip
    )
