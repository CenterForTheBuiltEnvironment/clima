import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from my_project.global_scheme import config, dropdown_names


def section_one_inputs():
    """ Return the inputs from section one.
    """
    return html.Div(
        className = "container-row full-width row-center",
        children = [
            html.H6(className = "text-next-to-input", children = ["Variable:"]),
            dcc.Dropdown(
                id = "sec1-var-dropdown", 
                options = [
                    {'label': i, 'value': dropdown_names[i]} for i in dropdown_names
                ], 
                value = 'DBT'
            ),
        ]
    )

def section_one():
    """ Return the graphs for section one
    """
    return html.Div(
        className = "container-col full-width",
        children = [
            section_one_inputs(),
            dcc.Loading(
                type = "circle",
                children = [
                    dcc.Graph(
                        className = "full-width",
                        id = 'query-yearly',
                        config = config
                    ),
                ]
            ),
            dcc.Loading(
                type = "circle",
                children = [
                    dcc.Graph(
                        className = "full-width",
                        id = 'query-daily',
                        config = config
                    ),
                ]
            ),
            dcc.Loading(
                type = "circle",
                children = [
                    dcc.Graph(
                        className = "full-width",
                        id = 'query-heatmap',
                        config = config
                    ),
                ]
            ), 
        ]
    )

