import functools
import time
from my_project.global_scheme import fig_config, name_dict


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


def generate_chart_name(tab_name, meta):
    # todo the file name should contain the image title, the function works but each figure gets the same config
    _fig_config = fig_config.copy()
    _fig_config["toImageButtonOptions"][
        "filename"
    ] = f"CBEClima_{meta[1]}_{meta[3]}_{tab_name}_tab"
    return _fig_config
