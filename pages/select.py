import base64
import json
import re

import dash
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Serverside, Output, Input, State, html, dcc, callback
from pandas import json_normalize

from pages.lib.extract_df import convert_df_units
from pages.lib.extract_df import create_df, get_data, get_location_info
from pages.lib.global_variables import Variables
from pages.lib.global_element_ids import ElementIds
from pages.lib.global_tab_names import TabNames
from config import PageUrls, PageInfo
from pages.lib.utils import generate_chart_name, get_default_global_filter_store_data

dash.register_page(
    __name__,
    name=PageInfo.SELECT_NAME,
    path=PageUrls.SELECT.value,
    order=PageInfo.SELECT_ORDER,
)


messages_alert = {
    "start": "To start, upload an EPW file or click on a point on the map!",
    "not_available": "The EPW for this location is not available",
    "success": "The EPW was successfully loaded!",
    "invalid_format": "The format of the EPW file you have uploaded is invalid.",
    "wrong_extension": "The file you have uploaded is not an EPW file",
}


def layout():
    """Contents in the first tab 'Select Weather File'"""
    return dmc.Stack(
        p="md",
        children=[
            dcc.Loading(
                custom_spinner=dmc.Skeleton(visible=True, h="100%"),
                fullscreen=True,
                children=alert(),
            ),
            dcc.Upload(
                id=ElementIds.UPLOAD_DATA,
                children=dmc.Button(
                    [
                        "Drag and Drop or ",
                        html.A("Select an EPW file from your computer"),
                    ],
                    id=ElementIds.UPLOAD_DATA_BUTTON,
                    variant="outline",
                    color="gray",
                    style={"borderStyle": "dashed"},
                    styles={"label": {"fontWeight": 400}},
                ),
                # Allow multiple files to be uploaded
                multiple=True,
                style={"display": "grid"},
            ),
            dmc.Skeleton(
                visible=False,
                id=ElementIds.SKELETON_GRAPH_CONTAINER,
                height=500,
                children=dmc.Box(id=ElementIds.TAB_ONE_MAP),
            ),
            dmc.Modal(
                id=ElementIds.MODAL,
                title=dmc.Text(id=ElementIds.MODAL_HEADER),
                opened=False,
                centered=True,
                children=[
                    dmc.Divider(
                        size="xs",
                        color="gray",
                        my="sm",
                        style={
                            "borderTop": "1px solid var(--mantine-color-gray-4)",
                            "marginTop": "-6px",
                        },
                    ),
                    dmc.Group(
                        [
                            dmc.Button(
                                "Close",
                                id=ElementIds.MODAL_CLOSE_BUTTON,
                                color="gray",
                                variant="outline",
                            ),
                            dmc.Button(
                                "Yes",
                                id=ElementIds.MODAL_YES_BUTTON,
                                color="blue",
                            ),
                        ],
                        justify="flex-end",
                    ),
                ],
            ),
        ],
    )


def alert():
    """Alert layout for the submit button."""
    return dmc.Alert(
        messages_alert["start"],
        color="blue",
        id=ElementIds.ALERT,
        withCloseButton=False,
        style={"maxHeight": "66px"},
    )


