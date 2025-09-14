import dash
from dash import dcc, Input, Output, State, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from pages.lib.global_column_names import ColNames
from config import DocLinks, UnitSystem
from pages.lib.global_element_ids import ElementIds
from pages.lib.page_icon import PageIcon


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
            dmc.Alert(
                [
                    "If you have a moment, help us improve Clima and take a ",
                    dmc.Anchor(
                        "quick user survey",
                        href="https://forms.gle/k289zP3R92jdu14M7",
                        target="_blank",
                        c="white",
                        underline=True,
                    ),
                    "! ☀️",
                ],
                id=ElementIds.ID_LAYOUT_ALERT_AUTO,
                title="CBE Clima User Survey",
                icon="Info",
                color="blue",
                variant="filled",
                withCloseButton=True,
                pos="fixed",
                top="25px",
                right="10px",
                w="400px",
                style={"zIndex": 1002, "display": "none"},
            ),
            dcc.Interval(
                id=ElementIds.ID_LAYOUT_INTERVAL_COMPONENT,
                interval=12 * 1000,
                n_intervals=0,
            ),
        ],
    )


def footer():
    """Build the footer at the bottom of the page."""
    white_anchor_style = {
        "underline": True,
        "c": "white",
        "fz": "md",
        "fw": 500,
        "target": "_blank",
    }

    footer_links = [
        (
            "Version: 0.9.0",
            "https://center-for-the-built-environment.gitbook.io/clima/version/changelog",
        ),
        ("Contributors", "https://cbe-berkeley.gitbook.io/clima/#contributions"),
        (
            "Report issues on GitHub",
            "https://github.com/CenterForTheBuiltEnvironment/clima/issues",
        ),
        (
            "Contact us",
            "https://github.com/CenterForTheBuiltEnvironment/clima/discussions",
        ),
        ("Documentation", "https://center-for-the-built-environment.gitbook.io/clima/"),
        (
            "License",
            "https://center-for-the-built-environment.gitbook.io/clima/#license",
        ),
    ]

    return dmc.Box(
        id=ElementIds.FOOTER_CONTAINER,
        p="md",
        m=0,
        c="white",
        bg="#003262",
        display="flex",
        w="100%",
        style={
            "flexWrap": "nowrap",
            "minHeight": "fit-content",
            "alignItems": "flex-start",
        },
        children=[
            # Logo section
            dmc.Box(
                children=[
                    dmc.Anchor(
                        href="https://cbe.berkeley.edu/",
                        children=dmc.Image(
                            src="assets/img/cbe-logo.png",
                            alt="CBE Logo",
                            h=65,
                            w="auto",
                            fit="contain",
                        ),
                    ),
                ],
                flex="0 0 33.333333%",
                maw="33.333333%",
                p="30px 15px 10px 25px",
                display="flex",
                style={"justifyContent": "flex-start", "alignItems": "flex-start"},
            ),
            # Content section
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
                                style={
                                    "fontSize": "16px",
                                    "lineHeight": 1.5,
                                    "fontWeight": 500,
                                    "color": "white",
                                },
                            ),
                            dmc.Group(
                                [
                                    dmc.Anchor(text, href=url, **white_anchor_style)
                                    for text, url in footer_links
                                ],
                                gap="sm",
                                mt="md",
                            ),
                        ],
                        mt="md",
                    ),
                ],
                flex="0 0 66.666667%",
                maw="66.666667%",
                p="0px 15px 10px 15px",
                display="flex",
                style={"justifyContent": "flex-start", "alignItems": "flex-start"},
            ),
        ],
    )


