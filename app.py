import dash_bootstrap_components as dbc
from dash_extensions.enrich import DashProxy, ServersideOutputTransform
from flask_caching import Cache

app = DashProxy(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    transforms=[ServersideOutputTransform()],
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

app.index_string = """<!DOCTYPE html>
<html lang="en-US">
<head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JDQTBEPS4B"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
    
      gtag('config', 'G-JDQTBEPS4B');
    </script>
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-WTDGD6Q');</script>
    <!-- End Google Tag Manager -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="co-authored by Giovanni Betti, Federico Tartarini, Christine Nguyen, Yunzhu Ji">
    <meta name="keywords" content="Climate analysis, EPW, Weather files, Data visualization, Building design">
    <meta name="description" content="The CBE Clima Tool is a web-based application built to support climate analysis specifically designed to support the need of architects and engineers interested in climate-adapted design. It allows users to analyze the climate data of more than 27,500 locations worldwide from both Energy Plus and Climate.One.Building.org. You can, however, also choose to upload your own EPW weather file. Our tool can be used to analyze and visualize data contained in EnergyPlus Weather (EPW) files. It furthermore calculates a number of climate-related values (i.e. solar azimuth and altitude, Universal Thermal Climate Index (UTCI), comfort indices, etc.) that are not contained in the EPW files but can be derived from the information therein contained. It can be freely accessed at clima.cbe.berkeley.edu">
    <title>CBE Clima Tool</title>
    <meta property="og:image" content="https://github.com/CenterForTheBuiltEnvironment/clima/tree/main/assets/og-image.png">
    <meta property="og:description" content="The CBE Clima Tool is a web-based application built to support climate analysis specifically designed to support the need of architects and engineers interested in climate-adapted design.">
    <meta property="og:title" content="CBE Clima Tool">
    {%favicon%}
    {%css%}
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WTDGD6Q"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
"""
