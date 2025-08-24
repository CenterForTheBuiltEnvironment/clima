import dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import dcc, html, Output, Input, State, callback

import plotly.graph_objects as go
import requests

from config import PageUrls, DocLinks, PageInfo, UnitSystem
from pages.lib.charts_summary import world_map
from pages.lib.extract_df import get_data
from pages.lib.global_scheme import template, tight_margins, mapping_dictionary
from pages.lib.template_graphs import violin
from pages.lib.global_column_names import ColNames
from pages.lib.global_elementids import ElementIds
from pages.lib.utils import (
    generate_chart_name,
    generate_units,
    generate_units_degree,
    title_with_tooltip,
    title_with_link,
)


dash.register_page(
    __name__,
    name=PageInfo.SUMMARY_NAME,
    path=PageUrls.SUMMARY.value,
    order=PageInfo.SUMMARY_ORDER,
)


def layout():
    """Contents in the second tab 'Climate Summary'."""

    return html.Div(
        className="container-col",
        id="tab-two-container",
        children=[
            #
        ],
    )


@callback(
    Output(ElementIds.TABLE_TWO_CONTAINER, "children"), [Input(ElementIds.ID_SUMMARY_SI_IP_RADIO_INPUT, "value")]
)
def update_layout(si_ip):
    if si_ip == UnitSystem.SI:
        heating_setpoint = 10
        cooling_setpoint = 18
    else:
        heating_setpoint = 50
        cooling_setpoint = 64

    return html.Div(
        className="container-col",
        id=ElementIds.TAB2_SCE1_CONTAINER,
        children=[
            dcc.Loading(
                type="circle",
                children=html.Div(
                    className="container-col",
                    id=ElementIds.LOCATION_INFO,
                    style={"padding": "12px"},
                ),
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(className="tab-two-section", id=ElementIds.WORLD_MAP),
            ),
            html.Div(
                children=title_with_tooltip(
                    text="Download",
                    id_button="download-button-label",
                    tooltip_text="Use the following buttons to download either the Clima sourcefile or the EPW file",
                ),
            ),
            dcc.Loading(
                type="circle",
                children=dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "Download EPW",
                                color="primary",
                                id=ElementIds.DOWN_EPW_BUTTON,
                            ),
                            width="auto",
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Download Clima dataframe",
                                color="primary",
                                id=ElementIds.DOWNLOAD_BUTTON,
                            ),
                            width="auto",
                        ),
                        dbc.Col(
                            [
                                dcc.Download(id=ElementIds.DOWNLOAD_DATAFRAME_CSV),
                                dcc.Download(id=ElementIds.DOWNLOAD_EPW),
                            ],
                            width=1,
                        ),
                    ],
                ),
            ),
            html.Div(
                children=title_with_link(
                    text="Heating and Cooling Degree Days",
                    id_button="hdd-cdd-chart",
                    doc_link=DocLinks.DEGREE_DAYS,
                ),
            ),
            dbc.Alert(
                "WARNING: Invalid Results! The CDD setpoint should be higher than the HDD setpoint!",
                color="warning",
                is_open=False,
                id=ElementIds.WARNING_CDD_HIGHER_HDD,
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Label(
                            "Heating degree day (HDD) setpoint",
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        dbc.Input(
                            id=ElementIds.INPUT_HDD_SET_POINT,
                            type="number",
                            value=heating_setpoint,
                            style={"width": "4rem"},
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        html.Label(
                            "Cooling degree day (CDD) setpoint",
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        dbc.Input(
                            id=ElementIds.INPUT_CDD_SET_POINT,
                            type="number",
                            value=cooling_setpoint,
                            style={"width": "4rem"},
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        dbc.Button(
                            id=ElementIds.SUBMIT_SET_POINTS,
                            children="Submit",
                            color="primary",
                        ),
                        width="auto",
                    ),
                ],
                align="center",
                justify="center",
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(id=ElementIds.DEGREE_DAYS_CHART_WRAPPER),
            ),
            html.Div(
                children=title_with_link(
                    text="Climate Profiles",
                    id_button="climate-profiles-chart",
                    doc_link=DocLinks.CLIMATE_PROFILES,
                ),
            ),
            dbc.Row(
                id=ElementIds.GRAPH_CONTAINER,
                children=[
                    dbc.Col(id=ElementIds.TEMP_PROFILE_GRAPH, width=12, md=6, lg=3),
                    dbc.Col(id=ElementIds.HUMIDITY_PROFILE_GRAPH, width=12, md=6, lg=3),
                    dbc.Col(id=ElementIds.SOLAR_RADIATION_GRAPH, width=12, md=6, lg=3),
                    dbc.Col(id=ElementIds.WIND_SPEED_GRAPH, width=12, md=6, lg=3),
                ],
            ),
        ],
    )


