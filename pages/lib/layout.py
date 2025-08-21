import dash_bootstrap_components as dbc
import dash
from dash import dcc, html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from config import DocLinks, UnitSystem


def alert():
    """Alert for survey."""
    return html.Div(
        id="alert-container",
        children=[
            dbc.Toast(
                [
                    "If you have a moment, help us improving Clima and take a ",
                    html.A(
                        "quick user survey",
                        href="https://forms.gle/k289zP3R92jdu14M7",
                        className="alert-link",
                        target="_blank",
                    ),
                    "! ☀️",
                ],
                id="alert-auto",
                header="CBE Clima User Survey",
                icon="info",
                is_open=False,
                dismissable=True,
                className="survey-alert",
                style={"position": "fixed", "top": 25, "right": 10, "width": 400},
            ),
            dcc.Interval(id="interval-component", interval=12 * 1000, n_intervals=0),
        ],
    )


def footer():
    """Build the footer at the bottom of the page."""
    return dbc.Row(
        align="center",
        justify="between",
        id="footer-container",
        children=[
            dbc.Col(
                children=[
                    dbc.Row(
                        html.A(
                            children=[
                                html.Img(
                                    src="assets/img/cbe-logo.png",
                                )
                            ],
                            href="https://cbe.berkeley.edu/",
                        )
                    ),
                ],
                width=12,
                md=4,
                style={"padding": "15px"},
            ),
            dbc.Col(
                children=[
                    dbc.Row(
                        [
                            dcc.Markdown(
                                """
                                Please cite us:
                                Betti, G., Tartarini, F., Nguyen, C, Schiavon, S. CBE Clima Tool: 
                                A free and open-source web application for climate analysis tailored to sustainable building design. 
                                Build. Simul. (2023). [https://doi.org/10.1007/s12273-023-1090-5](https://doi.org/10.1007/s12273-023-1090-5).
                                """
                            ),
                            dmc.Group(
                                [
                                    dmc.Anchor(
                                        "Version: 0.8.19",
                                        href="https://center-for-the-built-environment.gitbook.io/clima/version/changelog",
                                        underline=True,
                                        c="white",
                                        target="_blank",
                                    ),
                                    dmc.Anchor(
                                        "Contributors",
                                        href="https://cbe-berkeley.gitbook.io/clima/#contributions",
                                        underline=True,
                                        c="white",
                                        target="_blank",
                                    ),
                                    dmc.Anchor(
                                        "Report issues on GitHub",
                                        href="https://github.com/CenterForTheBuiltEnvironment/clima/issues",
                                        underline=True,
                                        c="white",
                                        target="_blank",
                                    ),
                                    dmc.Anchor(
                                        "Contact us",
                                        href="https://github.com/CenterForTheBuiltEnvironment/clima/discussions",
                                        underline=True,
                                        c="white",
                                        target="_blank",
                                    ),
                                    dmc.Anchor(
                                        "Documentation",
                                        href="https://center-for-the-built-environment.gitbook.io/clima/",
                                        underline=True,
                                        c="white",
                                        target="_blank",
                                    ),
                                    dmc.Anchor(
                                        "License",
                                        href="https://center-for-the-built-environment.gitbook.io/clima/#license",
                                        underline=True,
                                        c="white",
                                        target="_blank",
                                    ),
                                ],
                                spacing="sm",
                                style={"marginTop": "1rem"},
                            ),
                        ],
                        style={"marginTop": "1rem"},
                    ),
                ],
                width=12,
                md=8,
            ),
        ],
    )


def banner():
    """Build the banner at the top of the page."""
    return html.Div(
        id="banner",
        children=[
            dmc.Group(
                position="apart",
                align="center",
                children=[
                    dmc.Group(
                        align="center",
                        children=[
                            html.A(
                                href="/",
                                children=[
                                    dmc.Image(
                                        src="assets/img/cbe-logo-small.png",
                                        height=40,
                                        width="auto",
                                    )
                                ],
                            ),
                            dmc.Stack(
                                spacing=0,
                                children=[
                                    dmc.Title(
                                        "CBE Clima Tool",
                                        order=1,
                                        id="banner-title",
                                        style={"fontSize": "2rem"},
                                    ),
                                    dmc.Text(
                                        "Current Location:",
                                        id="banner-subtitle",
                                        size="sm",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dmc.Group(
                        align="center",
                        children=[
                            html.A(
                                dmc.Button(
                                    "Documentation",
                                    leftIcon=DashIconify(icon="bi:book-half", width=20),
                                    variant="filled",
                                    color="#5c7cfa",
                                ),
                                href=DocLinks.MAIN.value,
                                target="_blank",
                                style={"textDecoration": "none"},
                            ),
                            dmc.SegmentedControl(
                                id="global-local-radio-input",
                                value="local",
                                radius="md",
                                data=[
                                    {"label": "Global Value Ranges", "value": "global"},
                                    {"label": "Local Value Ranges", "value": "local"},
                                ],
                            ),
                            dmc.SegmentedControl(
                                id="si-ip-radio-input",
                                value=UnitSystem.SI,
                                radius="md",
                                data=[
                                    {
                                        "label": UnitSystem.SI.upper(),
                                        "value": UnitSystem.SI,
                                    },
                                    {
                                        "label": UnitSystem.IP.upper(),
                                        "value": UnitSystem.IP,
                                    },
                                ],
                            ),
                        ],
                    ),
                ],
            )
        ],
    )


def store():
    return html.Div(
        id="store",
        children=[
            dcc.Store(id="df-store", storage_type="session"),
            dcc.Store(id="meta-store", storage_type="session"),
            dcc.Store(id="url-store", storage_type="session"),
            dcc.Store(id="si-ip-unit-store", storage_type="session"),
            dcc.Store(id="lines-store", storage_type="session"),
        ],
    )


def build_tabs():
    return html.Div(
        id="tabs-container",
        children=[
            html.Div(
                id="tabs-parent",
                className="custom-tabs",
                children=[
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                dbc.NavLink(
                                    page["name"],
                                    id=page["path"],
                                    href=page["path"],
                                    active="exact",
                                    className="nav-link",
                                    disabled=True,
                                ),
                                className="custom-tab",
                            )
                            for page in dash.page_registry.values()
                            if page["name"] not in ["404", "changelog"]
                        ],
                        id="tabs",
                        class_name="tab-container",
                        pills=True,
                        justified=True,
                    )
                ],
            ),
            html.Div(
                id="store-container",
                children=[
                    store(),
                    html.Div(
                        id="tabs-content",
                        children=[
                            alert(),  # alert can be removed after survey is done
                            dash.page_container,
                        ],
                    ),
                ],
            ),
        ],
    )
