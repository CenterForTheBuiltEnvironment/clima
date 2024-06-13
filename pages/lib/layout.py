import dash_bootstrap_components as dbc
import dash
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
                                href=page["path"],
                                active="exact",
                                className="nav-link"
                            ),
                            className="custom-tab"
                        )
                        for page in dash.page_registry.values() if page["name"] not in ["404", "changelog"]
                        ],
                        id="tabs",
                        class_name="tab-container",
                        pills=True,
                        justified=True
                    )
                ]
            ),
            
            html.Div(
                id="store-container",
                children=[
                    store(),
                    html.Div(
                        id="tabs-content",
                        children=dash.page_container
                    )
                ]
            ),
        ]
    )