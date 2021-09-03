import base64
import io
import re
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from my_project.extract_df import create_df, get_data
from my_project.utils import plot_location_epw_files, generate_chart_name

messages_alert = {
    "start": "To start, upload an EPW file or click on a point on the map!",
    "not_available": "The EPW for this location is not available",
    "success": "The EPW was successfully loaded!",
    "invalid_format": "The format of the EPW file you have uploaded is invalid.",
    "wrong_extension": "The file you have uploaded is not an EPW file",
}


def layout_select():
    """Contents in the first tab 'Select Weather File'"""
    return html.Div(
        className="container-col tab-container",
        children=[
            dcc.Loading(
                id="loading-1",
                type="circle",
                fullscreen=True,
                children=alert(),
            ),
            dcc.Upload(
                id="upload-data",
                children=dbc.Button(
                    [
                        "Drag and Drop or ",
                        html.A("Select an EPW file from your computer"),
                    ],
                    id="upload-data-button",
                    outline=True,
                    color="secondary",
                    className="mt-2",
                    block=True,
                    style={"borderRadius": "5px", "borderStyle": "dashed"},
                ),
                # Allow multiple files to be uploaded
                multiple=True,
            ),
            dcc.Graph(
                id="tab-one-map",
                figure=plot_location_epw_files(),
                config=generate_chart_name("epw_location_select"),
            ),
            dbc.Modal(
                [
                    # dbc.ModalHeader("Header"),
                    dbc.ModalHeader(id="modal-header"),
                    dbc.ModalFooter(
                        children=[
                            dbc.Button(
                                "Close",
                                id="modal-close-button",
                                className="ml-2",
                                color="light",
                            ),
                            dbc.Button(
                                "Yes",
                                id="modal-yes-button",
                                className="ml-2",
                                color="primary",
                            ),
                        ]
                    ),
                ],
                id="modal",
                is_open=False,
            ),
        ],
    )


def alert():
    """Alert layout for the submit button."""
    return html.Div(
        [
            dbc.Alert(
                messages_alert["start"],
                color="primary",
                id="alert",
                dismissable=False,
                is_open=True,
                style={"maxHeight": "66px"},
            )
        ]
    )


@app.callback(
    [
        Output("df-store", "data"),
        Output("meta-store", "data"),
        Output("alert", "is_open"),
        Output("alert", "children"),
        Output("alert", "color"),
    ],
    [
        Input("modal-yes-button", "n_clicks"),
        Input("upload-data-button", "n_clicks"),
        Input("upload-data", "contents"),
    ],
    [
        State("upload-data", "filename"),
        State("url-store", "data"),
    ],
    prevent_initial_call=True,
)
# @code_timer
def submitted_data(
    use_epw_click, upload_click, list_of_contents, list_of_names, url_store
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
        df, location_info = create_df(lines, url_store)
        # fixme: DeprecationWarning: an integer is required (got type float).
        df = df.to_json(date_format="iso", orient="split")
        return (
            df,
            location_info,
            True,
            messages_alert["success"],
            "success",
        )

    elif (
        ctx.triggered[0]["prop_id"] == "upload-data.contents"
        and list_of_contents is not None
    ):
        content_type, content_string = list_of_contents[0].split(",")

        decoded = base64.b64decode(content_string)
        try:
            if "epw" in list_of_names[0]:
                # Assume that the user uploaded a CSV file
                lines = io.StringIO(decoded.decode("utf-8")).read().split("\n")
                df, location_info = create_df(lines, list_of_names[0])
                df = df.to_json(date_format="iso", orient="split")
                return (
                    df,
                    location_info,
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
        except Exception as e:
            print(e)
            return (
                None,
                None,
                True,
                messages_alert["wrong_extension"],
                "warning",
            )
    raise PreventUpdate


@app.callback(
    [
        Output("tab-summary", "disabled"),
        Output("tab-t-rh", "disabled"),
        Output("tab-sun", "disabled"),
        Output("tab-wind", "disabled"),
        Output("tab-psy-chart", "disabled"),
        Output("tab-data-explorer", "disabled"),
        Output("tab-outdoor-comfort", "disabled"),
        Output("tab-natural-ventilation", "disabled"),
        Output("banner-subtitle", "children"),
    ],
    [Input("df-store", "data")],
    State("meta-store", "data"),
)
def enable_tabs_when_data_is_loaded(data, meta):
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
            "Current Location: " + meta["city"] + ", " + meta["country"],
        )


@app.callback(
    [
        Output("modal", "is_open"),
        Output("url-store", "data"),
    ],
    [
        Input("modal-yes-button", "n_clicks"),
        Input("tab-one-map", "clickData"),
        Input("modal-close-button", "n_clicks"),
    ],
    [State("modal", "is_open")],
    prevent_initial_call=True,
)
def display_modal_when_data_clicked(clicks_use_epw, click_map, close_clicks, is_open):
    """display the modal to the user and check if he wants to use that file"""
    if click_map:
        url = re.search(
            r'href=[\'"]?([^\'" >]+)', click_map["points"][0]["customdata"][0]
        ).group(1)
        return not is_open, url
    return is_open, ""


@app.callback(
    [
        Output("modal-header", "children"),
    ],
    [
        Input("tab-one-map", "clickData"),
    ],
    prevent_initial_call=True,
)
def display_modal_when_data_clicked(click_map):
    """change the text of the modal header"""
    if click_map:
        return [f"Analyse data from {click_map['points'][0]['hovertext']}?"]
    return ["Analyse data from this location?"]
