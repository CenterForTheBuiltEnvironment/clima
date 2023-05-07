from dash import ctx
from dash.dependencies import Input, Output, State
from app import app

triggersAndCorresponding = {
    "month-hour-filter": {
        "month-range": "psy-month-slider",
        "month-invert": "invert-month-psy",
        "hour-range": "psy-hour-slider",
        "hour-invert": "invert-hour-psy"
    },
    "nv-month-hour-filter": {
        "month-range": "nv-month-slider",
        "month-invert": "invert-month-nv",
        "hour-range": "nv-hour-slider",
        "hour-invert": "invert-hour-nv"
    },
    "month-hour-filter-outdoor-comfort": {
        "month-range": "outdoor-comfort-month-slider",
        "month-invert": "invert-month-outdoor-comfort",
        "hour-range": "outdoor-comfort-hour-slider",
        "hour-invert": "invert-hour-outdoor-comfort"
    },
    "sec1-time-filter-input": {
        "month-range": "sec1-month-slider",
        "month-invert": "",
        "hour-range": "sec1-hour-slider",
        "hour-invert": ""
    },
    "sec2-time-filter-input": {
        "month-range": "sec2-month-slider",
        "month-invert": "invert-month-explore-heatmap",
        "hour-range": "sec2-hour-slider",
        "hour-invert": "invert-hour-explore-heatmap"
    },
    "tab6-sec3-time-filter-input": {
        "month-range": "tab6-sec3-query-month-slider",
        "month-invert": "invert-month-explore-more-charts",
        "hour-range": "tab6-sec3-query-hour-slider",
        "hour-invert": "invert-hour-explore-more-charts"
    },
}


@app.callback(
    Output("month-range-filter-store", "data"),
    [
        State("month-range-filter-store", "data"),
        *[State(triggersAndCorresponding[trigger]["month-range"], "value") for trigger in triggersAndCorresponding.keys()]
    ],
    [
        Input(triggerKey, "n_clicks") for triggerKey in triggersAndCorresponding.keys()
    ]
)
def update_month_range_filter_store(global_data_store, *args):
    trigger = ctx.triggered_id
    if trigger is not None and trigger != 0:
        return {"data": triggersAndCorresponding[trigger]["month-range"]}
    return global_data_store


@app.callback(
    Output("hour-range-filter-store", "data"),
    [
        State("hour-range-filter-store", "data"),
        *[State(triggersAndCorresponding[trigger]["hour-range"], "value") for trigger in triggersAndCorresponding.keys()]
    ],
    [
        Input(triggerKey, "n_clicks") for triggerKey in triggersAndCorresponding.keys()
    ]
)
def update_hour_range_filter_store(global_data_store, *args):
    trigger = ctx.triggered_id
    if trigger is not None and trigger != 0:
        return {"data": triggersAndCorresponding[trigger]["hour-range"]}
    return global_data_store


@app.callback(
    Output("month-invert-filter-store", "data"),
    [
        State("month-invert-filter-store", "data"),
        *[State(triggersAndCorresponding[trigger]["month-invert"], "value") for trigger in triggersAndCorresponding.keys()]
    ],
    [
        Input(triggerKey, "n_clicks") for triggerKey in triggersAndCorresponding.keys()
    ]
)
def update_month_invert_filter_store(global_data_store, *args):
    trigger = ctx.triggered_id
    if trigger is not None and trigger != 0:
        return {"data": triggersAndCorresponding[trigger]["month-invert"]}
    return global_data_store


@app.callback(
    Output("hour-invert-filter-store", "data"),
    [
        State("hour-invert-filter-store", "data"),
        *[State(triggersAndCorresponding[trigger]["hour-invert"], "value") for trigger in triggersAndCorresponding.keys()]
    ],
    [
        Input(triggerKey, "n_clicks") for triggerKey in triggersAndCorresponding.keys()
    ]
)
def update_hour_invert_filter_store(global_data_store, *args):
    trigger = ctx.triggered_id
    if trigger is not None and trigger != 0:
        return {"data": triggersAndCorresponding[trigger]["hour-invert"]}
    return global_data_store
