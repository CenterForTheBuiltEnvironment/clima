import dash
from dash import dcc, Input, Output, State, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from pages.lib.global_variables import Variables
from config import DocLinks, UnitSystem
from pages.lib.global_element_ids import ElementIds
from pages.lib.utils import (
    determine_month_and_hour_filter,
    get_default_global_filter_store_data,
    get_global_filter_state,
)


class NavBarIcons:
    _ICON_MAP = {
        "Climate Summary": "tabler:chart-bar",
        "Temperature and Humidity": "tabler:temperature",
        "Sun and Clouds": "tabler:sun",
        "Wind": "tabler:wind",
        "Psychrometric Chart": "tabler:chart-dots",
        "Natural Ventilation": "tabler:windmill",
        "Outdoor Comfort": "tabler:thermometer",
        "Data Explorer": "tabler:database",
        "Changelog": "tabler:history",
    }

    CLIMATE_SUMMARY = _ICON_MAP["Climate Summary"]
    TEMPERATURE_AND_HUMIDITY = _ICON_MAP["Temperature and Humidity"]
    SUN_AND_CLOUDS = _ICON_MAP["Sun and Clouds"]
    WIND = _ICON_MAP["Wind"]
    PSYCHROMETRIC_CHART = _ICON_MAP["Psychrometric Chart"]
    NATURAL_VENTILATION = _ICON_MAP["Natural Ventilation"]
    OUTDOOR_COMFORT = _ICON_MAP["Outdoor Comfort"]
    DATA_EXPLORER = _ICON_MAP["Data Explorer"]
    CHANGELOG = _ICON_MAP["Changelog"]

    @classmethod
    def get_icon(cls, page_name):
        """Get icon for a page name."""
        return cls._ICON_MAP.get(page_name, "tabler:circle")


# global filters
def create_tools_filter_components():
    # Apply month and hour filter (reduced nesting, same visual layout)
    return dmc.Stack(
        id=ElementIds.TOOLS_MONTH_HOUR_SECTION,
        children=[
            dmc.Divider(label="Filters", size="xs", color="blue"),
            # Month controls
            dmc.Text("Month Range:", size="xs", c="dimmed"),
            dcc.RangeSlider(
                id=ElementIds.TOOLS_MONTH_SLIDER,
                min=1,
                max=12,
                step=1,
                value=[1, 12],
                marks={1: "1", 12: "12"},
                tooltip={
                    "always_visible": False,
                    "placement": "top",
                },
                allowCross=False,
            ),
            dmc.Group(
                [
                    dmc.Switch(
                        id=ElementIds.TOOLS_INVERT_MONTH,
                        label="Invert",
                        checked=False,
                        size="xs",
                        color="blue",
                        style={"fontSize": "0.7rem"},
                    ),
                ],
                justify="flex-end",
            ),
            # Hour controls
            dmc.Text("Hour Range:", size="xs", c="dimmed"),
            dcc.RangeSlider(
                id=ElementIds.TOOLS_HOUR_SLIDER,
                min=0,
                max=24,
                step=1,
                value=[0, 24],
                marks={0: "0", 24: "24"},
                tooltip={
                    "always_visible": False,
                    "placement": "top",
                },
                allowCross=False,
            ),
            dmc.Group(
                [
                    dmc.Switch(
                        id=ElementIds.TOOLS_INVERT_HOUR,
                        label="Invert",
                        checked=False,
                        size="xs",
                        color="blue",
                        style={"fontSize": "0.7rem"},
                    ),
                ],
                justify="flex-end",
            ),
            dmc.Button(
                "Apply month and hour filter",
                id=ElementIds.TOOLS_APPLY_MONTH_HOUR_FILTER,
                color="blue",
                variant="filled",
                size="xs",
            ),
        ],
        gap="xs",
        p="xs",
    )


