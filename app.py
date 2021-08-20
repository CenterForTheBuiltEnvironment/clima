import dash_bootstrap_components as dbc
from dash import Dash
from flask_caching import Cache
import warnings

# todo remove ignore warnings
warnings.filterwarnings("ignore")

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

app.index_string = """<!DOCTYPE html>
<html>
<head>
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-JDQTBEPS4B"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-JDQTBEPS4B');
</script>
{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
</head>
<body>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
"""
