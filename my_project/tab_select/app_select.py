import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app, cache, TIMEOUT
from my_project.extract_df import create_df
from my_project.utils import code_timer

import pandas as pd


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
                    dbc.Button(
                        "Download EPW",
                        color="primary",
                        className="mr-1",
                        id="download-button",
                        disabled=True,
                    ),
                    dcc.Download(id="download-dataframe-csv"),
                ],
            ),
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
    [Input("submit-button", "n_clicks")],
    [State("input-url", "value")],
    prevent_initial_call=True,
)
@code_timer
@cache.memoize(timeout=TIMEOUT)
def submit_button(n_clicks, value):
    """Takes the input once submitted and stores it."""

    if n_clicks is None:
        raise PreventUpdate
    else:
        df, meta = create_df(value)
        if df is not None:
            # fixme: DeprecationWarning: an integer is required (got type float).
            df = df.to_json(date_format="iso", orient="split")
            # todo I should update the input value with the last entered
            return df, meta
        else:
            return None, None


@app.callback(
    Output("alert", "is_open"),
    Output("alert", "children"),
    Output("alert", "color"),
    Output("banner-subtitle", "children"),
    Output("download-button", "disabled"),
    [Input("df-store", "data")],
    [Input("submit-button", "n_clicks")],
    [State("meta-store", "data")],
)
def alert_display(data, n_clicks, meta):
    """Displays the alert for the submit button."""
    default = "Current Location: N/A"
    # todo store click count in memory
    if data is None and n_clicks is None:
        return True, "To start, submit a link below!", "primary", default, True
    elif data is None and n_clicks > 0:
        return (
            True,
            "This link is not available. Please choose another one.",
            "warning",
            default,
            False,
        )
    else:
        subtitle = "Current Location: " + meta[1] + ", " + meta[3]
        return (
            True,
            "Successfully loaded data. You can change location by submitting a link below!",
            "success",
            subtitle,
            False,
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
    print("in here")
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
    else:
        default_url = meta[-1]

    return default_url


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("download-button", "n_clicks"),
    [State("df-store", "data")],
    [State("meta-store", "data")],
    prevent_initial_call=True,
)
def func(n_clicks, df, meta):
    if n_clicks is None:
        raise PreventUpdate
    elif df is not None:
        df = pd.read_json(df, orient="split")

        file_name = "_".join(meta[1:4])
        return dcc.send_data_frame(df.to_csv, f"{file_name}_EPW.csv")
    else:
        print("df not loaded yet")
