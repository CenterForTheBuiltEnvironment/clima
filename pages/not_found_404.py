import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash_extensions import Lottie

from pages.lib.page_urls import PageUrls


dash.register_page(__name__, name="404")


layout = [
    dmc.Title("I could not find the page you are currently looking for", order=4),
    dmc.Text(
        "Please navigate the the home page by using the button below", className="mb-2"
    ),
    dmc.Anchor(
        dmc.Button(
            "Home page",
            fullWidth=True,
            leftIcon=DashIconify(icon="material-symbols:home-outline-rounded"),
        ),
        href="/",
    ),
    Lottie(
        options=dict(
            loop=True,
            autoplay=True,
            rendererSettings=dict(preserveAspectRatio="xMidYMid slice"),
        ),
        width="100%",
        url=PageUrls.NOT_FOUND.value,
    ),
]
