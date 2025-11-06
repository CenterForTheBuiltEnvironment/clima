import dash
import pandas as pd
import dash_mantine_components as dmc
import plotly.graph_objects as go
import requests

from dash.exceptions import PreventUpdate
from dash_extensions.enrich import dcc, Output, Input, State, callback
from config import PageUrls, DocLinks, PageInfo, UnitSystem
from pages.lib.charts_summary import world_map
from pages.lib.extract_df import get_data
from pages.lib.global_scheme import template, tight_margins
from pages.lib.template_graphs import violin
from pages.lib.global_variables import Variables, VariableInfo
from pages.lib.global_element_ids import ElementIds
from pages.lib.global_id_buttons import IdButtons
from pages.lib.global_tab_names import TabNames
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

    return dmc.Stack(
        id=ElementIds.TAB_TWO_CONTAINER,
        p="md",
        children=dmc.Skeleton(  # needed to avoid empty layout on load
            visible=True,
            height="100vh",
        ),
    )


@callback(
    Output(ElementIds.TAB_TWO_CONTAINER, "children"),
    [Input(ElementIds.ID_SUMMARY_SI_IP_RADIO_INPUT, "value")],
)
def update_layout(si_ip):
    if si_ip == UnitSystem.SI:
        heating_setpoint = 10
        cooling_setpoint = 18
    else:
        heating_setpoint = 50
        cooling_setpoint = 64

    return dmc.Stack(
        id=ElementIds.SUMMARY_SCE1_CONTAINER,
        children=[
            dmc.Skeleton(
                visible=False,
                children=dmc.Stack(
                    id=ElementIds.LOCATION_INFO,
                    children=[dmc.Text("info")]
                    * 10,  # placeholder text for height calc
                    gap=0,
                ),
            ),
            dmc.Skeleton(
                visible=False,
                h=300,
                children=dmc.Stack(id=ElementIds.WORLD_MAP),
            ),
            title_with_tooltip(
                text="Download",
                id_button=IdButtons.DOWNLOAD_BUTTON_LABEL,
                tooltip_text="Use the following buttons to download either the Clima sourcefile or the EPW file",
            ),
            dmc.Skeleton(
                visible=False,
                children=dmc.Group(
                    children=[
                        dmc.Button(
                            "Download EPW",
                            id=ElementIds.DOWN_EPW_BUTTON,
                            color="blue",
                            variant="filled",
                        ),
                        dmc.Button(
                            "Download Clima dataframe",
                            id=ElementIds.DOWNLOAD_BUTTON,
                            color="blue",
                            variant="filled",
                        ),
                        dcc.Download(id=ElementIds.DOWNLOAD_DATAFRAME_CSV),
                        dcc.Download(id=ElementIds.DOWNLOAD_EPW),
                    ],
                ),
            ),
            title_with_link(
                text="Heating and Cooling Degree Days",
                id_button=IdButtons.HDD_CDD_CHART,
                doc_link=DocLinks.DEGREE_DAYS,
            ),
            dmc.Stack(id=ElementIds.WARNING_CDD_HIGHER_HDD),
            dmc.Group(
                justify="center",
                children=[
                    dmc.Text("Heating degree day (HDD) setpoint"),
                    dmc.NumberInput(
                        id=ElementIds.INPUT_HDD_SET_POINT,
                        value=heating_setpoint,
                        step=1,
                        min=-100,
                        max=100,
                        w=80,
                        hideControls=False,
                    ),
                    dmc.Text("Cooling degree day (CDD) setpoint"),
                    dmc.NumberInput(
                        id=ElementIds.INPUT_CDD_SET_POINT,
                        value=cooling_setpoint,
                        step=1,
                        min=-100,
                        max=100,
                        w=80,
                        hideControls=False,
                    ),
                    dmc.Button(
                        id=ElementIds.SUBMIT_SET_POINTS,
                        children="Submit",
                        color="blue",
                        variant="filled",
                    ),
                ],
            ),
            dmc.Skeleton(
                visible=False,
                h=450,
                children=dmc.Stack(id=ElementIds.DEGREE_DAYS_CHART_WRAPPER),
            ),
            title_with_link(
                text="Climate Profiles",
                id_button=IdButtons.CLIMATE_PROFILES_CHART,
                doc_link=DocLinks.CLIMATE_PROFILES,
            ),
            dmc.Grid(
                id=ElementIds.GRAPH_CONTAINER,
                gutter="md",
                children=[
                    dmc.GridCol(
                        id=ElementIds.TEMP_PROFILE_GRAPH,
                        span={"base": 12, "sm": 6, "lg": 3},
                    ),
                    dmc.GridCol(
                        id=ElementIds.HUMIDITY_PROFILE_GRAPH,
                        span={"base": 12, "sm": 6, "lg": 3},
                    ),
                    dmc.GridCol(
                        id=ElementIds.SOLAR_RADIATION_GRAPH,
                        span={"base": 12, "sm": 6, "lg": 3},
                    ),
                    dmc.GridCol(
                        id=ElementIds.WIND_SPEED_GRAPH,
                        span={"base": 12, "sm": 6, "lg": 3},
                    ),
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
    return dcc.Graph(
        config=generate_chart_name(TabNames.MAP, meta),
        figure=world_map(meta),
    )


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
    location = (
        f"Location: {meta[Variables.CITY.col_name]}, {meta[Variables.COUNTRY.col_name]}"
    )
    lon = f"    Longitude: {meta[Variables.LON.col_name]}"
    lat = f"Latitude: {meta[Variables.LAT.col_name]}"

    site_elevation = round(float(meta[Variables.SITE_ELEVATION.col_name]), 2)
    if si_ip != UnitSystem.SI:
        site_elevation = round(site_elevation * 3.281, 2)
        elevation = f"Elevation above sea level: {site_elevation} ft"

    else:
        elevation = f"Elevation above sea level: {site_elevation} m"

    period = ""
    if meta[Variables.PERIOD.col_name]:
        start, stop = meta[Variables.PERIOD.col_name].split("-")
        period = f"This file is based on data collected between {start} and {stop}"

    climate_text = ""
    try:
        r = requests.get(
            f"http://climateapi.scottpinkelman.com/api/v1/location/{meta[Variables.LAT.col_name]}/{meta[Variables.LON.col_name]}"
        )
        if r.status_code == 200:
            j = r.json()["return_values"][0]
            climate_text = f"Köppen-Geiger climate zone: {j['koppen_geiger_zone']}. {j['zone_description']}."
    except Exception:
        pass

    # global horizontal irradiance
    # Note that the value is divided by 1000, so a corresponding change is made in the unit:
    total_solar_rad_value = round(df[Variables.GLOB_HOR_RAD.col_name].sum() / 1000, 2)
    total_solar_rad_unit = "k" + VariableInfo.from_col_name(
        Variables.GLOB_HOR_RAD.col_name
    ).get_unit(si_ip).replace("<sup>", "").replace("</sup>", "")
    total_solar_rad = f"Annual cumulative horizontal solar radiation: {total_solar_rad_value} {total_solar_rad_unit}"

    glob_sum = df[Variables.GLOB_HOR_RAD.col_name].sum()
    diffuse_percentage = (
        round(df[Variables.DIF_HOR_RAD.col_name].sum() / glob_sum * 100, 1)
        if glob_sum > 0
        else 0
    )
    total_diffuse_rad = (
        f"Percentage of diffuse horizontal solar radiation: {diffuse_percentage} %"
    )

    tmp_unit = VariableInfo.from_col_name(Variables.DBT.col_name).get_unit(si_ip)

    average_yearly_tmp = f"Average yearly temperature: {df[Variables.DBT.col_name].mean().round(1)} {tmp_unit}"
    hottest_yearly_tmp = f"Hottest yearly temperature (99%): {df[Variables.DBT.col_name].quantile(0.99).round(1)} {tmp_unit}"
    coldest_yearly_tmp = f"Coldest yearly temperature (1%): {df[Variables.DBT.col_name].quantile(0.01).round(1)} {tmp_unit}"

    return [
        dmc.Text(location, fw=700),
        dmc.Text(lon),
        dmc.Text(lat),
        dmc.Text(elevation),
        dmc.Text(period) if period else None,
        dmc.Text(climate_text) if climate_text else None,
        dmc.Text(average_yearly_tmp),
        dmc.Text(hottest_yearly_tmp),
        dmc.Text(coldest_yearly_tmp),
        dmc.Text(total_solar_rad),
        dmc.Text(total_diffuse_rad),
    ]


@callback(
    [
        Output(ElementIds.DEGREE_DAYS_CHART_WRAPPER, "children"),
        Output(ElementIds.WARNING_CDD_HIGHER_HDD, "is-open"),
    ],
    [
        Input(ElementIds.ID_SUMMARY_DF_STORE, "modified_timestamp"),
        Input(ElementIds.SUBMIT_SET_POINTS, "n_clicks"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_SUMMARY_DF_STORE, "data"),
        State(ElementIds.ID_SUMMARY_META_STORE, "data"),
        State(ElementIds.INPUT_HDD_SET_POINT, "value"),
        State(ElementIds.INPUT_CDD_SET_POINT, "value"),
        State(ElementIds.ID_SUMMARY_SI_IP_UNIT_STORE, "data"),
    ],
    prevent_initial_call=False,
)
def degree_day_chart(
    ts, n_clicks, global_filter_data, df, meta, hdd_value, cdd_value, si_ip
):
    """Redraw HDD/CDD chart only when Submit is clicked."""

    if df is None or meta is None:
        raise PreventUpdate

    if isinstance(df, (list, tuple, dict)):
        df = pd.DataFrame(df)

    # Apply global filter if active
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(
            df, global_filter_data, Variables.DBT.col_name
        )

    hdd_setpoint = hdd_value
    cdd_setpoint = cdd_value
    warning_setpoint = cdd_setpoint < hdd_setpoint

    color_hdd = "red"
    color_cdd = "dodgerblue"

    # Check if there's a filter marker
    has_filter_marker = "_is_filtered" in df.columns
    filtered_mask = None
    if has_filter_marker:
        filtered_mask = df["_is_filtered"]

    # Get original DBT values if available
    original_dbt_col = f"_{Variables.DBT.col_name}_original"
    use_original_for_filtered = has_filter_marker and original_dbt_col in df.columns

    hdd_array, cdd_array = [], []
    hdd_array_filtered, cdd_array_filtered = [], []
    months = df[Variables.MONTH_NAMES.col_name].unique()

    for i in range(1, 13):
        query_month = "month=="
        month_query = query_month + str(i)
        month_df = df.query(month_query)

        # Calculate HDD and CDD for unfiltered data
        if has_filter_marker and filtered_mask is not None:
            unfiltered_mask = ~month_df["_is_filtered"]
            unfiltered_dbt = month_df[Variables.DBT.col_name][unfiltered_mask]
        else:
            unfiltered_dbt = month_df[Variables.DBT.col_name]

        # Calculate HDD for unfiltered data
        a_unfiltered_hdd = unfiltered_dbt[unfiltered_dbt <= hdd_setpoint].sub(
            hdd_setpoint
        )
        hdd_array.append(int(a_unfiltered_hdd.sum(skipna=True) / 24))

        # Calculate CDD for unfiltered data
        a_unfiltered_cdd = unfiltered_dbt[unfiltered_dbt >= cdd_setpoint].sub(
            cdd_setpoint
        )
        cdd_array.append(int(a_unfiltered_cdd.sum(skipna=True) / 24))

        # Calculate HDD and CDD for filtered data (if any)
        if (
            has_filter_marker
            and filtered_mask is not None
            and month_df["_is_filtered"].any()
        ):
            filtered_mask_month = month_df["_is_filtered"]

            if use_original_for_filtered:
                # Use original DBT values for filtered data
                month_indices = month_df[filtered_mask_month].index
                filtered_dbt = df.loc[month_indices, original_dbt_col]
            else:
                # Fallback to current DBT values (shouldn't happen if filter is applied correctly)
                filtered_dbt = month_df[Variables.DBT.col_name][filtered_mask_month]

            # Calculate HDD for filtered data
            a_filtered_hdd = filtered_dbt[filtered_dbt <= hdd_setpoint].sub(
                hdd_setpoint
            )
            hdd_array_filtered.append(int(a_filtered_hdd.sum(skipna=True) / 24))

            # Calculate CDD for filtered data
            a_filtered_cdd = filtered_dbt[filtered_dbt >= cdd_setpoint].sub(
                cdd_setpoint
            )
            cdd_array_filtered.append(int(a_filtered_cdd.sum(skipna=True) / 24))
        else:
            hdd_array_filtered.append(0)
            cdd_array_filtered.append(0)

    traces = []

    # Add filtered data traces (gray) if any filtered data exists
    if has_filter_marker and filtered_mask is not None and filtered_mask.any():
        trace_cdd_filtered = go.Bar(
            x=months,
            y=cdd_array_filtered,
            name="Cooling Degree Days (Filtered)",
            marker_color="gray",
            customdata=cdd_array_filtered,
            hovertemplate="<b>Filtered Data</b><br>Cooling Degree Days: <br>%{customdata} per month<br><extra></extra>",
        )
        traces.append(trace_cdd_filtered)

        trace_hdd_filtered = go.Bar(
            x=months,
            y=hdd_array_filtered,
            name="Heating Degree Days (Filtered)",
            marker_color="lightgray",
            customdata=[abs(x) for x in hdd_array_filtered],
            hovertemplate="<b>Filtered Data</b><br>Heating Degree Days: <br>%{customdata} per month<br><extra></extra>",
        )
        traces.append(trace_hdd_filtered)

    # Add unfiltered data traces (normal colors)
    trace2 = go.Bar(
        x=months,
        y=cdd_array,
        name="Cooling Degree Days",
        marker_color=color_cdd,
        customdata=cdd_array,
        hovertemplate="Cooling Degree Days: <br>%{customdata} per month<br><extra></extra>",
    )
    traces.append(trace2)

    trace1 = go.Bar(
        x=months,
        y=hdd_array,
        name="Heating Degree Days",
        marker_color=color_hdd,
        customdata=[abs(x) for x in hdd_array],
        hovertemplate="Heating Degree Days: <br>%{customdata} per month<br><extra></extra>",
    )
    traces.append(trace1)

    fig = go.Figure(data=traces)
    fig.update_layout(
        barmode="relative",
        margin=tight_margins,
        template=template,
        dragmode=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", mirror=True)

    custom_inputs = f"{hdd_value}-{cdd_value}"
    units = generate_units_degree(si_ip)

    chart = dcc.Graph(
        id=ElementIds.DEGREE_DAYS_CHART,
        config=generate_chart_name(TabNames.HDD_CDD, meta, custom_inputs, units),
        figure=fig,
    )

    alert_children = (
        dmc.Alert(
            "WARNING: Invalid Results! The CDD setpoint should be higher than the HDD setpoint!",
            color="yellow",
            variant="filled",
            title="Warning",
            withCloseButton=True,
        )
        if warning_setpoint
        else None
    )

    return chart, alert_children


@callback(
    Output(ElementIds.TEMP_PROFILE_GRAPH, "children"),
    [
        Input(ElementIds.ID_SUMMARY_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_SUMMARY_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_SUMMARY_DF_STORE, "data"),
        State(ElementIds.ID_SUMMARY_META_STORE, "data"),
        State(ElementIds.ID_SUMMARY_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_violin_tdb(ts, global_local, global_filter_data, df, meta, si_ip):
    # Apply global filter if active
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(
            df, global_filter_data, Variables.DBT.col_name
        )
    units = generate_units_degree(si_ip)
    return dcc.Graph(
        id=ElementIds.TDB_PROFILE_GRAPH,
        config=generate_chart_name(TabNames.DRY_BULB_TEMPERATURE, meta, units),
        figure=violin(df, Variables.DBT.col_name, global_local, si_ip),
    )


@callback(
    Output(ElementIds.WIND_SPEED_GRAPH, "children"),
    [
        Input(ElementIds.ID_SUMMARY_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_SUMMARY_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_SUMMARY_DF_STORE, "data"),
        State(ElementIds.ID_SUMMARY_META_STORE, "data"),
        State(ElementIds.ID_SUMMARY_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_wind(ts, global_local, global_filter_data, df, meta, si_ip):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(
            df, global_filter_data, Variables.WIND_SPEED.col_name
        )
    units = generate_units(si_ip)
    return dcc.Graph(
        id=ElementIds.WIND_PROFILE_GRAPH,
        config=generate_chart_name(TabNames.WIND_SPEED, meta, units),
        figure=violin(df, Variables.WIND_SPEED.col_name, global_local, si_ip),
    )


@callback(
    Output(ElementIds.HUMIDITY_PROFILE_GRAPH, "children"),
    [
        Input(ElementIds.ID_SUMMARY_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_SUMMARY_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_SUMMARY_DF_STORE, "data"),
        State(ElementIds.ID_SUMMARY_META_STORE, "data"),
        State(ElementIds.ID_SUMMARY_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_rh(ts, global_local, global_filter_data, df, meta, si_ip):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(
            df, global_filter_data, Variables.RH.col_name
        )
    units = generate_units(si_ip)
    return dcc.Graph(
        id=ElementIds.RH_PROFILE_GRAPH,
        config=generate_chart_name(TabNames.RELATIVE_HUMIDITY, meta, units),
        figure=violin(df, Variables.RH.col_name, global_local, si_ip),
    )


@callback(
    Output(ElementIds.SOLAR_RADIATION_GRAPH, "children"),
    [
        Input(ElementIds.ID_SUMMARY_DF_STORE, "modified_timestamp"),
        Input(ElementIds.ID_SUMMARY_GLOBAL_LOCAL_RADIO_INPUT, "value"),
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    [
        State(ElementIds.ID_SUMMARY_DF_STORE, "data"),
        State(ElementIds.ID_SUMMARY_META_STORE, "data"),
        State(ElementIds.ID_SUMMARY_SI_IP_UNIT_STORE, "data"),
    ],
)
def update_tab_gh_rad(ts, global_local, global_filter_data, df, meta, si_ip):
    """Update the contents of tab two. Passing in the general info (df, meta)."""
    if global_filter_data and global_filter_data.get("filter_active", False):
        from pages.lib.layout import apply_global_month_hour_filter

        df = apply_global_month_hour_filter(
            df, global_filter_data, Variables.GLOB_HOR_RAD.col_name
        )
    units = generate_units(si_ip)
    return dcc.Graph(
        id=ElementIds.GH_RAD_PROFILE_GRAPH,
        config=generate_chart_name(TabNames.GLOBAL_HORIZONTAL_RADIATION, meta, units),
        figure=violin(df, Variables.GLOB_HOR_RAD.col_name, global_local, si_ip),
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
                df.to_csv,
                f"df_{meta[Variables.CITY.col_name]}_{meta[Variables.COUNTRY.col_name]}_Clima_SIunit.csv",
            )
        else:
            return dcc.send_data_frame(
                df.to_csv,
                f"df_{meta[Variables.CITY.col_name]}_{meta[Variables.COUNTRY.col_name]}_Clima_IPunit.csv",
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
            filename=f"{meta[Variables.CITY.col_name]}_{meta[Variables.COUNTRY.col_name]}.epw",
        )
    else:
        raise PreventUpdate