# add si-ip and map dictionary in the output
@callback(
    [
        Output(ElementIds.ID_SELECT_META_STORE, "data"),
        Output(ElementIds.ID_SELECT_LINES_STORE, "data"),
        Output(ElementIds.ALERT, "visible"),
        Output(ElementIds.ALERT, "children"),
        Output(ElementIds.ALERT, "color"),
        Output(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data", allow_duplicate=True),
    ],
    [
        Input(ElementIds.MODAL_YES_BUTTON, "n_clicks"),
        Input(ElementIds.UPLOAD_DATA_BUTTON, "n_clicks"),
        Input(ElementIds.UPLOAD_DATA, "contents"),
    ],
    [
        State(ElementIds.UPLOAD_DATA, "filename"),
        State(ElementIds.ID_SELECT_URL_STORE, "data"),
    ],
    prevent_initial_call=True,
)
# @code_timer
def submitted_data(
    _,
    __,
    list_of_contents,
    list_of_names,
    url_store,
):
    """Process the uploaded file or download the EPW from the URL"""
    ctx = dash.callback_context

    if ctx.triggered[0][Variables.PROP_ID.col_name] == "modal-yes-button.n_clicks":
        lines = get_data(url_store)
        if lines is None:
            return (
                None,
                None,
                True,
                messages_alert["not_available"],
                "orange",
                get_default_global_filter_store_data(),
            )
        location_info = get_location_info(
            lines, url_store
        )  # we might need to split this call into two, one returns df and one returns location_info
        return (
            location_info,
            lines,
            True,
            messages_alert["success"],
            "green",
            get_default_global_filter_store_data(),
        )

    elif (
        ctx.triggered[0][Variables.PROP_ID.col_name] == "upload-data.contents"
        and list_of_contents is not None
    ):
        content_type, content_string = list_of_contents[0].split(",")

        decoded_bytes = base64.b64decode(content_string)
        try:
            if "epw" in list_of_names[0]:
                # Assume that the user uploaded a CSV file
                try:
                    decoded_string = decoded_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    decoded_string = decoded_bytes.decode("latin-1")
                lines = decoded_string.split("\n")
                df, location_info = create_df(lines, list_of_names[0])
                return (
                    location_info,
                    lines,
                    True,
                    messages_alert["success"],
                    "green",
                    get_default_global_filter_store_data(),
                )
            else:
                return (
                    None,
                    None,
                    True,
                    messages_alert["invalid_format"],
                    "orange",
                    get_default_global_filter_store_data(),
                )
        except (ValueError, IndexError, KeyError) as e:
            print(f"Error parsing EPW file: {e}")
            return (
                None,
                None,
                True,
                messages_alert["wrong_extension"],
                "orange",
                get_default_global_filter_store_data(),
            )
    raise PreventUpdate


# add switch_si_ip function and convert the data-store
@callback(
    [
        Output(ElementIds.ID_SELECT_DF_STORE, "data"),
        Output(ElementIds.ID_SELECT_SI_IP_UNIT_STORE, "data"),
    ],
    [
        Input(ElementIds.ID_SELECT_LINES_STORE, "modified_timestamp"),
        Input(ElementIds.ID_SELECT_SI_IP_RADIO_INPUT, "value"),
    ],
    [
        State(ElementIds.ID_SELECT_URL_STORE, "data"),
        State(ElementIds.ID_SELECT_LINES_STORE, "data"),
    ],
)
def switch_si_ip(_, si_ip_input, url_store, lines):
    if lines is not None:
        df, _ = create_df(lines, url_store)

        df = convert_df_units(df, si_ip_input)

        return Serverside(df), si_ip_input
    else:
        return (
            None,
            None,
        )


@callback(
    [
        Output(ElementIds.NAV, "disabled"),
        Output(ElementIds.NAV_SUMMARY, "disabled"),
        Output(ElementIds.NAV_T_RH, "disabled"),
        Output(ElementIds.NAV_SUN, "disabled"),
        Output(ElementIds.NAV_WIND, "disabled"),
        Output(ElementIds.NAV_PSY_CHART, "disabled"),
        Output(ElementIds.NAV_EXPLORER, "disabled"),
        Output(ElementIds.NAV_OUTDOOR, "disabled"),
        Output(ElementIds.NAV_NATURAL_VENTILATION, "disabled"),
        Output(ElementIds.ID_SELECT_BANNER_SUBTITLE, "children"),
    ],
    [
        Input(ElementIds.ID_SELECT_META_STORE, "data"),
        Input(ElementIds.ID_SELECT_DF_STORE, "data"),
    ],
)
def enable_tabs_when_data_is_loaded(meta, data):
    """Hide tabs when data are not loaded"""
    default = "Current Location: N/A"
    if data is None:
        return (
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            default,
        )
    else:
        return (
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            "Current Location: "
            + meta[Variables.CITY.col_name]
            + ", "
            + meta[Variables.COUNTRY.col_name],
        )


@callback(
    [
        Output(ElementIds.MODAL, "opened"),
        Output(ElementIds.ID_SELECT_URL_STORE, "data"),
    ],
    [
        Input(ElementIds.MODAL_YES_BUTTON, "n_clicks"),
        Input(ElementIds.TAB_ONE_MAP, "clickData"),
        Input(ElementIds.MODAL_CLOSE_BUTTON, "n_clicks"),
    ],
    [State(ElementIds.MODAL, "opened")],
    prevent_initial_call=True,
)
def display_modal_when_data_clicked(_, click_map, __, opened):
    """display the modal to the user and check if he wants to use that file"""
    if click_map:
        url = re.search(
            r'href=[\'"]?([^\'" >]+)', click_map["points"][0]["customdata"][-1]
        ).group(1)
        return not opened, url
    return opened, ""


@callback(
    [Output(ElementIds.MODAL_HEADER, "children")],
    [Input(ElementIds.TAB_ONE_MAP, "clickData")],
    prevent_initial_call=True,
)
def change_text_modal(click_map):
    if click_map:
        return [f"Analyse data from {click_map['points'][0]['hovertext']}?"]
    return ["Analyse data from this location?"]


@callback(
    Output(ElementIds.SKELETON_GRAPH_CONTAINER, "children"),
    Input(ElementIds.SELECT_URL, "pathname"),
)
def plot_location_epw_files(pathname):
    # print(pathname)
    if pathname != "/":
        raise PreventUpdate

    with open("./assets/data/epw_location.json", encoding="utf8") as data_file:
        data = json.load(data_file)

    df = json_normalize(data[Variables.FEATURES.col_name])
    df[[Variables.LON.col_name, Variables.LAT.col_name]] = pd.DataFrame(
        df[Variables.GEOMETRY_COORDINATES.col_name].tolist()
    )
    df[Variables.LAT.col_name] += 0.010
    df = df.rename(columns={"properties.epw": "Source"})

    fig = px.scatter_mapbox(
        df.head(2585),
        lat="lat",
        lon="lon",
        hover_name="properties.title",
        color_discrete_sequence=["#3a0ca3"],
        hover_data=["Source"],
        zoom=2,
        height=500,
    )
    df_one_building = pd.read_csv("./assets/data/one_building.csv", compression="gzip")

    fig2 = px.scatter_mapbox(
        df_one_building,
        lat="lat",
        lon="lon",
        hover_name=df_one_building[Variables.NAME.col_name],
        color_discrete_sequence=["#4895ef"],
        hover_data=[
            "period",
            "elevation (m)",
            "time zone (GMT)",
            "99% Heating DB",
            "1% Cooling DB ",
            "Source",
        ],
        zoom=2,
        height=500,
    )
    fig.add_trace(fig2.data[0])
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return dcc.Graph(
        id=ElementIds.TAB_ONE_MAP,
        figure=fig,
        config=generate_chart_name(TabNames.EPW_LOCATION_SELECT),
    )
