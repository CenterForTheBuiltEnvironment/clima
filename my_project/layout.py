import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def footer():
    return html.Div(
        id="footer-container",
        className="container-row",
        children=[
            html.Div(
                className="container-col",
                id="footer-left-container",
                children=[
                    html.A(
                        children=[
                            html.Img(
                                id="cbe-logo",
                                src="assets/img/cbe-logo.png",
                                className="mb-2",
                            )
                        ],
                        href="https://cbe.berkeley.edu/",
                    ),
                    html.A(
                        "The CBE Clima Tool is licensed under a Creative Commons Attribution-Commercial 4.0 International License (CC BY 4.0)",
                        href="https://creativecommons.org/licenses/by/4.0/",
                    ),
                    html.A(
                        "Version: 0.3.2",
                        href="/changelog",
                    ),
                ],
            ),
            html.Div(
                className="container-row",
                id="footer-right-container",
                children=[
                    dcc.Markdown(
                        """
                    Developed by [Giovanni Betti](https://www.linkedin.com/in/gbetti/), 
                    [Christine Nguyen](https://chrlng.github.io/),
                    [Federico Tartarini](https://www.linkedin.com/in/federico-tartarini-3991995b/).
                    
                    Supported browsers: Chromium-based browsers, Firefox.
                    
                    Report issues with the Clima app [here](https://github.com/CenterForTheBuiltEnvironment/clima/issues).
                    """,
                    ),
                ],
            ),
        ],
    )


def build_banner():
    """Build the banner at the top of the page.

    TO DO: add in global and local buttons
    """
    return html.Div(
        id="banner",
        className="container-row",
        children=[
            html.Div(
                id="banner-text-left",
                className="container-row",
                children=[
                    html.A(
                        href="/",
                        children=[
                            html.Img(
                                id="logo-small", src="assets/img/cbe-logo-small.png"
                            ),
                        ],
                    ),
                    html.Div(
                        className="container-col",
                        children=[
                            html.H1(id="banner-title", children=["CBE Clima Tool"]),
                            html.H5(
                                id="banner-subtitle", children=["Current Location: N/A"]
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                id="banner-text-right",
                className="container-col",
                children=[
                    dbc.RadioItems(
                        options=[
                            {"label": "Global Value Ranges", "value": "global"},
                            {"label": "Local Value Ranges", "value": "local"},
                        ],
                        value="local",
                        id="global-local-radio-input",
                        inline=True,
                    ),
                ],
            ),
        ],
    )


def build_tabs():
    """Build the seven different tabs."""
    return html.Div(
        id="tabs-container",
        children=[
            dcc.Tabs(
                id="tabs",
                parent_className="custom-tabs",
                value="tab-select",
                children=[
                    dcc.Tab(
                        label="Select Weather File",
                        value="tab-select",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="tab-summary",
                        label="Climate Summary",
                        value="tab-summary",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        disabled=True,
                    ),
                    dcc.Tab(
                        id="tab-t-rh",
                        label="Temperature and Humidity",
                        value="tab-t-rh",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        disabled=True,
                    ),
                    dcc.Tab(
                        id="tab-sun",
                        label="Sun and Clouds",
                        value="tab-sun",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        disabled=True,
                    ),
                    dcc.Tab(
                        id="tab-wind",
                        label="Wind",
                        value="tab-wind",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        disabled=True,
                    ),
                    dcc.Tab(
                        id="tab-psy-chart",
                        label="Psychrometric Chart",
                        value="tab-psy-chart",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        disabled=True,
                    ),
                    dcc.Tab(
                        id="tab-outdoor-comfort",
                        label="Outdoor Comfort",
                        value="tab-outdoor-comfort",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        disabled=True,
                    ),
                    dcc.Tab(
                        id="tab-data-explorer",
                        label="Data Explorer",
                        value="tab-data-explorer",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        disabled=True,
                    ),
                ],
            ),
            html.Div(
                id="store-container",
                children=[store(), html.Div(id="tabs-content")],
            ),
        ],
    )


def store():
    return html.Div(
        id="store",
        children=[
            dcc.Store(id="df-store", storage_type="session"),
            dcc.Store(id="meta-store", storage_type="session"),
            dcc.Store(id="url-store", storage_type="session"),
        ],
    )
