import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, Input, Output, State, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from pages.lib.global_column_names import ColNames
from config import DocLinks, UnitSystem
from pages.lib.global_element_ids import ElementIds


def burger_button():
    """create burger button"""
    return dmc.ActionIcon(
        DashIconify(icon="radix-icons:hamburger-menu", width=20),
        id=ElementIds.BURGER_BUTTON,
        size="lg",
        variant="filled",
        color="blue",
    )


def alert():
    """Survey toast + periodic timer."""
    return dmc.Stack(
        gap=0,
        children=[
            dbc.Toast(
                [
                    "If you have a moment, help us improve Clima and take a ",
                    dmc.Anchor(
                        "quick user survey",
                        href="https://forms.gle/k289zP3R92jdu14M7",
                        target="_blank",
                        className="alert-link",
                    ),
                    "! ☀️",
                ],
                id=ElementIds.ID_LAYOUT_ALERT_AUTO,
                header="CBE Clima User Survey",
                icon="info",
                is_open=False,
                dismissable=True,
                className="survey-alert",
            ),
            dmc.Box(
                children=dcc.Interval(
                    id=ElementIds.ID_LAYOUT_INTERVAL_COMPONENT,
                    interval=12 * 1000,
                    n_intervals=0,
                )
            ),
        ],
    )


def footer():
    """Build the footer at the bottom of the page."""
    return dmc.Box(
        id=ElementIds.FOOTER_CONTAINER,
        children=[
            dmc.Box(
                children=[
                    dmc.Anchor(
                        href="https://cbe.berkeley.edu/",
                        children=dmc.Image(
                            src="assets/img/cbe-logo.png",
                            alt="CBE Logo",
                            h=65,
                            w="auto",
                            fit="contain"
                        )
                    ),
                ],
                className="footer-logo-section"
            ),
            dmc.Box(
                children=[
                    dmc.Stack(
                        gap="xs",
                        children=[
                            dcc.Markdown(
                                """
                                Please cite us:
                                Betti, G., Tartarini, F., Nguyen, C, Schiavon, S. CBE Clima Tool:
                                A free and open-source web application for climate analysis tailored to sustainable building design.
                                Build. Simul. (2023). [https://doi.org/10.1007/s12273-023-1090-5](https://doi.org/10.1007/s12273-023-1090-5).
                                """,
                                className="footer-markdown-text"
                            ),
                            dmc.Group(
                                [
                                    dmc.Anchor(
                                        "Version: 0.9.0",
                                        href="https://center-for-the-built-environment.gitbook.io/clima/version/changelog",
                                        underline=True,
                                        c="white",
                                        target="_blank",
                                        className="footer-link"
                                    ),
                                    dmc.Anchor(
                                        "Contributors",
                                        href="https://cbe-berkeley.gitbook.io/clima/#contributions",
                                        underline=True,
                                        c="white",
                                        target="_blank",
                                        className="footer-link"
                                    ),
                                    dmc.Anchor(
                                        "Report issues on GitHub",
                                        href="https://github.com/CenterForTheBuiltEnvironment/clima/issues",
                                        underline=True,
                                        c="white",
                                        target="_blank",
                                        className="footer-link"
                                    ),
                                    dmc.Anchor(
                                        "Contact us",
                                        href="https://github.com/CenterForTheBuiltEnvironment/clima/discussions",
                                        underline=True,
                                        c="white",
                                        target="_blank",
                                        className="footer-link"
                                    ),
                                    dmc.Anchor(
                                        "Documentation",
                                        href="https://center-for-the-built-environment.gitbook.io/clima/",
                                        underline=True,
                                        c="white",
                                        target="_blank",
                                        className="footer-link"
                                    ),
                                    dmc.Anchor(
                                        "License",
                                        href="https://center-for-the-built-environment.gitbook.io/clima/#license",
                                        underline=True,
                                        c="white",
                                        target="_blank",
                                        className="footer-link"
                                    ),
                                ],
                                gap="sm",
                                className="footer-links-group"
                            ),
                        ],
                        className="footer-text-content"
                    ),
                ],
                className="footer-content-section"
            ),
        ],
    )


