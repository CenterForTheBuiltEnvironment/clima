import dash_html_components as html
from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc

from my_project.layout import build_banner, build_tabs, footer
from my_project.tab_under_construction.construction import construction
from my_project.tab_wind.app_wind import layout_wind
from my_project.tab_sun.app_sun import layout_sun
from my_project.tab_select.app_select import layout_select
from my_project.tab_data_explorer.app_data_explorer import layout_data_explorer
from my_project.tab_outdoor_comfort.app_outdoor_comfort import layout_outdoor_comfort
from my_project.tab_t_rh.app_t_rh import layout_t_rh
from my_project.tab_psy_chart.app_psy_chart import layout_psy_chart
from my_project.tab_summary.app_summary import layout_summary
from my_project.page_changelog.app_changelog import changelog

from app import app, cache, TIMEOUT

server = app.server

app.title = "CBE Clima Tool"
app.layout = html.Div(
    id="big-container",
    children=[
        dcc.Location(id="url", refresh=False),
        # content will be rendered in this element
        build_banner(),
        html.Div(id="page-content"),
        # fixme the footer should be imported here, it should always tbe there as the banner
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
        return html.Div(children=[changelog(), footer()])


# Handle tab selection
@app.callback(Output("tabs-content", "children"), [Input("tabs", "value")])
@cache.memoize(timeout=TIMEOUT)
def render_content(tab):
    """Update the contents of the page depending on what tab the user selects."""
    if tab == "tab-select":
        return layout_select()
    elif tab == "tab-summary":
        return layout_summary()
    elif tab == "tab-t-rh":
        return layout_t_rh()
    elif tab == "tab-sun":
        return layout_sun()
    elif tab == "tab-wind":
        return layout_wind()
    elif tab == "tab-data-explorer":
        return layout_data_explorer()
    elif tab == "tab-outdoor_comfort":
        return layout_outdoor_comfort()
    elif tab == "tab-natural-ventilation":
        return construction()
    elif tab == "tab-psy-chart":
        return layout_psy_chart()
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8080, processes=1, threaded=True)
