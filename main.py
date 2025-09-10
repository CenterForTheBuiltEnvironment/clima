import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_extensions.enrich import Output, Input, callback
import dash_mantine_components as dmc

from app import app
from pages.lib.layout import banner, footer, build_tabs, burger_button, sidebar
from config import AppConfig
from pages.lib.global_element_ids import ElementIds

server = app.server

app.title = AppConfig.TITLE
app.layout = dmc.MantineProvider(
    theme={
        "colorScheme": "light",
        "primaryColor": "blue"
    },
    children=[
        dcc.Location(id=ElementIds.MAIN_URL, refresh=False),
        sidebar(),
        banner(),
        dmc.Box(id=ElementIds.PAGE_CONTENT, children=build_tabs()),
        footer(),
    ],
)


# callback for survey alert (dbc.Toast)
@callback(
    Output(ElementIds.ID_MAIN_ALERT_AUTO, "is_open"),
    Input(ElementIds.ID_MAIN_INTERVAL_COMPONENT, "n_intervals"),
)
def display_alert(n):
    return n == 1


if __name__ == "__main__":
    app.run(
        debug=AppConfig.DEBUG,
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        processes=AppConfig.PROCESSES,
        threaded=AppConfig.THREADED,
    )