def create_navbar():
    nav_link_styles = {
        "root": {
            "borderRadius": "0.375rem",
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

    # Select weather file - top-level menu item
    select_weather_file_page = next(
        (
            page
            for page in dash.page_registry.values()
            if page[Variables.NAME.col_name] == "Select weather file"
        ),
        None,
    )
    select_weather_file_link = (
        dmc.NavLink(
            label=select_weather_file_page[Variables.NAME.col_name],
            href=select_weather_file_page[Variables.PATH.col_name],
            id=f"nav-{select_weather_file_page[Variables.PATH.col_name].replace('/', '')}",
            active=False,
            styles=nav_link_styles,
        )
        if select_weather_file_page
        else None
    )

    # Secondary Menu - exclude "Select weather file" as it will be a top-level menu
    sub_links = [
        dmc.NavLink(
            label=page[Variables.NAME.col_name],
            leftSection=DashIconify(
                icon=NavBarIcons.get_icon(page[Variables.NAME.col_name]), width=20
            ),
            href=page[Variables.PATH.col_name],
            id=f"nav-{page[Variables.PATH.col_name].replace('/', '')}",
            active=False,
            styles=nav_link_styles,
        )
        for page in dash.page_registry.values()
        if page[Variables.NAME.col_name]
        not in ["404", "Changelog", "Select weather file"]
    ]

    parent_group = dmc.NavLink(
        label="Visualize weather file",
        children=sub_links,
        id=ElementIds.NAV_GROUP_MAIN,
        variant="light",
        childrenOffset=0,
        opened=True,
    )

    segmented_control_styles = {
        "control": {"flex": 1, "minWidth": 0},
    }

    controls_stack = dmc.Stack(
        gap="xs",
        p="xs",
        children=[
            dmc.Divider(label="Units and Ranges", size="xs", color="blue"),
            dmc.Tooltip(
                label=dmc.Text("You can choose value ranges between Global and Local"),
                position="right",
                withArrow=True,
                children=dmc.SegmentedControl(
                    id=ElementIds.SHARED_GLOBAL_LOCAL_RADIO_INPUT,
                    value="local",
                    color="blue",
                    data=[
                        {"label": "Global", "value": "global"},
                        {"label": "Local", "value": "local"},
                    ],
                    w=210,
                    size="sm",
                    styles=segmented_control_styles,
                ),
            ),
            dmc.Tooltip(
                label=dmc.Text("You can choose units between SI and IP"),
                position="right",
                withArrow=True,
                children=dmc.SegmentedControl(
                    id=ElementIds.SHARED_SI_IP_RADIO_INPUT,
                    value=UnitSystem.SI,
                    color="blue",
                    data=[
                        {"label": "SI", "value": UnitSystem.SI},
                        {"label": "IP", "value": UnitSystem.IP},
                    ],
                    w=210,
                    size="sm",
                    styles=segmented_control_styles,
                ),
            ),
        ],
    )

    filter_components = create_tools_filter_components()

    # Tools
    controls_group = dmc.NavLink(
        label="Filters and units",
        children=[filter_components, controls_stack],
        id=ElementIds.NAV_GROUP_CONTROLS,
        variant="light",
        childrenOffset=0,
        opened=True,
    )

    # Documentation
    doc_link = dmc.NavLink(
        label="Documentation",
        href=DocLinks.MAIN.value,
        target="_blank",
        id=ElementIds.NAV_DOC_LINK,
        variant="light",
    )

    return dmc.ScrollArea(
        children=[
            select_weather_file_link,
            parent_group,
            controls_group,
            doc_link,
        ],
    )


def create_header():
    return dmc.Group(
        [
            dmc.Burger(
                id=ElementIds.BURGER_BUTTON,
                size="sm",
                opened=True,
                color="blue",
            ),
            dmc.Anchor(
                href="/",
                children=dmc.Image(src="assets/img/cbe-logo-small.png", h=40, flex=0),
            ),
            dmc.Stack(
                gap="xs",
                children=[
                    dmc.Title(
                        "CBE Clima Tool",
                        order=2,
                        lh=1.1,
                        c="white",
                    ),
                    dmc.Text(
                        "Current Location: N/A",
                        id=ElementIds.ID_SELECT_BANNER_SUBTITLE,
                        size="sm",
                        style={"overflow": "hidden"},
                        c="white",
                    ),
                ],
                p="xs",
            ),
            dmc.Alert(
                [
                    "If you have a moment, help us improve Clima and take a ",
                    dmc.Anchor(
                        "quick user survey",
                        href="https://forms.gle/k289zP3R92jdu14M7",
                        target="_blank",
                        c="white",
                        underline="always",
                    ),
                    "! ☀️",
                ],
                id=ElementIds.ID_LAYOUT_ALERT_AUTO,
                title="CBE Clima User Survey",
                icon=dmc.ThemeIcon(
                    DashIconify(icon="tabler:info-circle", color="white"),
                ),
                color="blue",
                variant="filled",
                withCloseButton=True,
                w=400,
                pos="fixed",
                top="1em",
                right="1em",
                style={"zIndex": 1002, "display": "none"},
            ),
        ],
        pl="md",
    )


def create_footer():
    white_anchor_style = {
        "underline": "always",
        "c": "white",
        "target": "_blank",
    }

    footer_links = [
        (
            "Version: 0.10.1",
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

    return dmc.Group(
        [
            dmc.Anchor(
                href="https://cbe.berkeley.edu/",
                children=dmc.Image(
                    src="assets/img/cbe-logo.png",
                    alt="CBE Logo",
                    h=40,
                    w="auto",
                    fit="contain",
                ),
            ),
            dmc.Stack(
                gap="xs",
                children=[
                    dcc.Markdown(
                        """
                        Please cite us: Betti, G., Tartarini, F., Nguyen, C, Schiavon, S. CBE Clima Tool: A free and open-source web application for climate analysis tailored to sustainable building design. Build. Simul. (2023). [https://doi.org/10.1007/s12273-023-1090-5](https://doi.org/10.1007/s12273-023-1090-5).
                        """,
                        style={
                            "fontSize": "1rem",
                            "lineHeight": 1.3,
                            "fontWeight": 400,
                            "color": "white",
                            "textAlign": "left",
                        },
                    ),
                    dmc.Group(
                        [
                            dmc.Anchor(text, href=url, **white_anchor_style)
                            for text, url in footer_links
                        ],
                        gap="sm",
                        wrap="wrap",
                        justify="flex-start",
                    ),
                ],
                flex=1,
                align="flex-start",
                ml="xl",
            ),
        ],
        id=ElementIds.FOOTER_CONTAINER,
        p="sm",
        c="white",
        bg="#003262",
        justify="flex-start",
        align="center",
    )


def create_stores():
    return dmc.Box(
        id=ElementIds.STORE,
        children=[
            dcc.Store(id=ElementIds.SHARED_DF_STORE, storage_type="session"),
            dcc.Store(id=ElementIds.SHARED_META_STORE, storage_type="session"),
            dcc.Store(id=ElementIds.SHARED_URL_STORE, storage_type="session"),
            dcc.Store(id=ElementIds.SHARED_SI_IP_UNIT_STORE, storage_type="session"),
            dcc.Store(id=ElementIds.SHARED_LINES_STORE, storage_type="session"),
            dcc.Store(
                id=ElementIds.TOOLS_MENU_EXPANDED, data=False, storage_type="session"
            ),
            dcc.Store(
                id=ElementIds.TOOLS_GLOBAL_FILTER_STORE,
                data=get_default_global_filter_store_data(),
                storage_type="session",
            ),
            dcc.Interval(
                id=ElementIds.ID_LAYOUT_INTERVAL_COMPONENT,
                interval=12 * 1000,
                n_intervals=0,
            ),
        ],
    )


def create_collapsible_layout():
    return dmc.AppShell(
        [
            dmc.AppShellHeader(
                create_header(),
                bg="#003262",
            ),
            dmc.AppShellNavbar(
                id=ElementIds.NAVBAR,
                children=create_navbar(),
                bg="#f8f9fa",
            ),
            # including main and footer
            dmc.AppShellMain(
                children=[
                    create_stores(),
                    dash.page_container,
                    create_footer(),
                ],
                pos="relative",
                style={
                    "zIndex": 1,
                    "@media (max-width: 48rem)": {
                        "left": "0",
                    },
                },
            ),
        ],
        header={"height": 80},
        navbar={
            "width": 230,
            "breakpoint": "sm",
            "collapsed": {"mobile": True, "desktop": False},
            "id": ElementIds.NAVBAR_CONTAINER,
        },
        id=ElementIds.APP_SHELL,
    )


@callback(
    [
        Output(ElementIds.APP_SHELL, "navbar"),
        Output(ElementIds.TOOLS_MENU_EXPANDED, "data"),
    ],
    [
        Input(ElementIds.BURGER_BUTTON, "opened"),
        Input(ElementIds.NAV_GROUP_CONTROLS, "opened"),
        Input(ElementIds.NAV_GROUP_MAIN, "opened"),
    ],
    [
        State(ElementIds.APP_SHELL, "navbar"),
        State(ElementIds.TOOLS_MENU_EXPANDED, "data"),
    ],
)
def toggle_navbar_and_width(
    burger_opened, tools_opened, pages_opened, navbar, tools_expanded
):
    navbar["collapsed"] = {"mobile": not burger_opened, "desktop": not burger_opened}

    WIDTHS = {"default": 230, "pages": 230, "tools": 230}

    if tools_opened is not None:
        tools_expanded = tools_opened
        navbar["width"] = (
            WIDTHS["tools"]
            if tools_opened
            else (WIDTHS["pages"] if pages_opened else WIDTHS["default"])
        )
    elif pages_opened is not None:
        navbar["width"] = WIDTHS["pages"] if pages_opened else WIDTHS["default"]

    return navbar, tools_expanded


@callback(
    [
        Output(f"nav-{page[Variables.PATH.col_name].replace('/', '')}", "active")
        for page in dash.page_registry.values()
        if page[Variables.NAME.col_name] not in ["404", "Changelog"]
    ],
    Input(ElementIds.MAIN_URL, "pathname"),
    prevent_initial_call=True,
)
def update_nav_active_state(pathname):
    return [
        pathname == page[Variables.PATH.col_name]
        for page in dash.page_registry.values()
        if page[Variables.NAME.col_name] not in ["404", "Changelog"]
    ]


@callback(
    Output(ElementIds.ID_LAYOUT_ALERT_AUTO, "style"),
    Input(ElementIds.ID_LAYOUT_INTERVAL_COMPONENT, "n_intervals"),
    prevent_initial_call=True,
)
def show_alert_after_delay(n_intervals):
    return {"display": "block" if n_intervals == 1 else "none"}


@callback(
    Output(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    [
        Input(ElementIds.TOOLS_APPLY_MONTH_HOUR_FILTER, "n_clicks"),
    ],
    [
        State(ElementIds.TOOLS_MONTH_SLIDER, "value"),
        State(ElementIds.TOOLS_HOUR_SLIDER, "value"),
        State(ElementIds.TOOLS_INVERT_MONTH, "checked"),
        State(ElementIds.TOOLS_INVERT_HOUR, "checked"),
        State(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    prevent_initial_call=True,
)
def update_global_filter_state(
    apply_clicks, month_range, hour_range, invert_month, invert_hour, current_data
):
    if not apply_clicks:
        return current_data or get_default_global_filter_store_data()

    # Normalize existing data, then override with inputs
    base_state = get_global_filter_state(current_data)
    updated_state = {
        **base_state,
        "filter_active": True,
        "month_range": month_range or base_state["month_range"],
        "hour_range": hour_range or base_state["hour_range"],
        # store as booleans; readers use get_global_filter_state for coercion
        "invert_month": bool(invert_month),
        "invert_hour": bool(invert_hour),
    }

    return updated_state


def apply_global_month_hour_filter(df, filter_store_data, target_columns=None):
    filter_state = get_global_filter_state(filter_store_data)

    if not filter_state["filter_active"]:
        df_copy = df.copy()
        df_copy["_is_filtered"] = False
        return df_copy

    month_range = filter_state["month_range"]
    hour_range = filter_state["hour_range"]
    invert_month = filter_state["invert_month"]
    invert_hour = filter_state["invert_hour"]

    start_month, end_month, start_hour, end_hour = determine_month_and_hour_filter(
        month_range, hour_range, invert_month, invert_hour
    )

    df_copy = df.copy()

    if target_columns is None:
        target_columns = [Variables.DBT.col_name]
    elif isinstance(target_columns, str):
        target_columns = [target_columns]

    if start_month <= end_month:
        month_mask = (df_copy[Variables.MONTH.col_name] < start_month) | (
            df_copy[Variables.MONTH.col_name] > end_month
        )
    else:
        month_mask = (df_copy[Variables.MONTH.col_name] >= end_month) & (
            df_copy[Variables.MONTH.col_name] <= start_month
        )

    if start_hour <= end_hour:
        hour_mask = (df_copy[Variables.HOUR.col_name] < start_hour) | (
            df_copy[Variables.HOUR.col_name] > end_hour
        )
    else:
        hour_mask = (df_copy[Variables.HOUR.col_name] >= end_hour) & (
            df_copy[Variables.HOUR.col_name] <= start_hour
        )

    df_copy["_is_filtered"] = month_mask | hour_mask

    for target_col in target_columns:
        df_copy[f"_{target_col}_original"] = df_copy[target_col]

        from pages.lib.template_graphs import time_filtering

        time_filtering(
            df_copy, start_month, end_month, Variables.MONTH.col_name, target_col
        )
        time_filtering(
            df_copy, start_hour, end_hour, Variables.HOUR.col_name, target_col
        )

    return df_copy


@callback(
    [
        Output(ElementIds.TOOLS_MONTH_SLIDER, "value"),
        Output(ElementIds.TOOLS_HOUR_SLIDER, "value"),
        Output(ElementIds.TOOLS_INVERT_MONTH, "checked"),
        Output(ElementIds.TOOLS_INVERT_HOUR, "checked"),
    ],
    [
        Input(ElementIds.TOOLS_GLOBAL_FILTER_STORE, "data"),
    ],
    prevent_initial_call=False,
)
def sync_sliders_with_global_state(global_filter_data):
    state = get_global_filter_state(global_filter_data)
    return (
        state["month_range"],
        state["hour_range"],
        state["invert_month"],
        state["invert_hour"],
    )