def section_two_inputs():
    """ Return all the input forms from section two.
    """
    return html.Div(
            className = "container-row full-width three-inputs-container",
            children = [
                html.Div(
                    className = "container-col container-center one-of-three-container",
                    children = [
                        html.Div(
                            className = "container-row row-center full-width",
                            children = [
                                html.H6(
                                    className = "text-next-to-input", 
                                    children = ["Variable:"]
                                ),
                                dcc.Dropdown(
                                    id = "sec2-var-dropdown", 
                                    options = [
                                        {'label': i, 'value': dropdown_names[i]} for i in dropdown_names
                                    ], 
                                    value = 'RH'
                                ),
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className = "container-col container-center one-of-three-container",
                    children = [
                        dbc.Checklist(
                            options = [
                                {"label": "Apply Time Filters", "value": "time"},
                            ],
                            value = [],
                            id = "sec2-time-filter-input",
                        ),
                        html.Div(
                            className = 'container-row full-width container-center',
                            children = [
                                html.H6("Month Range"),
                                dcc.RangeSlider(
                                    id = 'sec2-month-slider',
                                    className = "month-hour-slider",
                                    min = 1,
                                    max = 12,
                                    step = 1,
                                    value = [1, 12], 
                                    marks = {
                                        1: '1',
                                        12: '12'
                                    },
                                    tooltip = {
                                        'always_visible': False,
                                        'placement' : 'top'
                                    },
                                    allowCross = True
                                ),
                            ]
                        ),
                        html.Div(
                            className = 'container-row full-width container-center',
                            children = [
                                html.H6("Hour Range"),
                                dcc.RangeSlider(
                                    className = "month-hour-slider",
                                    id = 'sec2-hour-slider',
                                    min = 1,
                                    max = 24,
                                    step = 1,
                                    value = [1, 24],
                                    marks = {
                                        1: '1',
                                        24: '24'
                                    },
                                    tooltip = {
                                        'always_visible': False,
                                        'placement' : 'topLeft'
                                    },
                                    allowCross = True
                                )
                            ]
                        ),
                    ]
                ), 
                html.Div(
                    className = "container-col container-center one-of-three-container",
                    children = [
                        dbc.Checklist(
                            options = [
                                {"label": "Apply Data Filters", "value": "data"},
                            ],
                            value = [],
                            id = "sec2-data-filter-input",
                        ),
                        html.Div(
                            className = "container-row row-center full-width",
                            children = [
                                html.H6(
                                    className = "text-next-to-input", 
                                    children = ["Filter Variable:"]
                                ),
                                dcc.Dropdown(
                                    id = "sec2-data-filter-var", 
                                    options = [
                                        {'label': i, 'value': dropdown_names[i]} for i in dropdown_names
                                    ], 
                                    value = 'RH'
                                ),
                            ]
                        ),
                        html.Div(
                            className = "container-row row-center full-width",
                            children = [
                                html.H6(
                                    className = "text-next-to-input",
                                    children = ["Min Value:"]
                                ),
                                dbc.Input(
                                    className = "num-input",
                                    id = "sec2-min-val",
                                    placeholder = "Enter a number for the min val",
                                    type = "number", 
                                    min = 0, 
                                    step = 1, 
                                ),
                            ]
                        ),
                        html.Div(
                            className = "container-row row-center full-width",
                            children = [
                                html.H6(
                                    className = "text-next-to-input",
                                    children = ["Max Value:"]
                                ),
                                dbc.Input(
                                    className = "num-input",
                                    id = "sec2-max-val",
                                    placeholder = "Enter a number for the max val",
                                    type = "number", 
                                    min = 0, 
                                    step = 1,
                                ),
                            ]
                        ),
                        # dbc.Button(
                        #     "Apply", color = "primary", className = "mr-1", id = "tab6-sec2-data-button"
                        # )
                    ]
                )
            ]
    )

def section_two():
    """ Return the two graphs in section two.
    """
    return html.Div(
        id = "tab6-sec2-container",
        className = "container-col container-center full-width",
        children = [
            section_two_inputs(),
            dcc.Loading(
                type = "circle",
                children = [
                    dcc.Graph(
                        className = "full-width",
                        id = 'custom-heatmap',
                        config = config
                    ),
                ]
            ),
            dbc.Checklist(
                options = [
                    {"label": "Normalize", "value": "normal"},
                ],
                value = [],
                id = "normalize",
            ),
            dcc.Loading(
                type = "circle",
                children = [
                    dcc.Graph(
                        className = "full-width",
                        id = 'custom-summary',
                        config = config
                    ),
                ]
            ),
        ]
    )

def section_three_inputs():
    """
    """
    return html.Div(
        className = "container-row full-width three-inputs-container",
        children = [
            html.Div(
                className = "container-col container-center one-of-three-container",
                children = [
                    html.Div(
                        className = "container-row row-center full-width",
                        children = [
                            html.H6(
                                className = "text-next-to-input", 
                                children = ["X Variable:"]
                            ),
                            dcc.Dropdown(
                                className = "tab6-sec3-dropdown",
                                id = "tab6-sec3-var-x-dropdown", 
                                options = [
                                    {'label': i, 'value': dropdown_names[i]} for i in dropdown_names
                                ], 
                                value = 'DBT'
                            ),
                        ]
                    ),
                    html.Div(
                        className = "container-row row-center full-width",
                        children = [
                            html.H6(
                                className = "text-next-to-input", 
                                children = ["Y Variable:"]
                            ),
                            dcc.Dropdown(
                                className = "tab6-sec3-dropdown",
                                id = "tab6-sec3-var-y-dropdown", 
                                options = [
                                    {'label': i, 'value': dropdown_names[i]} for i in dropdown_names
                                ], 
                                value = 'RH'
                            ),
                        ]
                    ),
                    html.Div(
                        className = "container-row row-center full-width",
                        children = [
                            html.H6(
                                className = "text-next-to-input", 
                                children = ["Color By:"]
                            ),
                            dcc.Dropdown(
                                className = "tab6-sec3-dropdown",
                                id = "tab6-sec3-colorby-dropdown", 
                                options = [
                                    {'label': i, 'value': dropdown_names[i]} for i in dropdown_names
                                ], 
                                value = 'GHrad'
                            ),
                        ]
                    ),
                ]
            ),
            html.Div(
                className = "container-col container-center one-of-three-container",
                children = [
                    dbc.Checklist(
                        options = [
                            {"label": "Apply Time Filters", "value": "time"},
                        ],
                        value = [],
                        id = "tab6-sec3-time-filter-input",
                    ),
                    html.Div(
                        className = 'container-row full-width container-center',
                        children = [
                            html.H6("Month Range"),
                            dcc.RangeSlider(
                                id = "tab6-sec3-query-month-slider",
                                min = 1,
                                max = 12,
                                step = 1,
                                value = [1, 12], 
                                marks = {
                                    1: '1',
                                    12: '12'
                                },
                                tooltip = {
                                    'always_visible': False,
                                    'placement' : 'top'
                                },
                                allowCross = True
                            ),
                        ]
                    ),
                    html.Div(
                        className = 'container-row full-width container-center',
                        children = [
                            html.H6("Hour Range"),
                            dcc.RangeSlider(
                                id = "tab6-sec3-query-hour-slider",
                                min = 1,
                                max = 24,
                                step = 1,
                                value = [1, 24],
                                marks = {
                                    1: '1',
                                    24: '24'
                                },
                                tooltip = {
                                    'always_visible': False,
                                    'placement' : 'top'
                                },
                                allowCross = True
                            )
                        ]
                    ),
                ]
            ),
            html.Div(
                className = "container-col container-center one-of-three-container",
                children = [
                    dbc.Checklist(
                        options = [
                            {"label": "Apply Data Filters", "value": "data"},
                        ],
                        value = [],
                        id = "tab6-sec3-data-filter-input",
                    ),
                    html.Div(
                        className = "container-row row-center full-width",
                        children = [
                            html.H6(
                                className = "text-next-to-input", 
                                children = ["Filter Variable:"]
                            ),
                            dcc.Dropdown(
                                className = "tab6-sec3-dropdown",
                                id = "tab6-sec3-filter-var-dropdown", 
                                options = [
                                    {'label': i, 'value': dropdown_names[i]} for i in dropdown_names
                                ], 
                                value = 'RH'
                            ),
                        ]
                    ),
                    html.Div(
                        className = "container-row row-center full-width",
                        children = [
                            html.H6(
                                className = "text-next-to-input",
                                children = ["Min Value:"]
                            ),
                            dbc.Input(
                                className = "num-input",
                                id = "tab6-sec3-min-val",
                                placeholder = "Enter a number for the min val",
                                type = "number", 
                                min = 0, 
                                step = 1
                            ),
                        ]
                    ),
                    html.Div(
                        className = "container-row row-center full-width",
                        children = [
                            html.H6(
                                className = "text-next-to-input",
                                children = ["Max Value:"]
                            ),
                            dbc.Input(
                                className = "num-input",
                                id = "tab6-sec3-max-val",
                                placeholder = "Enter a number for the max val",
                                type = "number", 
                                min = 0, 
                                step = 1
                            ),
                        ]
                    ),
                ]
            )
        ]
    )

def section_three():
    """ Return the two graphs in section three.
    """
    return html.Div(
        className = "container-col full-width",
        children = [
            section_three_inputs(),
            dcc.Loading(
                type = "circle",
                children = [
                    dcc.Graph(
                        id = 'three-var',
                        config = config
                    ),
                ]
            ),
            dcc.Loading(
                type = "circle",
                children = [
                    dcc.Graph(
                        id = 'two-var',
                        config = config
                    ),
                ]
            ),
        ]
    )

def tab_six():
    """ Return the contents of tab six."
    """
    return html.Div(
        className = 'continer-col container-center',
        children = [
            section_one(),
            section_two(),
            section_three()
        ]
    )
