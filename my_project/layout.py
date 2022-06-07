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
                    dbc.Row(
                        dcc.Markdown(
                            """
                            [The CBE Clima Tool is licensed under a Creative Commons 
                            Attribution-Commercial 4.0 International License (CC BY 
                            4.0)](https://creativecommons.org/licenses/by/4.0/)
                            
                            [Version: 0.6.3](https://center-for-the-built-environment.gitbook.io/clima/version/changelog)
                            """
                        ),
                        style={"padding": "25px 0px"},
                    ),
                ],
                width=12,
                md=4,
                style={"padding": "15px"},
            ),
            dbc.Col(
                children=[
                    dbc.Row(
                        dcc.Markdown(
                            """
                                Please cite us if you use this software:
                                Betti, G., Tartarini, F., Schiavon, S., Nguyen, C. (2021). 
                                CBE Clima Tool. Version 0.4.6. Center for the Built Environment, University of California Berkeley
                            
                                Developed by:
                                [Giovanni Betti](https://www.linkedin.com/in/gbetti/),
                                [Federico Tartarini](https://www.linkedin.com/in/federico-tartarini-3991995b/).
                                [Christine Nguyen](https://chrlng.github.io/),
            
                                Supported browsers: Chromium-based browsers, Firefox.
            
                                Report issues on [GitHub](https://github.com/CenterForTheBuiltEnvironment/clima/issues).
            
                                [Contact us](https://forms.gle/LRUq3vsFnE1QCLiA6)
                                
                                [Documentation](https://center-for-the-built-environment.gitbook.io/clima/)
                            """,
                        ),
                        style={"marginTop": "1rem"},
                    ),
                ],
                width=12,
                md=6,
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
                        children=[
                            dbc.RadioItems(
                                options=[
                                    {"label": "Global Value Ranges", "value": "global"},
                                    {"label": "Local Value Ranges", "value": "local"},
                                ],
                                value="local",
                                id="global-local-radio-input",
                                inline=False,
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
            dcc.Store(id="df-store", storage_type="session"),
            dcc.Store(id="meta-store", storage_type="session"),
            dcc.Store(id="url-store", storage_type="session"),
        ],
    )
