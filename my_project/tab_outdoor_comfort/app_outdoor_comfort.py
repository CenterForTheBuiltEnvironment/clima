from dash import dcc
from dash import html
from my_project.global_scheme import outdoor_dropdown_names
from dash.dependencies import Input, Output, State
from my_project.template_graphs import heatmap
from my_project.utils import title_with_tooltip, generate_chart_name

from app import app, cache, TIMEOUT


def layout_outdoor_comfort():
    return html.Div(
        className="container-col",
        children=[
            html.Div(
                className="container-row align-center justify-center",
                children=[
                    html.H3(
                        children=["Select a scenario: "],
                    ),
                    dcc.Dropdown(
                        id="tab7-dropdown",
                        style={
                            "width": "25rem",
                            "marginLeft": "1rem",
                            "marginRight": "2rem",
                        },
                        options=[
                            {"label": i, "value": outdoor_dropdown_names[i]}
                            for i in outdoor_dropdown_names
                        ],
                        value="utci_Sun_Wind",
                    ),
                    html.Div(id="image-selection"),
                ],
            ),
            html.Div(
                children=title_with_tooltip(
                    text="UTCI heatmap charts",
                    tooltip_text=None,
                    id_button="utci-charts-label",
                ),
            ),
            dcc.Loading(
                html.Div(id="utci-heatmap"),
                type="circle",
            ),
            dcc.Loading(
                html.Div(id="utci-category-heatmap"),
                type="circle",
            ),
        ],
    )


@app.callback(
    Output("utci-heatmap", "children"),
    [
        Input("tab7-dropdown", "value"),
        Input("global-local-radio-input", "value"),
    ],
    [State("df-store", "data"), State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_utci_value(var, global_local, df, meta):

    return dcc.Graph(
        config=generate_chart_name("utci_heatmap", meta),
        figure=heatmap(df, var, global_local),
    )


@app.callback(
    Output("image-selection", "children"),
    Input("tab7-dropdown", "value"),
)
def change_image_based_on_selection(value):
    if value == "utci_Sun_Wind":
        source = "./assets/img/sun_and_wind.png"
    elif value == "utci_Sun_noWind":
        source = "./assets/img/sun_no_wind.png"
    elif value == "utci_noSun_Wind":
        source = "./assets/img/no_sun_and_wind.png"
    else:
        source = "./assets/img/no_sun_no_wind.png"

    return html.Img(src=source, height=50)


@app.callback(
    Output("utci-category-heatmap", "children"),
    [
        Input("tab7-dropdown", "value"),
    ],
    [State("df-store", "data"), State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_tab_utci_category(var, df, meta):

    utci_stress_cat = heatmap(df, var + "_categories")
    utci_stress_cat["data"][0]["colorbar"] = dict(
        title="Thermal stress",
        titleside="top",
        tickmode="array",
        tickvals=[4, 3, 2, 1, 0, -1, -2, -3, -4, -5],
        ticktext=[
            "extreme heat stress",
            "very strong heat stress",
            "strong heat stress",
            "moderate heat stress",
            "no thermal stress",
            "slight cold stress",
            "moderate cold stress",
            "strong cold stress",
            "very strong cold stress",
            "extreme cold stress",
        ],
        ticks="outside",
    )
    return dcc.Graph(
        config=generate_chart_name("utci_heatmap_category", meta),
        figure=utci_stress_cat,
    )
