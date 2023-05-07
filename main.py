import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash
import os

from my_project.layout import banner, build_tabs, footer
from my_project.tab_wind.app_wind import layout_wind
from my_project.tab_sun.app_sun import layout_sun
from my_project.tab_select.app_select import layout_select
from my_project.tab_data_explorer.app_data_explorer import layout_data_explorer
from my_project.tab_outdoor_comfort.app_outdoor_comfort import layout_outdoor_comfort
from my_project.tab_t_rh.app_t_rh import layout_t_rh
from my_project.tab_psy_chart.app_psy_chart import layout_psy_chart
from my_project.tab_natural_ventilation.app_natural_ventilation import (
    layout_natural_ventilation,
)
from my_project.tab_summary.app_summary import layout_summary
from my_project.page_changelog.app_changelog import changelog

from app import app

server = app.server

app.title = "CBE Clima Tool"
app.layout = dbc.Container(
    fluid=True,
    style={"padding": "0"},
    children=[
        dcc.Location(id="url", refresh=False),
        banner(),
        html.Div(id="page-content"),
        footer(),
    ],
)


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/":
        return build_tabs()
    elif pathname == "/changelog":
        return html.Div(children=[changelog()])


# Handle tab selection
@app.callback(
    Output("tabs-content", "children"),
    [
        Input("tabs", "value"),
        Input("si-ip-radio-input", "value"),
        State("month-range-filter-store", "data"),
        State("hour-range-filter-store", "data"),
        State("month-invert-filter-store", "data"),
        State("hour-invert-filter-store", "data"),
    ],
)
def render_content(tab, si_ip, month_range_filter_store, hour_range_filter_store, month_invert_filter_store, hour_invert_filter_store):
    """Update the contents of the page depending on what tab the user selects."""
    if tab == "tab-select":
        return layout_select()
    elif tab == "tab-summary":
        return layout_summary(si_ip)
    elif tab == "tab-t-rh":
        return layout_t_rh()
    elif tab == "tab-sun":
        return layout_sun(si_ip)
    elif tab == "tab-wind":
        return layout_wind()
    elif tab == "tab-data-explorer":
        return layout_data_explorer()
    elif tab == "tab-outdoor-comfort":
        return layout_outdoor_comfort(month_range_filter_store, hour_range_filter_store, month_invert_filter_store, hour_invert_filter_store)
    elif tab == "tab-natural-ventilation":
        return layout_natural_ventilation(si_ip, month_range_filter_store, hour_range_filter_store, month_invert_filter_store, hour_invert_filter_store)
    elif tab == "tab-psy-chart":
        return layout_psy_chart(month_range_filter_store, hour_range_filter_store, month_invert_filter_store, hour_invert_filter_store)
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=8080,
        processes=1,
        threaded=True,
    )
