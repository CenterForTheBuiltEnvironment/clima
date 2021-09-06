import functools
import time
from my_project.global_scheme import fig_config
import pandas as pd
import json
from pandas import json_normalize
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import copy


def code_timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


def generate_chart_name(tab_name, meta=None):
    figure_config = copy.deepcopy(fig_config)
    if meta:
        figure_config["toImageButtonOptions"][
            "filename"
        ] = f"CBEClima_{meta['city']}_{meta['country']}_{tab_name}_tab"
    else:
        figure_config["toImageButtonOptions"]["filename"] = f"CBEClima_{tab_name}_tab"
    return figure_config


def plot_location_epw_files():
    with open("./assets/data/epw_location.json") as data_file:
        data = json.load(data_file)

    df = json_normalize(data["features"])
    df[["lon", "lat"]] = pd.DataFrame(df["geometry.coordinates"].tolist())
    df["lat"] += 0.005
    df["lat"] += 0.005

    df_one_building = pd.read_csv("./assets/data/one_building.csv")

    fig2 = px.scatter_mapbox(
        df.head(2585),
        lat="lat",
        lon="lon",
        hover_name="properties.title",
        color_discrete_sequence=["#3a0ca3"],
        hover_data=["properties.epw"],
        zoom=2,
        height=500,
    )
    fig = px.scatter_mapbox(
        df_one_building,
        lat="lat",
        lon="lon",
        hover_name="name",
        color_discrete_sequence=["#4895ef"],
        hover_data=["Source"],
        zoom=2,
        height=500,
    )
    fig.add_trace(fig2.data[0])
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


def title_with_tooltip(text, tooltip_text, id_button):

    display_tooltip = "none"
    if tooltip_text:
        display_tooltip = "block"

    return html.Div(
        className="container-row",
        style={"padding": "1rem", "marginTop": "1rem"},
        children=[
            html.H5(text, style={"marginRight": "0.5rem"}),
            html.Div(
                [
                    html.Sup(
                        html.Img(
                            id=id_button,
                            src="../assets/icons/help.png",
                            alt="help",
                            style={
                                "width": "1rem",
                                "height": "1rem",
                            },
                        ),
                    ),
                    dbc.Tooltip(
                        tooltip_text,
                        target=id_button,
                        placement="right",
                    ),
                ],
                style={"display": display_tooltip},
            ),
        ],
    )


def summary_table_tmp_rh_tab(df, var_selected):
    var = "RH"
    if var_selected == "dd_tdb":
        var = "DBT"
    df_summary = (
        df.groupby(["month_names", "month"])[var]
        .describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.99])
        .round(2)
    )
    df_summary = df_summary.reset_index(level="month_names").sort_index()
    df_summary = df_summary.drop(["count"], axis=1)
    df_summary = df_summary.rename(columns={"month_names": "month"})

    df_sum = (
        df[var].describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.99]).round(2).to_frame()
    )
    df_sum = df_sum.T.assign(count="Year").rename(columns={"count": "month"})

    return df_summary.append(df_sum)
