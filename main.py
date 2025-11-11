from dash import dcc
import dash_mantine_components as dmc

from app import app
from pages.lib.layout import create_collapsible_layout
from config import AppConfig
from pages.lib.global_element_ids import ElementIds

server = app.server

app.title = AppConfig.TITLE
app.layout = dmc.MantineProvider(
    children=[
        dcc.Location(id=ElementIds.MAIN_URL, refresh=False),
        create_collapsible_layout(),
    ],
)

if __name__ == "__main__":
    app.run(
        debug=AppConfig.DEBUG,
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        processes=AppConfig.PROCESSES,
        threaded=AppConfig.THREADED,
    )
