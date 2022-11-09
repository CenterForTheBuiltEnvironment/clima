import numpy as np
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from my_project.global_scheme import (
    sun_cloud_tab_dropdown_names,
    sun_cloud_tab_explore_dropdown_names,
    tight_margins,
    month_lst,
)
from dash.dependencies import Input, Output, State

from my_project.tab_sun.charts_sun import (
    monthly_solar,
    polar_graph,
    custom_cartesian_solar,
)
from my_project.template_graphs import heatmap, barchart, daily_profile
from my_project.utils import code_timer
from my_project.utils import title_with_tooltip, generate_chart_name

from app import app


def sun_path():
    """Return the layout for the custom sun path and its dropdowns."""
    return html.Div(
        className="container-col justify-center",
        children=[
            html.Div(
                children=title_with_tooltip(
                    text="Sun path chart",
                    tooltip_text=None,
                    id_button="sun-path-chart-label",
                ),
            ),
            dbc.Row(
                align="center",
                justify="center",
                children=[
                    html.H6(
                        className="text-next-to-input",
                        children=["View: "],
                        style={"width": "10rem"},
                    ),
                    dcc.Dropdown(
                        id="custom-sun-view-dropdown",
                        options=[
                            {"label": "Spherical", "value": "polar"},
                            {"label": "Cartesian", "value": "cartesian"},
                        ],
                        value="polar",
                        style={"width": "10rem"},
                    ),
                ],
            ),
            dbc.Row(
                align="center",
                justify="center",
                children=[
                    html.H6(
                        className="text-next-to-input",
                        children=["Variable: "],
                        style={"width": "10rem"},
                    ),
                    dcc.Dropdown(
                        id="custom-sun-var-dropdown",
                        options=[
                            {"label": i, "value": sun_cloud_tab_dropdown_names[i]}
                            for i in sun_cloud_tab_dropdown_names
                        ],
                        value="None",
                        style={"width": "20rem"},
                    ),
                ],
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(
                    id="custom-sunpath",
                ),
            ),
        ],
    )


def explore_daily_heatmap():
    """Contents of the bottom part of the tab"""
    return html.Div(
        className="container-col full-width",
        children=[
            html.Div(
                children=title_with_tooltip(
                    text="Daily charts",
                    tooltip_text=None,
                    id_button="daily-chart-label",
                ),
            ),
            html.Div(
                className="container-row justify-center align-center mb-2",
                children=[
                    html.H6(
                        className="text-next-to-input",
                        children=["Select variable: "],
                        style={"width": "10rem"},
                    ),
                    dcc.Dropdown(
                        id="tab4-explore-dropdown",
                        options=[
                            {
                                "label": i,
                                "value": sun_cloud_tab_explore_dropdown_names[i],
                            }
                            for i in sun_cloud_tab_explore_dropdown_names
                        ],
                        value="glob_hor_rad",
                        style={"width": "20rem"},
                    ),
                ],
            ),
            dcc.Loading(type="circle", children=html.Div(id="tab4-daily")),
            dcc.Loading(
                type="circle",
                children=html.Div(id="tab4-heatmap"),
            ),
        ],
    )


def static_section():
    return html.Div(
        className="container-col full-width",
        children=[
            html.Div(
                children=title_with_tooltip(
                    text="Global and Diffuse Horizontal Solar Radiation (Wh/m²)",
                    tooltip_text=None,
                    id_button="monthly-chart-label",
                ),
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(id="monthly-solar"),
            ),
            html.Div(
                children=title_with_tooltip(
                    text="Cloud coverage",
                    tooltip_text=None,
                    id_button="cloud-chart-label",
                ),
            ),
            dcc.Loading(
                type="circle",
                children=html.Div(id="cloud-cover"),
            ),
        ],
    )


def layout_sun():
    """Contents of tab four."""
    return html.Div(
        className="container-col",
        id="tab-four-container",
        children=[sun_path(), static_section(), explore_daily_heatmap()],
    )


@app.callback(
    [
        Output("monthly-solar", "children"),
        Output("cloud-cover", "children"),
    ],
    [
        Input("df-store", "modified_timestamp"),
    ],
    [State("df-store", "data"), State("meta-store", "data")],
)
@code_timer
def monthly_and_cloud_chart(ts, df, meta):
    """Update the contents of tab four. Passing in the polar selection and the general info (df, meta)."""

    # Sun Radiation
    monthly = monthly_solar(df)
    monthly = monthly.update_layout(margin=tight_margins)

    # Cloud Cover
    cover = barchart(df, "tot_sky_cover", [False], [False, "", 3, 7], True)
    cover = cover.update_layout(
        margin=tight_margins,
        title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
    )
    cover.update_xaxes(
        dict(tickmode="array", tickvals=np.arange(0, 12, 1), ticktext=month_lst)
    )

    return dcc.Graph(
        config=generate_chart_name("monthly_sun", meta),
        figure=monthly,
    ), dcc.Graph(
        config=generate_chart_name("cloud_cover_sun", meta),
        figure=cover,
    )


@app.callback(
    Output("custom-sunpath", "children"),
    [
        Input("custom-sun-view-dropdown", "value"),
        Input("custom-sun-var-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [State("df-store", "data"), State("meta-store", "data")],
)
@code_timer
def sun_path_chart(view, var, global_local, df, meta):
    """Update the contents of tab four. Passing in the polar selection and the general info (df, meta)."""

    if view == "polar":
        return dcc.Graph(
            config=generate_chart_name("spherical_sun_path_sun", meta),
            figure=polar_graph(df, meta, global_local, var),
        )
    else:
        return dcc.Graph(
            config=generate_chart_name("cartesian_sun_path_sun", meta),
            figure=custom_cartesian_solar(df, meta, global_local, var),
        )


@app.callback(
    Output("tab4-daily", "children"),
    [
        Input("tab4-explore-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [State("df-store", "data"), State("meta-store", "data")],
)
@code_timer
def daily(var, global_local, df, meta):
    """Update the contents of tab four section two. Passing in the general info (df, meta)."""

    return dcc.Graph(
        config=generate_chart_name("daily_sun", meta),
        figure=daily_profile(df, var, global_local),
    )


@app.callback(
    Output("tab4-heatmap", "children"),
    [
        Input("tab4-explore-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [State("df-store", "data"), State("meta-store", "data")],
)
@code_timer
def update_heatmap(var, global_local, df, meta):

    return dcc.Graph(
        config=generate_chart_name("heatmap_sun", meta),
        figure=heatmap(df, var, global_local),
    )
