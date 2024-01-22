import dash_bootstrap_components as dbc
from dash import dcc, html


def footer():
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
                                [Version: 0.8.17](https://center-for-the-built-environment.gitbook.io/clima/version/changelog)
                                """
                            ),
                            dcc.Markdown(
                                """
                                    [Contributors](https://cbe-berkeley.gitbook.io/clima/#contributions),
                                    [Report issues on GitHub](https://github.com/CenterForTheBuiltEnvironment/clima/issues),
                                    [Contact us page](https://forms.gle/LRUq3vsFnE1QCLiA6),
                                    [Documentation page](https://center-for-the-built-environment.gitbook.io/clima/),
                                    [License](https://center-for-the-built-environment.gitbook.io/clima/#license)
                                """,
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
            dbc.Row(
                align="center",
                children=[
                    dbc.Col(
                        html.A(
                            href="/",
                            children=[
                                html.Img(
                                    src="assets/img/cbe-logo-small.png",
                                ),
                            ],
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        children=[
                            html.H1(id="banner-title", children=["CBE Clima Tool"]),
                            html.H5(
                                id="banner-subtitle",
                                children=["Current Location:"],
                            ),
                        ],
                    ),
                    dbc.Col(
                        style={"fontWeight": "400", "padding": "1rem"},
                        align="end",
                        children=[
                            dbc.Row(
                                style={"text-align": "right"},
                                children=[
                                    dbc.RadioItems(
                                        options=[
                                            {
                                                "label": "Global Value Ranges",
                                                "value": "global",
                                            },
                                            {
                                                "label": "Local Value Ranges",
                                                "value": "local",
                                            },
                                        ],
                                        value="local",
                                        id="global-local-radio-input",
                                        inline=True,
                                    ),
                                ],
                            ),
                            dbc.Row(
                                align="end",
                                style={"text-align": "right"},
                                children=[
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "SI", "value": "si"},
                                            {"label": "IP", "value": "ip"},
                                        ],
                                        value="si",
                                        id="si-ip-radio-input",
                                        inline=True,
                                    ),
                                ],
                            ),
                        ],
                        width="auto",
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
                        id="tab-natural-ventilation",
                        label="Natural Ventilation",
                        value="tab-natural-ventilation",
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
            dcc.Loading(
                [
                    dcc.Store(id="df-store", storage_type="session"),
                    dcc.Store(id="meta-store", storage_type="session"),
                    dcc.Store(id="url-store", storage_type="session"),
                    dcc.Store(id="si-ip-unit-store", storage_type="session"),
                    dcc.Store(id="lines-store", storage_type="session"),
                ],
                fullscreen=True,
                type="dot",
            )
        ],
    )
