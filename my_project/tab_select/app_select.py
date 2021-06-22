import base64
import datetime
import io
import dash_table
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app, cache, TIMEOUT
from my_project.extract_df import create_df, get_data
from my_project.utils import code_timer


def layout_select():
    """Contents in the first tab 'Select Weather File'"""
    return html.Div(
        className="container-col tab-container",
        children=[
            alert(),
            html.Div(
                id="tab-one-form-container",
                className="container-row",
                children=[
                    dcc.Input(
                        id="input-url",
                        value="",
                        type="text",
                    ),
                    dbc.Button(
                        "Submit", color="primary", className="mr-1", id="submit-button"
                    ),
                ],
            ),
            dcc.Upload(
                id="upload-data",
                children=dbc.Button(
                    [
                        "Drag and Drop or ",
                        html.A("Select Files"),
                        " your EPW file",
                    ],
                    outline=True,
                    color="secondary",
                    className="mt-2",
                    block=True,
                    style={"borderRadius": "5px", "borderStyle": "dashed"},
                ),
                # Allow multiple files to be uploaded
                multiple=True,
            ),
            html.Div(id="output-data-upload"),
            html.Embed(id="tab-one-map", src="https://www.ladybug.tools/epwmap/"),
            html.P(
                children=[
                    "This ",
                    html.A("EPW Map", href="https://www.ladybug.tools/epwmap/"),
                    " has been developed by and is used with kind permission of the amazing folks at ",
                    html.A("Ladybug Tools", href="https://www.ladybug.tools/"),
                ]
            ),
        ],
    )


def alert():
    """Alert layout for the submit button."""
    return html.Div(
        [
            dbc.Alert(
                "Submit a link below or upload an EPW file!",
                color="primary",
                id="alert",
                dismissable=True,
                is_open=True,
                style={"maxHeight": "66px"},
            )
        ]
    )


# TAB: Select EPW
@app.callback(
    Output("df-store", "data"),
    Output("meta-store", "data"),
    Output("alert", "is_open"),
    Output("alert", "children"),
    Output("alert", "color"),
    Output("banner-subtitle", "children"),
    Input("submit-button", "n_clicks"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("input-url", "value"),
    prevent_initial_call=True,
)
@code_timer
# @cache.memoize(timeout=TIMEOUT)
def submit_button(n_clicks, list_of_contents, list_of_names, url):
    """Takes the input once submitted and stores it."""
    default = "Current Location: N/A"

    ctx = dash.callback_context
    print(ctx.triggered[0]["prop_id"])

    if ctx.triggered[0]["prop_id"] == "submit-button.n_clicks":
        if n_clicks is None:
            raise PreventUpdate
        else:
            lines = get_data(url)
            if lines is None:
                return (
                    None,
                    None,
                    True,
                    "This link you have selected is not available. Please choose another one.",
                    "warning",
                    default,
                )
            df, meta = create_df(lines, url)
            # fixme: DeprecationWarning: an integer is required (got type float).
            df = df.to_json(date_format="iso", orient="split")
            # todo I should update the input value with the last entered
            return (
                df,
                meta,
                True,
                "Successfully loaded data. You can change location by submitting a link below or by uploading your EPW file!",
                "success",
                "Current Location: " + meta[1] + ", " + meta[3],
            )

    else:
        if list_of_contents is not None:
            content_type, content_string = list_of_contents[0].split(",")

            decoded = base64.b64decode(content_string)
            try:
                if "epw" in list_of_names[0]:
                    # Assume that the user uploaded a CSV file
                    lines = io.StringIO(decoded.decode("utf-8")).read().split("\n")
                    df, meta = create_df(lines, list_of_names[0])
                    df = df.to_json(date_format="iso", orient="split")
                    return (
                        df,
                        meta,
                        True,
                        "Successfully loaded your EPW file. You can change location by submitting a link below or by uploading your EPW file!",
                        "success",
                        "Current Location: " + meta[1] + ", " + meta[3],
                    )
                else:
                    return (
                        None,
                        None,
                        True,
                        "The format of the EPW file you have uploaded is invalid.",
                        "warning",
                        default,
                    )
            except Exception as e:
                print(e)
                return (
                    None,
                    None,
                    True,
                    "The file you have uploaded is not an EPW file",
                    "warning",
                    default,
                )


@app.callback(
    Output("tab-summary", "disabled"),
    Output("tab-t-rh", "disabled"),
    Output("tab-sun", "disabled"),
    Output("tab-wind", "disabled"),
    Output("tab-psy-chart", "disabled"),
    Output("tab-data-explorer", "disabled"),
    Output("tab-outdoor_comfort", "disabled"),
    Output("tab-natural-ventilation", "disabled"),
    [Input("df-store", "data")],
    [Input("submit-button", "n_clicks")],
)
def enable_disable_tabs(data, n_clicks):
    if data is None and n_clicks is None:
        return True, True, True, True, True, True, True, True
    else:
        return False, False, False, False, False, False, False, False


# update the value of the input URL
@app.callback(
    Output("input-url", "value"),
    Input("meta-store", "modified_timestamp"),
    State("meta-store", "data"),
)
def on_data(ts, meta):
    if ts is None:
        raise PreventUpdate

    if meta is None:
        default_url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw"
    elif "http" not in meta[-1]:
        default_url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw"
    else:
        default_url = meta[-1]

    return default_url
