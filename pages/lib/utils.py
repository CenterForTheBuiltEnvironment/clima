import copy
import functools
import time
import math

import pandas as pd
from dash import html, dash_table, dcc
import dash_mantine_components as dmc

from config import UnitSystem
from pages.lib.global_scheme import fig_config, month_lst
from pages.lib.global_variables import Variables, VariableInfo


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


def generate_chart_name(tab_name, meta=None, custom_inputs=None, units=None):
    figure_config = copy.deepcopy(fig_config)
    custom_str = ""
    if custom_inputs:
        custom_str += f"_{custom_inputs}"
    if units:
        custom_str += f"_{units}"
    if meta:
        file_name = f"{meta[Variables.CITY.col_name]}_{meta[Variables.COUNTRY.col_name]}_{tab_name}{custom_str}"
        figure_config[Variables.TO_IMAGE_BUTTON_OPTIONS.col_name][
            Variables.FILE_NAME.col_name
        ] = file_name
    else:
        figure_config[Variables.TO_IMAGE_BUTTON_OPTIONS.col_name][
            Variables.FILE_NAME.col_name
        ] = f"{tab_name}{custom_str}"
    return figure_config


def generate_units(si_ip):
    """Generate units for the chart titles."""
    if si_ip == UnitSystem.SI:
        return UnitSystem.SI
    else:
        return UnitSystem.IP


def generate_units_degree(si_ip):
    return "C" if si_ip == UnitSystem.SI else "F" if si_ip == UnitSystem.IP else None


def generate_custom_inputs(var):
    try:
        variable = VariableInfo.from_col_name(var)
        if variable.name:
            return "".join(word.capitalize() for word in variable.name.split(" "))
    except KeyError:
        pass
    return None


def generate_custom_inputs_time(start_month, end_month, start_hour, end_hour):
    month_names = [""] + month_lst
    start_month_abbr = month_names[int(start_month)]
    end_month_abbr = month_names[int(end_month)]
    custom_inputs = (
        f"{start_month_abbr}-{end_month_abbr}_{start_hour:02d}-{end_hour:02d}"
    )
    return custom_inputs


def generate_custom_inputs_nv(
    start_month, end_month, start_hour, end_hour, min_dbt_val, max_dbt_val
):
    month_names = [""] + month_lst
    start_month_abbr = month_names[int(start_month)]
    end_month_abbr = month_names[int(end_month)]
    custom_inputs = f"{min_dbt_val:02d}-{max_dbt_val:02d}_{start_month_abbr}-{end_month_abbr}_{start_hour:02d}-{end_hour:02d}"
    return custom_inputs


def generate_custom_inputs_explorer(
    var, start_month, end_month, start_hour, end_hour, filter_var, min_val, max_val
):
    month_names = [""] + month_lst
    start_month_abbr = month_names[int(start_month)]
    end_month_abbr = month_names[int(end_month)]
    try:
        var_name = VariableInfo.from_col_name(var).get_name()
        var_fullname = (
            "".join(word.capitalize() for word in var_name.split(" "))
            if var_name
            else var
        )
    except KeyError:
        var_fullname = var

    try:
        filter_name = VariableInfo.from_col_name(filter_var).get_name()
        filter_fullname = (
            "".join(word.capitalize() for word in filter_name.split(" "))
            if filter_name
            else filter_var
        )
    except KeyError:
        filter_fullname = filter_var
    custom_inputs = f"{var_fullname}_{start_month_abbr}-{end_month_abbr}_{start_hour:02d}-{end_hour:02d}_{filter_fullname}_{min_val}-{max_val}"
    return custom_inputs


def generate_custom_inputs_psy(
    start_month,
    end_month,
    start_hour,
    end_hour,
    colorby_var,
    data_filter_var,
    min_val,
    max_val,
):
    month_names = [""] + month_lst
    start_month_abbr = month_names[int(start_month)]
    end_month_abbr = month_names[int(end_month)]

    def format_variable_name(var: str) -> str:
        try:
            variable = VariableInfo.from_col_name(var)
            name = variable.get_name()
            return (
                "".join(word.capitalize() for word in name.split(" ")) if name else var
            )
        except KeyError:
            return var

    colorby_fullname = format_variable_name(colorby_var)
    data_filter_fullname = format_variable_name(data_filter_var)

    if colorby_var == "None":
        custom_inputs = f"{start_month_abbr}-{end_month_abbr}_{start_hour:02d}-{end_hour:02d}_{data_filter_fullname}_{min_val}-{max_val}"
    else:
        custom_inputs = f"{colorby_fullname}_{start_month_abbr}-{end_month_abbr}_{start_hour:02d}-{end_hour:02d}_{data_filter_fullname}_{min_val}-{max_val}"
    return custom_inputs


