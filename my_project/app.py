import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from .extract_df import create_df
from .tab_one import tab_one
from .tab_two import tab_two
from .tab_three import tab_three
from .tab_four import tab_four_graphs
from .layout import build_banner, build_tabs, build_footer
from .server import app 

app.title = "EPW Viz"
app.layout = html.Div(
    id = 'big-container',
    children = [
        build_banner(),
        build_tabs(), 
    ]
)