def banner():
    """Top banner rewritten with dash-mantine-components only."""
    return dmc.Box(
        id=ElementIds.BANNER,
        children=[
            dmc.Group(
                justify="space-between",
                align="center",
                wrap="nowrap",
                children=[
                    dmc.Group(
                        align="center",
                        gap="md",
                        children=[
                            burger_button(),
                            dmc.Image(src="assets/img/cbe-logo-small.png", h=40, w="auto"),
                            dmc.Stack(
                                gap=2,
                                children=[
                                    dmc.Title(
                                        "CBE Clima Tool",
                                        id=ElementIds.BANNER_TITLE,
                                        order=2,
                                    ),
                                    dmc.Text(
                                        "Current Location: N/A",
                                        id=ElementIds.ID_LAYOUT_BANNER_SUBTITLE,
                                        size="sm",
                                        opacity=0.85,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            )
        ],
    )


def sidebar():
    """ create side bar """
    return dmc.Drawer(
        id=ElementIds.SIDE_BAR,
        title=dmc.Group([
            dmc.Image(src="assets/img/cbe-logo-small.png", h=30, w="auto"),
            dmc.Text("CBE Clima Tool", fw=600)
        ]),
        padding="md",
        size="300px",
        zIndex=999,
        opened=False,
        className="custom-sidebar",
        styles={
            "title": {"paddingRight": 30},
        },
        children=[
            dmc.Stack(
                gap="sm",
                children=build_sidebar_nav_items()
            )
        ],
    )


# Pages Icon
PAGE_ICON_MAP = {
    "Select Weather File": "tabler:upload",
    "Climate Summary": "tabler:chart-bar",
    "Temperature and Humidity": "tabler:temperature",
    "Sun and Clouds": "tabler:sun",
    "Wind": "tabler:wind",
    "Psychrometric Chart": "tabler:chart-dots",
    "Natural Ventilation": "tabler:windmill",
    "Outdoor Comfort": "tabler:thermometer",
    "Data Explorer": "tabler:database",
    "Changelog": "tabler:history"
}

def build_sidebar_nav_items():
    # === Secondary Menu ===
    sub_links = []
    for page in dash.page_registry.values():
        if page[ColNames.NAME] in ["404"]:
            continue
        icon = PAGE_ICON_MAP.get(page[ColNames.NAME], "tabler:circle")
        sub_links.append(
            dmc.NavLink(
                label=page[ColNames.NAME],
                leftSection=DashIconify(icon=icon, width=20),
                href=page[ColNames.PATH],
                id=f"nav-{page[ColNames.PATH].replace('/', '')}",
                active=False,
                style={"marginBottom": "4px"},
            )
        )

    # Primary Menu
    parent_group = dmc.NavLink(
        label="Pages Menu",
        leftSection=DashIconify(icon="tabler:list-details", width=20),
        children=sub_links,
        id=ElementIds.NAV_GROUP_MAIN,
        variant="light",
        childrenOffset=18,
    )

    controls_stack = dmc.Stack(
        gap="sm",
        px=0,
        py="xs",
        children=[
            dmc.SegmentedControl(
                id=ElementIds.ID_LAYOUT_GLOBAL_LOCAL_RADIO_INPUT,
                value="local",
                data=[
                    {"label": "Global Value Ranges", "value": "global"},
                    {"label": "Local Value Ranges",  "value": "local"},
                ],
                radius="md",
                size="sm",
            ),
            dmc.SegmentedControl(
                id=ElementIds.ID_LAYOUT_SI_IP_RADIO_INPUT,
                value=UnitSystem.SI,
                data=[
                    {"label": UnitSystem.SI.upper(), "value": UnitSystem.SI},
                    {"label": UnitSystem.IP.upper(), "value": UnitSystem.IP},
                ],
                radius="md",
                size="sm",
            ),
        ],
    )

    # Primary Menu
    controls_group = dmc.NavLink(
        label="Tools Menu",
        leftSection=DashIconify(icon="tabler:settings", width=20),
        children=[controls_stack],
        id=ElementIds.NAV_GROUP_CONTROLS,
        variant="light",
        childrenOffset=18,
    )

    # Primary Menu - Documentation
    doc_link = dmc.NavLink(
        label="Documentation",
        leftSection=DashIconify(icon="tabler:file-text", width=20),
        href=DocLinks.MAIN.value,
        target="_blank",
        id=ElementIds.NAV_DOC_LINK,
        variant="light",
    )
    return [parent_group, controls_group, doc_link]


def store():
    return dmc.Box(
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
    return dmc.Box(
        id=ElementIds.TABS_CONTAINER,
        children=[
            dmc.Box(
                id=ElementIds.STORE_CONTAINER,
                children=[
                    store(),
                    dmc.Box(
                        id=ElementIds.TABS_CONTENT,
                        children=[
                            alert(),
                            dash.page_container,
                        ],
                    ),
                ],
            ),
        ],
    )

@callback(
    Output(ElementIds.SIDE_BAR, "opened"),
    Input(ElementIds.BURGER_BUTTON, "n_clicks"),
    State(ElementIds.SIDE_BAR, "opened"),
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks, opened):
    if n_clicks:
        return not opened
    return opened


@callback(
    Output(ElementIds.SIDE_BAR, "opened", allow_duplicate=True),
    Input(ElementIds.LAYOUT_URL, "pathname"),
    prevent_initial_call='initial_duplicate',
)
def close_sidebar_on_navigation(pathname):
    return False


# Callback to set active state for navigation links based on current URL
@callback(
    [Output(f"nav-{page[ColNames.PATH].replace('/', '')}", "active") 
     for page in dash.page_registry.values() 
     if page[ColNames.NAME] not in ["404"]],
    Input(ElementIds.LAYOUT_URL, "pathname"),
    prevent_initial_call=True,
)
def update_nav_active_state(pathname):
    """Update active state of navigation links based on current URL pathname"""
    active_states = []
    
    for page in dash.page_registry.values():
        if page[ColNames.NAME] in ["404"]:
            continue
            
        # Check if current pathname matches this page's path
        is_active = pathname == page[ColNames.PATH]
        active_states.append(is_active)
    
    return active_states
