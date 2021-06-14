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
                    html.P(
                        "The CBE Clima Tool is licensed under a Creative Commons Attribution-Commercial 4.0 International License"
                    ),
                    html.A(
                        "Version: 0.1.0",
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
                    [Juliet Kim](https://www.linkedin.com/in/suhyangkim/).
                    
                    Supported browsers: Google Chrome, Opera.
                    """
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
                        value="global",
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
                value="tab-1",
                children=[
                    dcc.Tab(
                        label="Select Weather File",
                        value="tab-1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        label="Climate Summary",
                        value="tab-2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        label="Temperature and Humidity",
                        value="tab-3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        label="Sun and Clouds",
                        value="tab-4",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        label="Wind",
                        value="tab-5",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        label="Psychrometric Chart",
                        value="tab-9",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        label="Data Explorer",
                        value="tab-6",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        label="Outdoor Comfort",
                        value="tab-7",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        label="Natural Ventilation",
                        value="tab-8",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            ),
            html.Div(
                id="store-container",
                children=[store(), html.Div(id="tabs-content"), footer()],
            ),
        ],
    )


def changelog():
    """changelog page"""
    f = open("CHANGELOG.md", "r")

    return dbc.Container(
        className="container p-4",
        children=[dcc.Markdown(f.read())],
    )


def store():
    return html.Div(
        id="store",
        children=[
            dcc.Store(id="df-store", storage_type="session"),
            dcc.Store(id="meta-store", storage_type="session"),
        ],
    )
