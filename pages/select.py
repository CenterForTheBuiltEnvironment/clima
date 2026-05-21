import base64
import os

import dash
import dash_leaflet as dl
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Serverside, Output, Input, State, html, dcc, callback
from dash_extensions.javascript import assign

from pages.lib.extract_df import convert_df_units
from pages.lib.extract_df import create_df, get_data, get_location_info
from pages.lib.global_variables import Variables
from pages.lib.global_element_ids import ElementIds
from config import PageUrls, PageInfo
from pages.lib.utils import get_default_global_filter_store_data

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

_GEO_URL = "/geojson/locations?v=" + str(int(os.path.getmtime("assets/data/locations.geojson.gz")))

# Create marker and bind tooltip in one function — pointToLayer is only ever called
# for individual point features, never for cluster markers, so properties are always complete.
_point_to_layer = assign("""function(feature, latlng, ctx) {
    const p = feature.properties;
    const color = p.source === "ep" ? "#3a0ca3" : "#4895ef";
    const marker = L.circleMarker(latlng, {
        radius: 5, color: color, fillColor: color, fillOpacity: 0.8, weight: 1
    });

    let html = '<b>' + (p.title || '') + '</b><br/>'
             + 'Lat: ' + latlng.lat.toFixed(2) + ', Lon: ' + latlng.lng.toFixed(2) + '<br/>';
    if (p.source === 'ob') {
        html += 'Period: '         + (p.period || 'N/A') + '<br/>'
              + 'Elevation: '      + (p.elev   || 'N/A') + ' m<br/>'
              + 'Time zone: GMT'   + (p.tz     || 'N/A') + '<br/>'
              + '99% Heating DB: ' + (p.heat99 || 'N/A') + '<br/>'
              + '1% Cooling DB: '  + (p.cool1  || 'N/A') + '<br/>'
              + 'Source: Climate.OneBuilding.Org';
    } else {
        html += 'Source: EnergyPlus';
    }
    marker.bindTooltip(html, {sticky: true, opacity: 0.9});
    return marker;
}""")


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
                multiple=True,
                style={"display": "grid"},
            ),
            dl.Map(
                id="map-container",
                center=[20, 0],
                zoom=2,
                style={"height": "500px", "width": "100%"},
                children=[
                    dl.TileLayer(
                        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
                        attribution=(
                            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                            ' contributors &copy; <a href="https://carto.com/">CARTO</a>'
                        ),
                    ),
                    dl.GeoJSON(
                        id=ElementIds.TAB_ONE_MAP,
                        url=_GEO_URL,
                        cluster=True,
                        zoomToBoundsOnClick=True,
                        pointToLayer=_point_to_layer,
                        superClusterOptions={"radius": 80, "maxZoom": 15},
                    ),
                ],
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
        Output(ElementIds.SHARED_META_STORE, "data"),
        Output(ElementIds.SHARED_LINES_STORE, "data"),
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
        State(ElementIds.SHARED_URL_STORE, "data"),
    ],
    prevent_initial_call=True,
)
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
        location_info = get_location_info(lines, url_store)
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
        Output(ElementIds.SHARED_DF_STORE, "data"),
        Output(ElementIds.SHARED_SI_IP_UNIT_STORE, "data"),
    ],
    [
        Input(ElementIds.SHARED_LINES_STORE, "modified_timestamp"),
        Input(ElementIds.SHARED_SI_IP_RADIO_INPUT, "value"),
    ],
    [
        State(ElementIds.SHARED_URL_STORE, "data"),
        State(ElementIds.SHARED_LINES_STORE, "data"),
    ],
)
def switch_si_ip(_, si_ip_input, url_store, lines):
    if lines is not None:
        df, _ = create_df(lines, url_store)
        df = convert_df_units(df, si_ip_input)
        return Serverside(df), si_ip_input
    else:
        return (None, None)


@callback(
    [
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
        Input(ElementIds.SHARED_META_STORE, "data"),
        Input(ElementIds.SHARED_DF_STORE, "data"),
    ],
)
def enable_tabs_when_data_is_loaded(meta, data):
    """Hide tabs when data are not loaded"""
    location_string = "Location: N/A"
    disable_links = True
    if data is not None:
        location_string = f"Location: {meta[Variables.CITY.col_name]}, {meta[Variables.COUNTRY.col_name]}"
        disable_links = False

    return (
        disable_links,
        disable_links,
        disable_links,
        disable_links,
        disable_links,
        disable_links,
        disable_links,
        disable_links,
        location_string,
    )


@callback(
    [
        Output(ElementIds.MODAL, "opened"),
        Output(ElementIds.SHARED_URL_STORE, "data"),
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
    """Display the modal when a map location is clicked."""
    if click_map:
        url = (click_map.get("properties") or {}).get("url")
        if url:
            return not opened, url
    return opened, ""


@callback(
    [Output(ElementIds.MODAL_HEADER, "children")],
    [Input(ElementIds.TAB_ONE_MAP, "clickData")],
    prevent_initial_call=True,
)
def change_text_modal(click_map):
    if click_map:
        title = (click_map.get("properties") or {}).get("title")
        if title:
            return [f"Analyse data from {title}?"]
    return ["Analyse data from this location?"]
