# Colors Dictionary
blue_red_yellow = ["#00b3ff", "#000082", "#ff0000", "#ffff00"]
dry_humid = ["#ffe600", "#00c8ff", "#0000ff"]
sun_colors = [
    "#293a59",
    "#960c2c",
    "#ff0000",
    "#ff7b00",
    "#fffc00",
    "#ffff7b",
    "#ffffff",
]
light_colors = ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"]
bright_colors = ["#730a8c", "#0d0db3", "#0f85be", "#0f85be", "#b11421", "#fdf130"]
wind_speed_color = [
    "#ffffff",
    "#b2f2ff",
    "#33ddff",
    "#00aaff",
    "#0055ff",
    "#0000ff",
    "#aa00ff",
    "#ff00ff",
    "#cc0000",
    "#ffaa00",
]
wind_dir_color = ["#0072dd", "#00c420", "#eded00", "#be00d5", "#0072dd"]
cloud_colors = ["#00aaff", "#ffffff", "#c2c2c2"]
utci_categories_color = [
    # Let first 10% (0.1) of the values have color rgb(0, 0, 0)
    [0, "#2B2977"],
    [0.0555, "#2B2977"],
    [0.0555, "#38429B"],
    [0.0555 + 0.111 * 1, "#38429B"],
    [0.0555 + 0.111 * 1, "#4253A4"],
    [0.0555 + 0.111 * 2, "#4253A4"],
    [0.0555 + 0.111 * 2, "#4B62AD"],
    [0.0555 + 0.111 * 3, "#4B62AD"],
    [0.0555 + 0.111 * 3, "#68B8E7"],
    [0.0555 + 0.111 * 4, "#68B8E7"],
    [0.0555 + 0.111 * 4, "#53B848"],
    [0.0555 + 0.111 * 5, "#53B848"],
    [0.0555 + 0.111 * 5, "#EE8522"],
    [0.0555 + 0.111 * 6, "#EE8522"],
    [0.0555 + 0.111 * 6, "#EA2C24"],
    [0.0555 + 0.111 * 7, "#EA2C24"],
    [0.0555 + 0.111 * 7, "#B12224"],
    [0.0555 + 0.111 * 8, "#B12224"],
    [0.0555 + 0.111 * 8, "#751613"],
    [1.0, "#751613"],
]

# containers
container_row_center_full = "container-row row-center"
container_col_center_one_of_three = (
    "container-col justify-center one-of-three-container"
)

# Misc
month_lst = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

import plotly.io as pio

clima_template = "plotly_white"

pio.templates.default = clima_template
template = clima_template

fig_config = {
    "modeBarButtonsToRemove": [
        "toggleSpikelines",
        "hoverCompareCartesian",
        "select2d",
        "zoom2d",
        "autoScale2d",
        "pan2d",
        "lasso2d",
        "zoomIn2d",
        "zoomOut2d",
        "hoverClosestCartesian",
    ],
    "displaylogo": False,
    "displayModeBar": "hover",
    "toImageButtonOptions": {"format": "svg", "filename": "Clima tool graph"},
}

tight_margins = dict(l=20, r=20, t=33, b=20)

# Units Dictionary
degrees_unit = "\u00B0deg"
temperature_unit = "\u00B0C"
radiation_unit = "Wh/m<sup>2</sup>"
thermal_stress_label = "Thermal stress"

