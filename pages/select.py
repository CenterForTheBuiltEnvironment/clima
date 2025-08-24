import base64
import json
import re

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Serverside, Output, Input, State, html, dcc, callback
from pandas import json_normalize

from pages.lib.extract_df import convert_data
from pages.lib.extract_df import create_df, get_data, get_location_info
from pages.lib.global_elementids import ElementIds
from pages.lib.global_scheme import mapping_dictionary
from config import PageUrls, PageInfo, UnitSystem
from pages.lib.utils import generate_chart_name

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
    return html.Div(
        className="container-col tab-container",
        children=[
            dcc.Loading(
                id=ElementIds.LOADING_ONE,
                type="circle",
                fullscreen=True,
                children=alert(),
            ),
            dcc.Upload(
                id=ElementIds.UPLOAD_DATA,
                children=dbc.Button(
                    [
                        "Drag and Drop or ",
                        html.A("Select an EPW file from your computer"),
                    ],
                    id=ElementIds.UPLOAD_DATA_BUTTON,
                    outline=True,
                    color="secondary",
                    className="mt-2",
                    style={"borderRadius": "5px", "borderStyle": "dashed"},
                ),
                # Allow multiple files to be uploaded
                multiple=True,
                className="d-grid",
            ),
            dmc.Skeleton(
                visible=False,
                id=ElementIds.SKELETON_GRAPH_CONTAINER,
                height=500,
                children=html.Div(id=ElementIds.TAB_ONE_MAP),
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(id=ElementIds.MODAL_HEADER),
                    dbc.ModalFooter(
                        children=[
                            dbc.Button(
                                "Close",
                                id=ElementIds.MODAL_CLOSE_BUTTON,
                                className="ml-2",
                                color="light",
                            ),
                            dbc.Button(
                                "Yes",
                                id=ElementIds.MODAL_YES_BUTTON,
                                className="ml-2",
                                color="primary",
                            ),
                        ]
                    ),
                ],
                id=ElementIds.MODAL,
                is_open=False,
            ),
        ],
    )


def alert():
    """Alert layout for the submit button."""
    return dbc.Alert(
        messages_alert["start"],
        color="primary",
        id=ElementIds.ALERT,
        dismissable=False,
        is_open=True,
        style={"maxHeight": "66px"},
    )


# add si-ip and map dictionary in the output
@callback(
    [
        Output(ElementIds.ID_SELECT_META_STORE, "data"),
        Output(ElementIds.LINES_STORE, "data"),
        Output(ElementIds.ALERT, "is_open"),
        Output(ElementIds.ALERT, "children"),
        Output(ElementIds.ALERT, "color"),
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

    if ctx.triggered[0]["prop_id"] == "modal-yes-button.n_clicks":
        lines = get_data(url_store)
        if lines is None:
            return (
                None,
                None,
                True,
                messages_alert["not_available"],
                "warning",
            )
        location_info = get_location_info(
            lines, url_store
        )  # we might need to split this call into two, one returns df and one returns location_info
        return (
            location_info,
            lines,
            True,
            messages_alert["success"],
            "success",
        )

    elif (
        ctx.triggered[0]["prop_id"] == "upload-data.contents"
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
                    "success",
                )
            else:
                return (
                    None,
                    None,
                    True,
                    messages_alert["invalid_format"],
                    "warning",
                )
        except Exception:
            # print(e)
            return (
                None,
                None,
                True,
                messages_alert["wrong_extension"],
                "warning",
            )
    raise PreventUpdate


# add switch_si_ip function and convert the data-store
@callback(
    [
        Output(ElementIds.ID_SELECT_DF_STORE, "data"),
        Output(ElementIds.ID_SELECT_SI_IP_UNIT_STORE, "data"),
    ],
    [
        Input(ElementIds.LINES_STORE, "modified_timestamp"),
        Input(ElementIds.ID_SELECT_SI_IP_RADIO_INPUT, "value"),
    ],
    [State(ElementIds.ID_SELECT_URL_STORE, "data"), State("lines-store", "data")],
)
def switch_si_ip(_, si_ip_input, url_store, lines):
    if lines is not None:
        df, _ = create_df(lines, url_store)
        map_json = json.dumps(mapping_dictionary)
        if si_ip_input == UnitSystem.IP:
            map_json = convert_data(df, map_json)
        return Serverside(df), si_ip_input
    else:
        return (
            None,
            None,
        )


@callback(
    [
        Output("/", "disabled"),
        Output("/summary", "disabled"),
        Output("/t-rh", "disabled"),
        Output("/sun", "disabled"),
        Output("/wind", "disabled"),
        Output("/psy-chart", "disabled"),
        Output("/explorer", "disabled"),
        Output("/outdoor", "disabled"),
        Output("/natural-ventilation", "disabled"),
        Output(ElementIds.BANNER_SUBTITLE, "children"),
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
            "Current Location: " + meta["city"] + ", " + meta["country"],
        )


@callback(
    [
        Output(ElementIds.MODAL, "is_open"),
        Output(ElementIds.ID_SELECT_URL_STORE, "data"),
    ],
    [
        Input(ElementIds.MODAL_YES_BUTTON, "n_clicks"),
        Input(ElementIds.TAB_ONE_MAP, "clickData"),
        Input(ElementIds.MODAL_CLOSE_BUTTON, "n_clicks"),
    ],
    [State(ElementIds.MODAL, "is_open")],
    prevent_initial_call=True,
)
def display_modal_when_data_clicked(_, click_map, __, is_open):
    """display the modal to the user and check if he wants to use that file"""
    if click_map:
        url = re.search(
            r'href=[\'"]?([^\'" >]+)', click_map["points"][0]["customdata"][-1]
        ).group(1)
        return not is_open, url
    return is_open, ""


@callback(
    [
        Output(ElementIds.MODAL_HEADER, "children"),
    ],
    [
        Input(ElementIds.TAB_ONE_MAP, "clickData"),
    ],
    prevent_initial_call=True,
)
def change_text_modal(click_map):
    """change the text of the modal header"""
    if click_map:
        return [f"Analyse data from {click_map['points'][0]['hovertext']}?"]
    return ["Analyse data from this location?"]


@callback(
    Output(ElementIds.SKELETON_GRAPH_CONTAINER, "children"),
    Input("url", "pathname"),
)
def plot_location_epw_files(pathname):
    # print(pathname)
    if pathname != "/":
        raise PreventUpdate

    with open("./assets/data/epw_location.json", encoding="utf8") as data_file:
        data = json.load(data_file)

    df = json_normalize(data["features"])
    df[["lon", "lat"]] = pd.DataFrame(df["geometry.coordinates"].tolist())
    df["lat"] += 0.005
    df["lat"] += 0.005
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
        hover_name=df_one_building["name"],
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

    return (
        dcc.Graph(
            id=ElementIds.TAB_ONE_MAP,
            figure=fig,
            config=generate_chart_name("epw_location_select"),
        ),
    )
