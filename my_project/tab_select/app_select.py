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
            html.Div(
                children=[
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(
                            [
                                "Drag and Drop or ",
                                html.A("Select Files"),
                                " your EPW file",
                            ]
                        ),
                        style={
                            "width": "98%",
                            "height": "50px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "margin": "10px",
                        },
                        # Allow multiple files to be uploaded
                        multiple=True,
                    ),
                ],
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
                id="alert",
                dismissable=True,
                is_open=False,
            )
        ]
    )


# TAB: Select EPW
@app.callback(
    Output("df-store", "data"),
    Output("meta-store", "data"),
    Input("submit-button", "n_clicks"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
    State("input-url", "value"),
    prevent_initial_call=True,
)
@code_timer
# @cache.memoize(timeout=TIMEOUT)
def submit_button(n_clicks, list_of_contents, list_of_names, list_of_dates, url):
    """Takes the input once submitted and stores it."""

    ctx = dash.callback_context
    print(ctx.triggered[0]["prop_id"])

    if ctx.triggered[0]["prop_id"] == "submit-button.n_clicks":
        if n_clicks is None:
            raise PreventUpdate
        else:
            lines = get_data(url)
            if lines is None:
                return None, None
            df, meta = create_df(lines, url)
            if df is not None:
                # fixme: DeprecationWarning: an integer is required (got type float).
                df = df.to_json(date_format="iso", orient="split")
                # todo I should update the input value with the last entered
                return df, meta
            else:
                return None, None

    else:
        print(list_of_contents, list_of_names, list_of_dates)
        if list_of_contents is not None:
            content_type, content_string = list_of_contents[0].split(",")

            decoded = base64.b64decode(content_string)
            try:
                if "epw" in list_of_names[0]:
                    # Assume that the user uploaded a CSV file
                    lines = io.StringIO(decoded.decode("utf-8")).read().split("\n")
                    df, meta_data = create_df(lines, list_of_names[0])
                    df = df.to_json(date_format="iso", orient="split")
                    return df, meta_data
                else:
                    return None, None
            except Exception as e:
                print(e)
                return None, None


@app.callback(
    Output("alert", "is_open"),
    Output("alert", "children"),
    Output("alert", "color"),
    Output("banner-subtitle", "children"),
    [Input("df-store", "data")],
    [Input("submit-button", "n_clicks")],
    [State("meta-store", "data")],
)
def alert_display(data, n_clicks, meta):
    """Displays the alert for the submit button."""
    default = "Current Location: N/A"
    # todo store click count in memory
    if data is None and n_clicks is None:
        return True, "To start, submit a link below!", "primary", default
    elif data is None and n_clicks > 0:
        return (
            True,
            "This link is not available. Please choose another one.",
            "warning",
            default,
        )
    else:
        subtitle = "Current Location: " + meta[1] + ", " + meta[3]
        return (
            True,
            "Successfully loaded data. You can change location by submitting a link below or by uploading your EPW file!",
            "success",
            subtitle,
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


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "epw" in filename:
            # Assume that the user uploaded a CSV file
            lines = io.StringIO(decoded.decode("utf-8")).read().split("\n")
            df, meta_data = create_df(lines, filename)
            df = df.head()
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return html.Div(
        [
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),
            dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df.columns],
            ),
            html.Hr(),  # horizontal line
            # For debugging, display the raw contents provided by the web browser
            html.Div("Raw Content"),
            html.Pre(
                contents[0:200] + "...",
                style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"},
            ),
        ]
    )


@app.callback(
    Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children
