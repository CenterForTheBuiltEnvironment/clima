import dash_bootstrap_components as dbc
from dash import Dash
from flask_caching import Cache
import warnings

# todo remove ignore warnings
# warnings.filterwarnings("ignore")

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
cache = Cache(
    app.server,
    config={
        "CACHE_TYPE": "flask_caching.backends.SimpleCache",
        "CACHE_DIR": "cache-directory",
    },
)
TIMEOUT = 600
app.config.suppress_callback_exceptions = True
