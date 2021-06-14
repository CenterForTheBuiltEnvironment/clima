import dash_html_components as html
from dash.dependencies import Input, Output

from my_project.layout import build_banner, build_tabs
from my_project.construction import construction
from my_project.tab_five.app_five import tab_five
from my_project.tab_four.app_four import tab_four
from my_project.tab_one.app_one import tab_one
from my_project.tab_six.app_six import tab_six
from my_project.tab_seven.app_seven import tab_seven
from my_project.tab_three.app_three import tab_three
from my_project.tab_nine.app_nine import tab_nine
from my_project.tab_two.app_two import tab_two

from app import app, cache, TIMEOUT

server = app.server

app.title = "CBE Clima Tool"
app.layout = html.Div(
    id="big-container",
    children=[
        build_banner(),
        build_tabs(),
    ],
)

# Handle tab selection
@app.callback(Output("tabs-content", "children"), [Input("tabs", "value")])
@cache.memoize(timeout=TIMEOUT)
def render_content(tab):
    """Update the contents of the page depending on what tab the user selects."""
    if tab == "tab-1":
        return tab_one()
    elif tab == "tab-2":
        return tab_two()
    elif tab == "tab-3":
        return tab_three()
    elif tab == "tab-4":
        return tab_four()
    elif tab == "tab-5":
        return tab_five()
    elif tab == "tab-6":
        return tab_six()
    elif tab == "tab-7":
        return tab_seven()
    elif tab == "tab-8":
        return construction()
    elif tab == "tab-9":
        return tab_nine()
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080)
