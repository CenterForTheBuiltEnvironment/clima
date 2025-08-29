import dash_bootstrap_components as dbc
import dash
from dash import dcc, html
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from pages.lib.global_column_names import ColNames
from config import DocLinks, UnitSystem
from pages.lib.global_element_ids import ElementIds


def alert():
    """Alert for survey."""
    return html.Div(
        id=ElementIds.ALERT_CONTAINER,
        children=[
            dbc.Toast(
                [
                    "If you have a moment, help us improve Clima and take a ",
                    html.A(
                        "quick user survey",
                        href="https://forms.gle/k289zP3R92jdu14M7",
                        className="alert-link",
                        target="_blank",
                    ),
                    "! ☀️",
                ],
                id=ElementIds.ID_LAYOUT_ALERT_AUTO,
                header="CBE Clima User Survey",
                icon="info",
                is_open=False,
                dismissable=True,
                className="survey-alert",
                style={"position": "fixed", "top": 25, "right": 10, "width": 400},
            ),
            dcc.Interval(id=ElementIds.ID_LAYOUT_INTERVAL_COMPONENT, interval=12 * 1000, n_intervals=0),
        ],
    )


def footer():
    """Build the footer at the bottom of the page."""
    return dbc.Row(
        align="center",
        justify="between",
        id=ElementIds.FOOTER_CONTAINER,
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
                                        "Version: 0.9.0",
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
        id=ElementIds.BANNER,
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
                                        id=ElementIds.BANNER_TITLE,
                                        style={"fontSize": "2rem"},
                                    ),
                                    dmc.Text(
                                        "Current Location:",
                                        id=ElementIds.ID_LAYOUT_BANNER_SUBTITLE,
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
                                id=ElementIds.ID_LAYOUT_GLOBAL_LOCAL_RADIO_INPUT,
                                value="local",
                                radius="md",
                                data=[
                                    {"label": "Global Value Ranges", "value": "global"},
                                    {"label": "Local Value Ranges", "value": "local"},
                                ],
                            ),
                            dmc.SegmentedControl(
                                id=ElementIds.ID_LAYOUT_SI_IP_RADIO_INPUT,
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
        id=ElementIds.STORE,
        children=[
            dcc.Store(id=ElementIds.ID_LAYOUT_DF_STORE, storage_type="session"),
            dcc.Store(id=ElementIds.ID_LAYOUT_META_STORE, storage_type="session"),
            dcc.Store(id=ElementIds.ID_LAYOUT_URL_STORE, storage_type="session"),
            dcc.Store(id=ElementIds.ID_LAYOUT_SI_IP_UNIT_STORE, storage_type="session"),
            dcc.Store(id=ElementIds.ID_LAYOUT_LINES_STORE, storage_type="session"),
        ],
    )


def build_tabs():
    return html.Div(
        id=ElementIds.TABS_CONTAINER,
        children=[
            html.Div(
                id=ElementIds.TABS_PARENT,
                className="custom-tabs",
                children=[
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                dbc.NavLink(
                                    page[ColNames.NAME],
                                    id=page[ColNames.PATH],
                                    href=page[ColNames.PATH],
                                    active="exact",
                                    className="nav-link",
                                    disabled=True,
                                ),
                                className="custom-tab",
                            )
                            for page in dash.page_registry.values()
                            if page[ColNames.NAME] not in ["404", "changelog"]
                        ],
                        id=ElementIds.TABS,
                        class_name="tab-container",
                        pills=True,
                        justified=True,
                    )
                ],
            ),
            html.Div(
                id=ElementIds.STORE_CONTAINER,
                children=[
                    store(),
                    html.Div(
                        id=ElementIds.TABS_CONTENT,
                        children=[
                            alert(),  # alert can be removed after survey is done
                            dash.page_container,
                        ],
                    ),
                ],
            ),
        ],
    )