# @callback(
#     [Output('input-hdd-set-point', 'value'), Output('input-cdd-set-point', 'value')],
#     [Input('si-ip-radio-input', 'value')]
# )
# def update_setpoints(si_ip_unit_store_data):
#     if si_ip_unit_store_data == 'si':
#         return 10, 18
#     else:
#         return 50, 64


@callback(
    Output(ElementIds.WORLD_MAP, "children"),
    Input(ElementIds.ID_SUMMARY_META_STORE, "data"),
)
def update_map(meta):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    map_world = dcc.Graph(
        id=ElementIds.GH_RAD_PROFILE_GRAPH,
        config=generate_chart_name("map", meta),
        figure=world_map(meta),
    )

    return map_world


@callback(
    Output(ElementIds.LOCATION_INFO, "children"),
    Input(ElementIds.ID_SUMMARY_DF_STORE, "modified_timestamp"),
    [
        State(ElementIds.ID_SUMMARY_DF_STORE, "data"),
        State(ElementIds.ID_SUMMARY_META_STORE, "data"),
        State(ElementIds.ID_SUMMARY_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_location_info(ts, df, meta, si_ip):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    location = f"Location: {meta['city']}, {meta['country']}"
    lon = f"Longitude: {meta['lon']}"
    lat = f"Latitude: {meta['lat']}"

    site_elevation = float(meta["site_elevation"])
    site_elevation = round(site_elevation, 2)
    if si_ip != UnitSystem.SI:
        site_elevation = site_elevation * 3.281
        site_elevation = round(site_elevation, 2)
        elevation = f"Elevation above sea level: {str(site_elevation)} ft"
    else:
        elevation = f"Elevation above sea level: {meta['site_elevation']} m"
    period = ""
    if meta["period"]:
        start, stop = meta["period"].split("-")
        period = f"This file is based on data collected between {start} and {stop}"

    r = requests.get(
        f"http://climateapi.scottpinkelman.com/api/v1/location/{meta['lat']}/{meta['lon']}"
    )

    climate_text = ""
    if r.status_code == 200:
        try:
            climate_zone = r.json()["return_values"][0]["koppen_geiger_zone"]
            zone_description = r.json()["return_values"][0]["zone_description"]

            climate_text = (
                f"Köppen–Geiger climate zone: {climate_zone}. {zone_description}."
            )
        except KeyError:
            pass

    # global horizontal irradiance
    # Note that the value is divided by 1000, so a corresponding change is made in the unit:
    total_solar_rad_value = round(df["glob_hor_rad"].sum() / 1000, 2)
    total_solar_rad_unit = "k" + mapping_dictionary["glob_hor_rad"][si_ip]["unit"]
    total_solar_rad = f"Annual cumulative horizontal solar radiation: {total_solar_rad_value} {total_solar_rad_unit}"

    glob_sum = df["glob_hor_rad"].sum()
    if glob_sum > 0:
        diffuse_percentage = round(df["dif_hor_rad"].sum() / glob_sum * 100, 1)
    else:
        diffuse_percentage = 0
    total_diffuse_rad = (
        f"Percentage of diffuse horizontal solar radiation: {diffuse_percentage} %"
    )
    tmp_unit = mapping_dictionary[ColNames.DBT][si_ip]["unit"]
    average_yearly_tmp = (
        f"Average yearly temperature: {df['DBT'].mean().round(1)} " + tmp_unit
    )
    hottest_yearly_tmp = (
        f"Hottest yearly temperature (99%): {df['DBT'].quantile(0.99).round(1)} "
        + tmp_unit
    )
    coldest_yearly_tmp = (
        f"Coldest yearly temperature (1%): {df['DBT'].quantile(0.01).round(1)} "
        + tmp_unit
    )

    location_info = dbc.Col(
        [
            dbc.Row(location, style={"fontWeight": "bold"}),
            dbc.Row(lon),
            dbc.Row(lat),
            dbc.Row(elevation),
            dbc.Row(period),
            dbc.Row(climate_text),
            dbc.Row(average_yearly_tmp),
            dbc.Row(hottest_yearly_tmp),
            dbc.Row(coldest_yearly_tmp),
            dbc.Row(
                dcc.Markdown(
                    dangerously_allow_html=True,
                    children=[total_solar_rad],
                    style={"padding": 0},
                )
            ),
            dbc.Row(total_diffuse_rad),
        ],
    )

    return location_info


@callback(
    [
        Output(ElementIds.DEGREE_DAYS_CHART_WRAPPER, "children"),
        Output(ElementIds.WARNING_CDD_HIGHER_HDD, "is_open"),
    ],
    [
        Input(ElementIds.ID_SUMMARY_DF_STORE, "modified_timestamp"),
        Input(ElementIds.SUBMIT_SET_POINTS, "n_clicks_timestamp"),
    ],
    [
        State(ElementIds.ID_SUMMARY_DF_STORE, "data"),
        State(ElementIds.ID_SUMMARY_META_STORE, "data"),
        State(ElementIds.INPUT_HDD_SET_POINT, "value"),
        State(ElementIds.INPUT_CDD_SET_POINT, "value"),
        State(ElementIds.SUBMIT_SET_POINTS, "n_clicks"),
        State(ElementIds.ID_SUMMARY_SI_IP_UNIT_STORE, "data"),
    ],
)
def degree_day_chart(ts, ts_click, df, meta, hdd_value, cdd_value, n_clicks, si_ip):
    """Update the contents of tab two. Passing in the general info (df, meta)."""

    ctx = dash.callback_context

    if (
        ctx.triggered[0]["prop_id"] == "submit-set-points.n_clicks_timestamp"
        or n_clicks is None
    ):
        hdd_setpoint = hdd_value
        cdd_setpoint = cdd_value

        warning_setpoint = False
        if cdd_setpoint < hdd_setpoint:
            warning_setpoint = True

        color_hdd = "red"
        color_cdd = "dodgerblue"

        hdd_array = []
        cdd_array = []
        months = df[ColNames.MONTH_NAMES].unique()

        for i in range(1, 13):
            query_month = "month=="

            # calculates HDD per month
            query = query_month + str(i) + " and DBT<=" + str(hdd_setpoint)
            a = df.query(query)[ColNames.DBT].sub(hdd_setpoint)
            hdd = a.sum(axis=0, skipna=True)
            hdd = hdd / 24
            hdd = int(hdd)
            hdd_array.append(hdd)

            # calculates CDD per month
            query = query_month + str(i) + " and DBT>=" + str(cdd_setpoint)
            a = df.query(query)[ColNames.DBT].sub(cdd_setpoint)
            cdd = a.sum(axis=0, skipna=True)
            cdd = cdd / 24
            cdd = int(cdd)
            cdd_array.append(cdd)

        trace1 = go.Bar(
            x=months,
            y=hdd_array,
            name="Heating Degree Days",
            marker_color=color_hdd,
            customdata=[abs(ele) for ele in hdd_array],
            hovertemplate=(
                " Heating Degree Days: <br>%{customdata} per month<br><extra></extra>"
            ),
        )
        trace2 = go.Bar(
            x=months,
            y=cdd_array,
            name="Cooling Degree Days",
            marker_color=color_cdd,
            customdata=cdd_array,
            hovertemplate=(
                "Cooling Degree Days: <br>%{customdata} per month<br><extra></extra>"
            ),
        )

        data = [trace2, trace1]

        fig = go.Figure(
            data=data,
        )
        fig.update_layout(
            barmode="relative",
            margin=tight_margins,
            template=template,
            dragmode=False,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1
            ),
        )

        fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
        fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)

        custom_inputs = f"{hdd_value}-{cdd_value}"
        units = generate_units_degree(si_ip)

        chart = dcc.Graph(
            id="degree-days-chart",
            config=generate_chart_name("hdd_cdd", meta, custom_inputs, units),
            figure=fig,
        )

        return chart, warning_setpoint


@callback(
    Output(ElementIds.TEMP_PROFILE_GRAPH, "children"),
    [
        Input(ElementIds.ID_SUMMARY_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_SUMMARY_GLOBAL_LOCAL_RADIO_INPUT, "value"),
    ],
    [
        State(ElementIds.ID_SUMMARY_DF_STORE, "data"),
        State(ElementIds.ID_SUMMARY_META_STORE, "data"),
        State(ElementIds.ID_SUMMARY_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_violin_tdb(ts, global_local, df, meta, si_ip):
    units = generate_units_degree(si_ip)
    return dcc.Graph(
        id=ElementIds.TDB_PROFILE_GRAPH,
        className="violin-container",
        config=generate_chart_name("DryBulbTemperature", meta, units),
        figure=violin(df, ColNames.DBT, global_local, si_ip),
    )


@callback(
    Output(ElementIds.WIND_SPEED_GRAPH, "children"),
    [
        Input(ElementIds.ID_SUMMARY_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_SUMMARY_GLOBAL_LOCAL_RADIO_INPUT, "value"),
    ],
    [
        State(ElementIds.ID_SUMMARY_DF_STORE, "data"),
        State(ElementIds.ID_SUMMARY_META_STORE, "data"),
        State(ElementIds.ID_SUMMARY_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_wind(ts, global_local, df, meta, si_ip):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    units = generate_units(si_ip)
    return dcc.Graph(
        id="wind-profile-graph",
        className="violin-container",
        config=generate_chart_name("WindSpeed", meta, units),
        figure=violin(df, ColNames.WIND_SPEED, global_local, si_ip),
    )


@callback(
    Output(ElementIds.HUMIDITY_PROFILE_GRAPH, "children"),
    [
        Input(ElementIds.ID_SUMMARY_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_SUMMARY_GLOBAL_LOCAL_RADIO_INPUT, "value"),
    ],
    [
        State(ElementIds.ID_SUMMARY_DF_STORE, "data"),
        State(ElementIds.ID_SUMMARY_META_STORE, "data"),
        State(ElementIds.ID_SUMMARY_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_rh(ts, global_local, df, meta, si_ip):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    units = generate_units(si_ip)
    return dcc.Graph(
        id=ElementIds.RH_PROFILE_GRAPH,
        className="violin-container",
        config=generate_chart_name("RelativeHumidity", meta, units),
        figure=violin(df, ColNames.RH, global_local, si_ip),
    )


@callback(
    Output(ElementIds.SOLAR_RADIATION_GRAPH, "children"),
    [
        Input(ElementIds.ID_SUMMARY_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_SUMMARY_GLOBAL_LOCAL_RADIO_INPUT, "value"),
    ],
    [
        State(ElementIds.ID_SUMMARY_DF_STORE, "data"),
        State(ElementIds.ID_SUMMARY_META_STORE, "data"),
        State(ElementIds.ID_SUMMARY_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_gh_rad(ts, global_local, df, meta, si_ip):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    units = generate_units(si_ip)
    return dcc.Graph(
        id=ElementIds.GH_RAD_PROFILE_GRAPH,
        className="violin-container",
        config=generate_chart_name("GlobalHorizontalRadiation", meta, units),
        figure=violin(df, ColNames.GLOB_HOR_RAD, global_local, si_ip),
    )


@callback(
    Output(ElementIds.DOWNLOAD_DATAFRAME_CSV, "data"),
    [Input(ElementIds.DOWNLOAD_BUTTON, "n_clicks")],
    [
        State(ElementIds.ID_SUMMARY_DF_STORE, "data"),
        State(ElementIds.ID_SUMMARY_META_STORE, "data"),
        State(ElementIds.ID_SUMMARY_SI_IP_UNIT_STORE, "data"),
    ],
    prevent_initial_call=True,
)
def download_clima_dataframe(n_clicks, df, meta, si_ip):
    if n_clicks is None:
        raise PreventUpdate
    elif df is not None:
        if si_ip == UnitSystem.SI:
            return dcc.send_data_frame(
                df.to_csv, f"df_{meta['city']}_{meta['country']}_Clima_SIunit.csv"
            )
        else:
            return dcc.send_data_frame(
                df.to_csv, f"df_{meta['city']}_{meta['country']}_Clima_IPunit.csv"
            )
    else:
        print("df not loaded yet")


@callback(
    Output(ElementIds.DOWNLOAD_EPW, "data"),
    [Input(ElementIds.DOWN_EPW_BUTTON, "n_clicks")],
    [State(ElementIds.ID_SUMMARY_META_STORE, "data")],
    prevent_initial_call=True,
)
def download_epw(n_clicks, meta):
    if n_clicks is None:
        raise PreventUpdate
    elif meta is not None:
        lines = get_data(meta["url"])
        lines = [x.strip().replace("\\r", "") for x in lines[:-1]]
        lines[0] = lines[0].replace("b'", "")
        return dict(
            content="\n".join(lines),
            filename=f"{meta['city']}_{meta['country']}.epw",
        )
    else:
        raise PreventUpdate