mapping_dictionary = {
    "None": {"name": "None"},
    "DOY": {"name": "Day of the year", "unit": "days", "range": [0, 365]},
    "day": {"name": "day", "range": [1, 31]},
    "month": {"name": "months", "unit": "months", "range": [1, 12]},
    "hour": {
        "name": "hours of the day",
        "color": [
            "#000000",
            "#355e7e",
            "#6b5c7b",
            "#c06c84",
            "#f8b195",
            "#c92a42",
            "#c92a42",
            "#c92a42",
            "#000000",
        ],
        "unit": "h",
        "range": [1, 24],
    },
    "DBT": {
        "name": "Dry bulb temperature",
        "color": ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        "unit": "°C",
        "range": [-40, 50],
    },
    "DPT": {
        "name": "Dew point temperature",
        "color": ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        "unit": "°C",
        "range": [-50, 35],
    },
    "RH": {
        "name": "Relative humidity",
        "color": ["#ffe600", "#00c8ff", "#0000ff"],
        "unit": "%",
        "range": [0, 100],
    },
    "Apressure": {
        "name": "Atmospheric pressure",
        "color": [
            "#ffffff",
            "#b2f2ff",
            "#33ddff",
            "#00aaff",
            "#0055ff",
            "#0000ff",
            "#aa00ff",
            "#ff00ff",
            "#cc0000",
            "#ffaa00",
        ],
        "unit": "Pa",
        "range": [95000, 105000],
    },
    "EHrad": {
        "name": "Extraterrestrial horizontal irradiation",
        "color": [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        "unit": radiation_unit,
        "range": [0, 1200],
    },
    "HIRrad": {
        "name": "´Horizontal infrared radiation",
        "color": [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        "unit": radiation_unit,
        "range": [0, 500],
    },
    "GHrad": {
        "name": "Global horizontal radiation",
        "color": [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        "unit": radiation_unit,
        "range": [0, 1200],
    },
    "DNrad": {
        "name": "Direct normal radiation",
        "color": [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        "unit": radiation_unit,
        "range": [0, 1200],
    },
    "DifHrad": {
        "name": "Diffuse horizontal radiation",
        "color": [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        "unit": radiation_unit,
        "range": [0, 1200],
    },
    "GHillum": {
        "name": "Global horizontal illuminance",
        "color": ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],
        "unit": "lux",
        "range": [0, 120000],
    },
    "DNillum": {
        "name": "Direct normal illuminance",
        "color": ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],
        "unit": "lux",
        "range": [0, 120000],
    },
    "DifHillum": {
        "name": "Diffuse horizontal illuminance",
        "color": ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],
        "unit": "lux",
        "range": [0, 120000],
    },
    "Zlumi": {
        "name": "Zenith luminance",
        "color": ["#730a8c", "#0d0db3", "#0f85be", "#0f85be", "#b11421", "#fdf130"],
        "unit": "cd/m<sup>2</sup>",
        "range": [0, 60000],
    },
    "Wdir": {
        "name": "Wind direction",
        "color": ["#0072dd", "#00c420", "#eded00", "#be00d5", "#0072dd"],
        "unit": "°deg",
        "range": [0, 360],
    },
    "Wspeed": {
        "name": "Wind speed",
        "color": [
            "#ffffff",
            "#b2f2ff",
            "#33ddff",
            "#00aaff",
            "#0055ff",
            "#0000ff",
            "#aa00ff",
            "#ff00ff",
            "#cc0000",
            "#ffaa00",
        ],
        "unit": "m/s",
        "range": [0, 20],
    },
    "Tskycover": {
        "name": "Total sky cover",
        "color": ["#00aaff", "#ffffff", "#c2c2c2"],
        "unit": "tenths",
        "range": [0, 10],
    },
    "Oskycover": {
        "name": "Opaque sky cover",
        "color": ["#00aaff", "#ffffff", "#c2c2c2"],
        "unit": "tenths",
        "range": [0, 10],
    },
    "Vis": {
        "name": "Visibility",
        "color": ["#00aaff", "#ffffff", "#c2c2c2"],
        "unit": "Km",
        "range": [0, 100],
    },
    "apparent_zenith": {
        "name": "Apparent zenith",
        "color": [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        "unit": "°deg",
        "range": [0, 180],
    },
    "zenith": {
        "name": "Zenith",
        "color": [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        "unit": "°deg",
        "range": [0, 180],
    },
    "apparent_elevation": {
        "name": "Apparent elevation",
        "color": [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        "unit": "°deg",
        "range": [-90, 90],
    },
    "elevation": {
        "name": "Elevation",
        "color": [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        "unit": "°deg",
        "range": [-90, 90],
    },
    "azimuth": {
        "name": "Azimuth",
        "color": [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        "unit": "°deg",
        "range": [0, 360],
    },
    "equation_of_time": {
        "name": "Equation of time",
        "color": [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        "unit": "°deg",
        "range": [-20, 20],
    },
    "utci_Sun_Wind": {
        "name": "UTCI: Sun & Wind",
        "color": ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        "unit": "°C",
        "range": [-70, 70],
    },
    "utci_noSun_Wind": {
        "name": "UTCI: no Sun & Wind",
        "color": ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        "unit": "°C",
        "range": [-70, 70],
    },
    "utci_Sun_noWind": {
        "name": "UTCI: Sun & no Wind",
        "color": ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        "unit": "°C",
        "range": [-70, 70],
    },
    "utci_noSun_noWind": {
        "name": "UTCI: no Sun & no Wind",
        "color": ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        "unit": "°C",
        "range": [-70, 70],
    },
    "utci_Sun_Wind_categories": {
        "name": "UTCI: Sun & Wind : categories",
        "color": [
            [0, "#2B2977"],
            [0.0555, "#2B2977"],
            [0.0555, "#38429B"],
            [0.1665, "#38429B"],
            [0.1665, "#4253A4"],
            [0.2775, "#4253A4"],
            [0.2775, "#4B62AD"],
            [0.3885, "#4B62AD"],
            [0.3885, "#68B8E7"],
            [0.4995, "#68B8E7"],
            [0.4995, "#53B848"],
            [0.6105, "#53B848"],
            [0.6105, "#EE8522"],
            [0.7215, "#EE8522"],
            [0.7215, "#EA2C24"],
            [0.8325, "#EA2C24"],
            [0.8325, "#B12224"],
            [0.9435, "#B12224"],
            [0.9435, "#751613"],
            [1.0, "#751613"],
        ],
        "unit": thermal_stress_label,
        "range": [-5, 4],
    },
    "utci_noSun_Wind_categories": {
        "name": "UTCI: no Sun & Wind : categories",
        "color": [
            [0, "#2B2977"],
            [0.0555, "#2B2977"],
            [0.0555, "#38429B"],
            [0.1665, "#38429B"],
            [0.1665, "#4253A4"],
            [0.2775, "#4253A4"],
            [0.2775, "#4B62AD"],
            [0.3885, "#4B62AD"],
            [0.3885, "#68B8E7"],
            [0.4995, "#68B8E7"],
            [0.4995, "#53B848"],
            [0.6105, "#53B848"],
            [0.6105, "#EE8522"],
            [0.7215, "#EE8522"],
            [0.7215, "#EA2C24"],
            [0.8325, "#EA2C24"],
            [0.8325, "#B12224"],
            [0.9435, "#B12224"],
            [0.9435, "#751613"],
            [1.0, "#751613"],
        ],
        "unit": thermal_stress_label,
        "range": [-5, 4],
    },
    "utci_Sun_noWind_categories": {
        "name": "UTCI: Sun & no WInd : categories",
        "color": [
            [0, "#2B2977"],
            [0.0555, "#2B2977"],
            [0.0555, "#38429B"],
            [0.1665, "#38429B"],
            [0.1665, "#4253A4"],
            [0.2775, "#4253A4"],
            [0.2775, "#4B62AD"],
            [0.3885, "#4B62AD"],
            [0.3885, "#68B8E7"],
            [0.4995, "#68B8E7"],
            [0.4995, "#53B848"],
            [0.6105, "#53B848"],
            [0.6105, "#EE8522"],
            [0.7215, "#EE8522"],
            [0.7215, "#EA2C24"],
            [0.8325, "#EA2C24"],
            [0.8325, "#B12224"],
            [0.9435, "#B12224"],
            [0.9435, "#751613"],
            [1.0, "#751613"],
        ],
        "unit": thermal_stress_label,
        "range": [-5, 4],
    },
    "utci_noSun_noWind_categories": {
        "name": "UTCI: no Sun & no Wind : categories",
        "color": [
            [0, "#2B2977"],
            [0.0555, "#2B2977"],
            [0.0555, "#38429B"],
            [0.1665, "#38429B"],
            [0.1665, "#4253A4"],
            [0.2775, "#4253A4"],
            [0.2775, "#4B62AD"],
            [0.3885, "#4B62AD"],
            [0.3885, "#68B8E7"],
            [0.4995, "#68B8E7"],
            [0.4995, "#53B848"],
            [0.6105, "#53B848"],
            [0.6105, "#EE8522"],
            [0.7215, "#EE8522"],
            [0.7215, "#EA2C24"],
            [0.8325, "#EA2C24"],
            [0.8325, "#B12224"],
            [0.9435, "#B12224"],
            [0.9435, "#751613"],
            [1.0, "#751613"],
        ],
        "unit": thermal_stress_label,
        "range": [-5, 4],
    },
    "p_vap": {
        "name": "Vapor partial pressure",
        "color": ["#ffe600", "#00c8ff", "#0000ff"],
        "unit": "Pa",
        "range": [0, 5000],
    },
    "p_sat": {
        "name": "Saturation pressure",
        "unit": "Pa",
    },
    "hr": {
        "name": "Absolute humidity",
        "color": ["#ffe600", "#00c8ff", "#0000ff"],
        "unit": "kg water/kg dry air",
        "range": [0, 0.03],
    },
    "t_wb": {
        "name": "Wet bulb temperature",
        "color": ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        "unit": "°C",
        "range": [-40, 50],
    },
    "t_dp": {
        "name": "Dew point temperature",
        "color": ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        "unit": "°C",
        "range": [-40, 50],
    },
    "h": {
        "name": "Enthalpy",
        "color": ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        "unit": "J/kg dry air",
        "range": [0, 110000],
    },
}

# Dropdown Names
variables_sun_cloud_tab_dropdown = [
    "None",
    "DBT",
    "DPT",
    "RH",
    "Apressure",
    "EHrad",
    "HIRrad",
    "GHrad",
    "DNrad",
    "DifHrad",
    "GHillum",
    "DNillum",
    "DifHillum",
    "Zlumi",
    "Wdir",
    "Wspeed",
    "Tskycover",
    "Oskycover",
    "Vis",
]
variables_dropdown = [
    "DBT",
    "DPT",
    "RH",
    "Apressure",
    "EHrad",
    "HIRrad",
    "GHrad",
    "DNrad",
    "DifHrad",
    "GHillum",
    "DNillum",
    "DifHillum",
    "Zlumi",
    "Wdir",
    "Wspeed",
    "Tskycover",
    "Oskycover",
    "Vis",
]
variables_more_variables_dropdown = [
    "utci_Sun_Wind",
    "utci_noSun_Wind",
    "utci_Sun_noWind",
    "utci_noSun_noWind",
    "utci_Sun_Wind_categories",
    "utci_noSun_Wind_categories",
    "utci_Sun_noWind_categories",
    "utci_noSun_noWind_categories",
    "p_vap",
    "hr",
    "t_wb",
    "t_dp",
    "elevation",
    "azimuth",
    "p_sat",
]
variables_sun_cloud_tab_explore_dropdown = [
    "EHrad",
    "HIRrad",
    "GHrad",
    "DNrad",
    "DifHrad",
    "GHillum",
    "DNillum",
    "DifHillum",
    "Zlumi",
    "Oskycover",
]
variables_outdoor_dropdown = [
    "utci_Sun_Wind",
    "utci_Sun_noWind",
    "utci_noSun_Wind",
    "utci_noSun_noWind",
]

sun_cloud_tab_dropdown_names = {
    mapping_dictionary[key]["name"]: key for key in variables_sun_cloud_tab_dropdown
}

dropdown_names = {mapping_dictionary[key]["name"]: key for key in variables_dropdown}

more_variables_dropdown = {
    mapping_dictionary[key]["name"]: key for key in variables_more_variables_dropdown
}

sun_cloud_tab_explore_dropdown_names = {
    mapping_dictionary[key]["name"]: key
    for key in variables_sun_cloud_tab_explore_dropdown
}

outdoor_dropdown_names = {
    mapping_dictionary[key]["name"]: key for key in variables_outdoor_dropdown
}