def title_with_tooltip(text, tooltip_text, id_button):
    if tooltip_text:
        return dmc.Group(
            children=[
                dmc.Title(text, order=3),
                dmc.Tooltip(
                    label=tooltip_text,
                    position="right",
                    withArrow=True,
                    children=[
                        dmc.Image(
                            id=id_button,
                            src="/assets/icons/help.png",
                            alt="help",
                            w=16,
                            h=16,
                        )
                    ],
                ),
            ],
        )
    else:
        return dmc.Group(
            children=[
                dmc.Title(text, order=3),
            ],
        )


def title_with_link(
    text,
    tooltip_text="Click to access the official documentation",
    id_button=None,
    doc_link: str = "",
):
    return dmc.Group(
        children=[
            dmc.Title(text, order=3),
            dmc.Tooltip(
                label=tooltip_text,
                position="right",
                withArrow=True,
                children=[
                    html.A(
                        dmc.Image(
                            id=id_button,
                            src="/assets/icons/book.png",
                            alt="book",
                            w=16,
                            h=16,
                        ),
                        href=doc_link,
                        target="_blank",
                    )
                ],
            ),
        ],
    )


def summary_table_tmp_rh_tab(df, value, si_ip):
    df_summary = (
        df.groupby([Variables.MONTH_NAMES.col_name, Variables.MONTH.col_name])[value]
        .describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.99])
        .round(2)
    )
    # Robust reset: when groupby is empty, index level names may be lost (None)
    df_summary = df_summary.reset_index()
    # Ensure we have a single human-readable month column named 'month'
    has_month_num = Variables.MONTH.col_name in df_summary.columns
    has_month_name = Variables.MONTH_NAMES.col_name in df_summary.columns
    if has_month_num:
        df_summary = df_summary.sort_values(by=Variables.MONTH.col_name)
    if has_month_name and has_month_num:
        # Keep readable names as 'month', drop numeric to avoid duplicate columns
        df_summary = df_summary.rename(
            columns={Variables.MONTH_NAMES.col_name: Variables.MONTH.col_name}
        )
        # After rename there will be two 'month' columns; drop the numeric one by position
        # Keep the leftmost 'month' (the renamed names column)
        cols = []
        seen = set()
        for c in df_summary.columns:
            if c == Variables.MONTH.col_name:
                if c in seen:
                    continue
                seen.add(c)
                cols.append(c)
            else:
                cols.append(c)
        df_summary = df_summary.loc[:, cols]
        # Explicitly drop the numeric month column if still present as a duplicate
        if df_summary.columns.duplicated().any():
            df_summary = df_summary.loc[:, ~df_summary.columns.duplicated()]
    elif has_month_name and not has_month_num:
        df_summary = df_summary.rename(
            columns={Variables.MONTH_NAMES.col_name: Variables.MONTH.col_name}
        )
    # Drop 'count' if present
    if "count" in df_summary.columns:
        df_summary = df_summary.drop(["count"], axis=1)
    # Guarantee unique columns
    if df_summary.columns.duplicated().any():
        df_summary = df_summary.loc[:, ~df_summary.columns.duplicated()]

    df_sum = (
        df[value]
        .describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.99])
        .round(2)
        .to_frame()
    )
    df_sum = df_sum.T.assign(count="Year").rename(
        columns={"count": Variables.MONTH.col_name}
    )

    df_summary = pd.concat([df_summary, df_sum], ignore_index=True)

    unit = (
        VariableInfo.from_col_name(value)
        .get_unit(si_ip)
        .replace("<sup>", "")
        .replace("</sup>", "")
    )
    return dash_table.DataTable(
        columns=[
            (
                {"name": i, "id": i}
                if i == Variables.MONTH.col_name
                else {"name": f"{i} ({unit})", "id": i}
            )
            for i in df_summary.columns
        ],
        style_table={"overflowX": "auto"},
        data=df_summary.to_dict("records"),
        style_cell={"textAlign": "center", "padding": "5px 10px"},
        style_cell_conditional=[{"if": {"column_id": "month"}, "textAlign": "right"}],
        style_header={"backgroundColor": "rgb(220, 220, 220)", "fontWeight": "bold"},
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "white"},
            {"if": {"row_index": "even"}, "backgroundColor": "rgb(250, 250, 250)"},
            {"if": {"row_index": [12]}, "backgroundColor": "rgb(220, 220, 220)"},
        ],
        style_as_list_view=True,
    )


def determine_month_and_hour_filter(month, hour, invert_month, invert_hour):
    start_month, end_month = month
    if invert_month and (start_month != 1 or end_month != 12):
        end_month, start_month = month
    start_hour, end_hour = hour
    if invert_hour and (start_hour != 0 or end_hour != 24):
        end_hour, start_hour = hour

    return start_month, end_month, start_hour, end_hour


def dropdown(options=None, **kwargs):
    """
    Wrapper for dcc.Dropdown which
    - makes "clearable=False" the default, so we don't need to handle None
    - accepts dicts, and preserves order.
    """
    if options is None:
        options = {}
    return dcc.Dropdown(
        options=[{"label": k, "value": v} for k, v in options.items()],
        clearable=False,
        style={"width": "14rem"},
        **kwargs,
    )