def banner():
    """Top banner rewritten with dash-mantine-components only."""
    return dmc.Box(
        id=ElementIds.BANNER,
        p="md",
        bg="#003262",
        c="white",
        pos="relative",
        style={"zIndex": 1},
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
                            dmc.Image(
                                src="assets/img/cbe-logo-small.png", h=40, w="auto"
                            ),
                            dmc.Stack(
                                gap=2,
                                children=[
                                    dmc.Title(
                                        "CBE Clima Tool",
                                        id=ElementIds.BANNER_TITLE,
                                        order=2,
                                        fw=500,
                                        ff="'Open Sans', sans-serif",
                                        lh=1.1,
                                        c="white",
                                    ),
                                    dmc.Text(
                                        "Current Location: N/A",
                                        id=ElementIds.ID_LAYOUT_BANNER_SUBTITLE,
                                        size="sm",
                                        opacity=0.85,
                                        ff="'Poppins', sans-serif",
                                        fw=400,
                                        h=25,
                                        style={"overflow": "hidden"},
                                        c="white",
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
    """create sidebar"""
    return dmc.Drawer(
        id=ElementIds.SIDE_BAR,
        title=dmc.Group(
            [
                dmc.Image(src="assets/img/cbe-logo-small.png", h=30, w="auto"),
                dmc.Text("CBE Clima Tool", fw=600),
            ]
        ),
        size="300px",
        zIndex=1001,
        opened=False,
        styles={
            "content": {
                "top": "80px",
                "left": 0,
                "position": "fixed",
                "borderRadius": "0 8px 8px 0",
                "boxShadow": "2px 0 8px rgba(0,0,0,0.1)",
                "backgroundColor": "#f8f9fa",
                "padding": "16px",
            },
            "overlay": {
                "top": "80px",
                "left": 0,
                "height": "calc(100vh - 80px)",
                "position": "fixed",
            },
            "header": {
                "borderBottom": "1px solid #e9ecef",
                "paddingBottom": "12px",
                "marginBottom": "16px",
                "position": "sticky",
                "top": 0,
                "backgroundColor": "#f8f9fa",
                "zIndex": 1002,
            },
            "title": {
                "fontWeight": 600,
                "fontSize": "18px",
                "paddingRight": 30,
                "position": "relative",
                "zIndex": 1001,
            },
            "body": {
                "padding": 0,
                "overflowY": "auto",
                "maxHeight": "calc(100vh - 80px)",
                "position": "relative",
                "zIndex": 1,
            },
        },
        children=[dmc.Stack(gap=0, children=build_sidebar_nav_items())],
    )


def build_sidebar_nav_items():
    nav_link_styles = {
        "root": {
            "borderRadius": "6px",
            "transition": "all 0.2s ease",
            "&:hover": {"backgroundColor": "#e3f2fd"},
            "&[data-active='true']": {
                "backgroundColor": "#1976d2",
                "color": "white",
                "fontWeight": 600,
            },
            "&[data-active='true']:hover": {
                "backgroundColor": "#1565c0",
                "color": "white",
            },
        }
    }

    # === Secondary Menu ===
    sub_links = [
        dmc.NavLink(
            label=page[ColNames.NAME],
            leftSection=DashIconify(
                icon=PageIcon.get_icon(page[ColNames.NAME]), width=20
            ),
            href=page[ColNames.PATH],
            id=f"nav-{page[ColNames.PATH].replace('/', '')}",
            active=False,
            mb="xs",
            styles=nav_link_styles,
        )
        for page in dash.page_registry.values()
        if page[ColNames.NAME] not in ["404"]
    ]

    # Primary Menu
    parent_group = dmc.NavLink(
        label="Pages Menu",
        leftSection=DashIconify(icon="tabler:list-details", width=20),
        children=sub_links,
        id=ElementIds.NAV_GROUP_MAIN,
        variant="light",
        childrenOffset=18,
    )

    segmented_control_styles = {
        "root": {"width": "100%"},
        "control": {"flex": 1, "minWidth": 0},
    }

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
                    {"label": "Local Value Ranges", "value": "local"},
                ],
                radius="md",
                size="sm",
                w="100%",
                styles=segmented_control_styles,
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
                w="100%",
                styles=segmented_control_styles,
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
        m=0,
        mt=0,
        children=[
            store(),
            dmc.Box(
                id=ElementIds.TABS_CONTENT,
                p="md",
                children=[
                    alert(),
                    dash.page_container,
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
    return not opened if n_clicks else opened


@callback(
    Output(ElementIds.SIDE_BAR, "opened", allow_duplicate=True),
    Input(ElementIds.LAYOUT_URL, "pathname"),
    prevent_initial_call="initial_duplicate",
)
def close_sidebar_on_navigation(pathname):
    return False


# Callback to set active state for navigation links based on current URL
@callback(
    [
        Output(f"nav-{page[ColNames.PATH].replace('/', '')}", "active")
        for page in dash.page_registry.values()
        if page[ColNames.NAME] not in ["404"]
    ],
    Input(ElementIds.LAYOUT_URL, "pathname"),
    prevent_initial_call=True,
)
def update_nav_active_state(pathname):
    """Update active state of navigation links based on current URL pathname"""
    return [
        pathname == page[ColNames.PATH]
        for page in dash.page_registry.values()
        if page[ColNames.NAME] not in ["404"]
    ]


@callback(
    Output(ElementIds.ID_LAYOUT_ALERT_AUTO, "style"),
    Input(ElementIds.ID_LAYOUT_INTERVAL_COMPONENT, "n_intervals"),
    prevent_initial_call=True,
)
def show_alert_after_delay(n_intervals):
    """Show alert after 6 seconds, then hide after 5 more seconds"""
    base_style = {
        "position": "fixed",
        "top": "25px",
        "right": "10px",
        "width": "400px",
        "zIndex": 1002,
    }

    # Determine display status based on the number of intervals
    if n_intervals == 1:
        return {**base_style, "display": "block"}
    else:
        return {**base_style, "display": "none"}
