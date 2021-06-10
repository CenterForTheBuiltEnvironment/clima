import dash_core_components as dcc
import dash_html_components as html
from my_project.global_scheme import config, month_lst, container_row_center_full


def sliders():
    """Returns 2 sliders for the hour"""
    return html.Div(
        className="container-col container-center",
        id="slider-container",
        children=[
            html.H3("Customizable Wind Rose"),
            html.Div(
                className="container-row each-slider",
                children=[
                    html.P("Month Range"),
                    dcc.RangeSlider(
                        id="month-slider",
                        min=1,
                        max=12,
                        step=1,
                        value=[1, 12],
                        marks={1: "1", 12: "12"},
                        tooltip={"always_visible": False, "placement": "top"},
                        allowCross=True,
                    ),
                ],
            ),
            html.Div(
                className="container-row each-slider",
                children=[
                    html.P("Hour Range"),
                    dcc.RangeSlider(
                        id="hour-slider",
                        min=1,
                        max=24,
                        step=1,
                        value=[1, 24],
                        marks={1: "1", 24: "24"},
                        tooltip={"always_visible": False, "placement": "topLeft"},
                        allowCross=False,
                    ),
                ],
            ),
        ],
    )


def seasonal_wind_rose():
    """Return the section with the 4 seasonal wind rose graphs."""
    return html.Div(
        className="container-col full-width",
        children=[
            html.H5("Seasonal Wind Rose"),
            html.Div(
                className=container_row_center_full,
                children=[
                    html.Div(
                        className="container-col",
                        children=[
                            # dcc.Graph(
                            #     className = "seasonal-graph",
                            #     id = "winter-wind-rose",
                            #     config = config
                            # ),
                            dcc.Loading(
                                type="circle",
                                children=[
                                    dcc.Graph(
                                        className="seasonal-graph",
                                        id="winter-wind-rose",
                                        config=config,
                                    ),
                                ],
                            ),
                            html.P(
                                className="seasonal-text", id="winter-wind-rose-text"
                            ),
                        ],
                    ),
                    html.Div(
                        className="container-col",
                        children=[
                            dcc.Loading(
                                type="circle",
                                children=[
                                    dcc.Graph(
                                        className="seasonal-graph",
                                        id="spring-wind-rose",
                                        config=config,
                                    ),
                                ],
                            ),
                            html.P(
                                className="seasonal-text", id="spring-wind-rose-text"
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className=container_row_center_full,
                children=[
                    html.Div(
                        className="container-col",
                        children=[
                            dcc.Loading(
                                type="circle",
                                children=[
                                    dcc.Graph(
                                        className="seasonal-graph",
                                        id="summer-wind-rose",
                                        config=config,
                                    ),
                                ],
                            ),
                            html.P(
                                className="seasonal-text", id="summer-wind-rose-text"
                            ),
                        ],
                    ),
                    html.Div(
                        className="container-col",
                        children=[
                            dcc.Loading(
                                type="circle",
                                children=[
                                    dcc.Graph(
                                        className="seasonal-graph",
                                        id="fall-wind-rose",
                                        config=config,
                                    ),
                                ],
                            ),
                            html.P(className="seasonal-text", id="fall-wind-rose-text"),
                        ],
                    ),
                ],
            ),
        ],
    )


def daily_wind_rose():
    """Return the section for the 3 daily wind rose graphs."""
    return html.Div(
        className="container-col full-width",
        id="tab5-daily-container",
        children=[
            html.H5("Daily Wind Rose"),
            html.Div(
                id="daily-wind-rose-outer-container",
                className="container-row full-width",
                children=[
                    html.Div(
                        className="container-col",
                        children=[
                            html.Div(
                                dcc.Loading(
                                    type="circle",
                                    children=[
                                        dcc.Graph(
                                            className="daily-wind-graph",
                                            id="morning-wind-rose",
                                            config=config,
                                        ),
                                    ],
                                ),
                            ),
                            html.P(className="daily-text", id="morning-windrose-text"),
                        ],
                    ),
                    html.Div(
                        className="container-col",
                        children=[
                            html.Div(
                                dcc.Loading(
                                    type="circle",
                                    children=[
                                        dcc.Graph(
                                            className="daily-wind-graph",
                                            id="noon-wind-rose",
                                            config=config,
                                        ),
                                    ],
                                ),
                            ),
                            html.P(className="daily-text", id="noon-windrose-text"),
                        ],
                    ),
                    html.Div(
                        className="container-col",
                        children=[
                            html.Div(
                                dcc.Loading(
                                    type="circle",
                                    children=[
                                        dcc.Graph(
                                            className="daily-wind-graph",
                                            id="night-wind-rose",
                                            config=config,
                                        ),
                                    ],
                                ),
                            ),
                            html.P(className="daily-text", id="night-windrose-text"),
                        ],
                    ),
                ],
            ),
        ],
    )


def custom_windrose():
    """"""
    return html.Div(
        className="container-col container-center full-width",
        id="custom-windrose-container",
        children=[
            html.H4("Customizable Windrose"),
            html.Div(
                className="container-row full-width container-center",
                id="tab5-custom-dropdown-container",
                children=[
                    html.Div(
                        className="container-col container-center tab5-custom-half-container",
                        children=[
                            html.Div(
                                className=container_row_center_full,
                                children=[
                                    html.H6(
                                        className="text-next-to-input",
                                        children=["Start Month:"],
                                    ),
                                    dcc.Dropdown(
                                        id="tab5-custom-start-month",
                                        options=[
                                            {"label": j, "value": i + 1}
                                            for i, j in enumerate(month_lst)
                                        ],
                                        value="1",
                                    ),
                                ],
                            ),
                            html.Div(
                                className=container_row_center_full,
                                children=[
                                    html.H6(
                                        className="text-next-to-input",
                                        children=["Start Hour:"],
                                    ),
                                    dcc.Dropdown(
                                        id="tab5-custom-start-hour",
                                        options=[
                                            {"label": str(i) + ":00", "value": i}
                                            for i in range(1, 25)
                                        ],
                                        value="1",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="container-col tab5-custom-half-container container-center",
                        children=[
                            html.Div(
                                className=container_row_center_full,
                                children=[
                                    html.H6(
                                        className="text-next-to-input",
                                        children=["End Month:"],
                                    ),
                                    dcc.Dropdown(
                                        id="tab5-custom-end-month",
                                        options=[
                                            {"label": j, "value": i + 1}
                                            for i, j in enumerate(month_lst)
                                        ],
                                        value="12",
                                    ),
                                ],
                            ),
                            html.Div(
                                className=container_row_center_full,
                                children=[
                                    html.H6(
                                        className="text-next-to-input",
                                        children=["End Hour:"],
                                    ),
                                    dcc.Dropdown(
                                        id="tab5-custom-end-hour",
                                        options=[
                                            {"label": str(i) + ":00", "value": i}
                                            for i in range(1, 25)
                                        ],
                                        value="24",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="custom-wind-rose", config=config),
                ],
            ),
        ],
    )


def tab_five():
    """Contents in the fifth tab 'Wind'."""
    return html.Div(
        className="container-col",
        id="tab-five-container",
        children=[
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="wind-rose", config=config),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="wind-speed", config=config),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=[
                    dcc.Graph(id="wind-direction", config=config),
                ],
            ),
            seasonal_wind_rose(),
            daily_wind_rose(),
            custom_windrose(),
        ],
    )