def get_max_min_value(series: pd.Series, base: int = 5) -> tuple[int, int]:
    """Calculate rounded-up max and rounded-down min values based on a base step.

    Args:
        series: Pandas Series of numeric values.
        base: The rounding base. Default is 5.

    Returns:
        Tuple of (max_value, min_value) adjusted to nearest base step.
    """
    # Guard against all-NaN series after filtering
    non_na = series.dropna()
    if non_na.empty:
        # Fallback to a symmetric small range to avoid rendering errors
        return base, -base

    data_max = base * math.ceil(non_na.max() / base)
    data_min = base * math.floor(non_na.min() / base)
    return data_max, data_min


def get_default_global_filter_store_data() -> dict:
    """Return default data structure for TOOLS_GLOBAL_FILTER_STORE.

    Centralizes the default so it can be reused across pages without duplication.
    """
    return {
        "month_range": [1, 12],
        "hour_range": [0, 24],
        "invert_month": [],
        "invert_hour": [],
        "filter_active": False,
    }


def get_global_filter_state(filter_store_data: dict | None) -> dict:
    """Normalize filter store data into a consistent, easy-to-use structure.

    Ensures defaults are applied and types are coerced to booleans where appropriate.
    """
    default_data = get_default_global_filter_store_data()
    data = (
        default_data if not filter_store_data else {**default_data, **filter_store_data}
    )

    return {
        "filter_active": bool(data.get("filter_active", False)),
        "month_range": data.get("month_range", [1, 12]),
        "hour_range": data.get("hour_range", [0, 24]),
        # invert flags may be stored as []/['invert'] or booleans; coerce to bool
        "invert_month": bool(data.get("invert_month", [])),
        "invert_hour": bool(data.get("invert_hour", [])),
    }


def get_time_filter_from_store(
    filter_store_data: dict | None,
) -> tuple[bool, list[int], list[int], bool, bool]:
    """Return normalized time filter arguments from the global filter store.

    Returns (time_filter, month, hour, invert_month, invert_hour).
    """
    state = get_global_filter_state(filter_store_data)
    return (
        True,
        state["month_range"],
        state["hour_range"],
        state["invert_month"],
        state["invert_hour"],
    )


def separate_filtered_data(df, var=None):
    # Check if there's a filter marker
    has_filter_marker = "_is_filtered" in df.columns
    filtered_mask = None
    if has_filter_marker:
        filtered_mask = df["_is_filtered"]

    # Get original values if available
    original_var_col = None
    use_original_for_filtered = False
    if var is not None:
        original_var_col = f"_{var}_original"
        use_original_for_filtered = has_filter_marker and original_var_col in df.columns

    # Separate filtered and unfiltered data
    if has_filter_marker and filtered_mask is not None:
        df_unfiltered = df[~filtered_mask].copy()
        df_filtered = df[filtered_mask].copy() if filtered_mask.any() else None
    else:
        df_unfiltered = df
        df_filtered = None

    return {
        "has_filter_marker": has_filter_marker,
        "filtered_mask": filtered_mask,
        "df_unfiltered": df_unfiltered,
        "df_filtered": df_filtered,
        "original_var_col": original_var_col,
        "use_original_for_filtered": use_original_for_filtered,
    }


def has_filtered_data(df_filtered):
    return df_filtered is not None and len(df_filtered) > 0


def get_variable_info(var, si_ip):
    variable = VariableInfo.from_col_name(var)
    return {
        "var_unit": variable.get_unit(si_ip),
        "var_range": variable.get_range(si_ip),
        "var_name": variable.get_name(),
        "var_color": variable.get_color(),
    }


def unpack_variable_info(var_info, keys=None):
    if keys is None:
        keys = ["var_unit", "var_range", "var_name", "var_color"]
    return tuple(var_info[key] for key in keys)


def get_variable_range(
    var, df, global_local, si_ip, use_original_for_range=False, original_values=None
):
    var_info = get_variable_info(var, si_ip)
    var_range = var_info["var_range"]

    if global_local == "global":
        return var_range
    else:
        if use_original_for_range and original_values is not None:
            data_max, data_min = get_max_min_value(original_values)
        else:
            data_max, data_min = get_max_min_value(df[var])
        return [data_min, data_max]


def get_original_column_values(df, var):
    original_col = f"_{var}_original"
    if original_col in df.columns:
        return df[original_col].copy()
    else:
        return df[var].copy()


def calculate_daily_statistics(df, var_col, date_col=Variables.UTC_TIME.col_name):
    if len(df) == 0:
        return pd.DataFrame({"min": [], "max": [], "mean": []})

    df_with_date = df.copy()
    df_with_date["_date"] = df_with_date[date_col].dt.date
    return df_with_date.groupby("_date")[var_col].agg(["min", "max", "mean"])
