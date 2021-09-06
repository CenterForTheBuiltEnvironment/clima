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

# color dictionary
color_dict = {
    # TEMP
    "DBT": blue_red_yellow,
    "DPT": blue_red_yellow,
    # HUMIDITY
    "DryHumid": dry_humid,
    "RH": dry_humid,
    # SOLAR
    "GHrad": sun_colors,
    "DNrad": sun_colors,
    "DifHrad": sun_colors,
    "EHrad": sun_colors,
    "HIRrad": sun_colors,
    # Solar position
    "apparent_zenith": sun_colors,
    "zenith": sun_colors,
    "apparent_elevation": sun_colors,
    "elevation": sun_colors,
    "azimuth": sun_colors,
    "equation_of_time": sun_colors,
    # ILLUMINACE
    "GHillum": light_colors,
    "DNillum": light_colors,
    "DifHillum": light_colors,
    # LUMINANCE
    "Zlumi": bright_colors,
    # WIND
    "Wspeed": wind_speed_color,
    "Wdir": wind_dir_color,
    # Clouds # Visibility
    "CloudColors": cloud_colors,
    "Tskycover": cloud_colors,
    "Oskycover": cloud_colors,
    "Vis": cloud_colors,
    "hour": [
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
    "Apressure": wind_speed_color,
    # UTCI temperatures
    "utci_Sun_Wind": blue_red_yellow,
    "utci_noSun_Wind": blue_red_yellow,
    "utci_Sun_noWind": blue_red_yellow,
    "utci_noSun_noWind": blue_red_yellow,
    # UTCI categories
    "utci_Sun_Wind_categories": utci_categories_color,
    "utci_noSun_Wind_categories": utci_categories_color,
    "utci_Sun_noWind_categories": utci_categories_color,
    "utci_noSun_noWind_categories": utci_categories_color,
    # other psychrometric quantities
    "p_vap": dry_humid,
    "hr": dry_humid,
    "t_wb": blue_red_yellow,
    "t_dp": blue_red_yellow,
    "h": blue_red_yellow,
}

# Units Dictionary
degrees_unit = "\u00B0deg"
temperature_unit = "\u00B0C"
radiation_unit = "Wh/m<sup>2</sup>"
thermal_stress_label = "Thermal stress"

unit_dict = {
    "DOY": "days",
    "month": "months",
    "hour": "h",
    # Temp
    "DBT": temperature_unit,  # "&#8451"
    "DPT": temperature_unit,  # "&#8451"
    # Humidity
    "RH": "%",
    # Pressure
    "Apressure": "Pa",
    # Radiation
    "EHrad": radiation_unit,
    "HIRrad": radiation_unit,
    "GHrad": radiation_unit,
    "DNrad": radiation_unit,
    "DifHrad": radiation_unit,
    # Illuminance
    "GHillum": "lux",
    "DNillum": "lux",
    "DifHillum": "lux",
    # Luminance
    "Zlumi": "cd/m<sup>2</sup>",
    # Wind
    "Wdir": degrees_unit,
    "Wspeed": "m/s",
    # Clouds
    "Tskycover": "tenths",
    "Oskycover": "tenths",
    # Visibility
    "Vis": "Km",
    # Solar position
    "apparent_zenith": degrees_unit,
    "zenith": degrees_unit,
    "apparent_elevation": degrees_unit,
    "elevation": degrees_unit,
    "azimuth": degrees_unit,
    "equation_of_time": degrees_unit,
    # UTCI temperatures
    "utci_Sun_Wind": temperature_unit,  # "&#8451",
    "utci_noSun_Wind": temperature_unit,  # "&#8451",
    "utci_Sun_noWind": temperature_unit,  # "&#8451",
    "utci_noSun_noWind": temperature_unit,  # "&#8451",
    # UTCI categories
    "utci_Sun_Wind_categories": thermal_stress_label,
    "utci_noSun_Wind_categories": thermal_stress_label,
    "utci_Sun_noWind_categories": thermal_stress_label,
    "utci_noSun_noWind_categories": thermal_stress_label,
    # other psychrometric values
    "p_vap": "Pa",
    "hr": "kg water/kg dry air",
    "t_wb": temperature_unit,  # "&#8451"
    "t_dp": temperature_unit,  # "&#8451"
    "h": "J/kg dry air",
}

# Global Names
name_dict = {
    "DOY": "Day of the year",
    "day": "day",
    "month": "months",
    "hour": "hours of the day",
    # Temp
    "DBT": "Dry bulb temperature",
    "DPT": "Dew point temperature",
    # Humidity
    "RH": "Relative humidity",
    # Pressure
    "Apressure": "Atmospheric pressure",
    # Radiation
    "EHrad": "Extraterrestrial horizontal irradiation",
    "HIRrad": "´Horizontal infrared radiation",
    "GHrad": "Global horizontal radiation",
    "DNrad": "Direct normal radiation",
    "DifHrad": "Diffuse horizontal radiation",
    # Illuminance
    "GHillum": "Global horizontal illuminance",
    "DNillum": "Direct normal illuminance",
    "DifHillum": "Diffuse horizontal illuminance",
    # Luminance
    "Zlumi": "Zenith luminance",
    # Wind
    "Wdir": "Wind direction",
    "Wspeed": "Wind speed",
    # Clouds
    "Tskycover": "Total sky cover",
    "Oskycover": "Opaque sky cover",
    # Visibility
    "Vis": "Visibility",
    # Solar position
    "apparent_zenith": "Apparent zenith",
    "zenith": "Zenith",
    "apparent_elevation": "Apparent elevation",
    "elevation": "Elevation",
    "azimuth": "Azimuth",
    "equation_of_time": "Equation of time",
    # UTCI temperatures
    "utci_Sun_Wind": "UTCI: Sun & Wind",
    "utci_noSun_Wind": "UTCI: no Sun & Wind",
    "utci_Sun_noWind": "UTCI: Sun & no WInd",
    "utci_noSun_noWind": "UTCI: no Sun & no Wind",
    # UTCI categories
    "utci_Sun_Wind_categories": "UTCI: Sun & Wind : categories",
    "utci_noSun_Wind_categories": "UTCI: no Sun & Wind : categories",
    "utci_Sun_noWind_categories": "UTCI: Sun & no WInd : categories",
    "utci_noSun_noWind_categories": "UTCI: no Sun & no Wind : categories",
    # psychrometric variables
    "p_vap": "Vapor partial pressure",
    "hr": "Absolute humidity",
    "t_wb": "Wet bulb temperature",
    "t_dp": "Dew point temperature",
    "h": "Enthalpy",
}

# Dropdown Names
sun_cloud_tab_dropdown_names = {
    "None": "None",
    "Dry bulb temperature": "DBT",
    "Dew point temperature": "DPT",
    "Relative humidity": "RH",
    "Atmospheric pressure": "Apressure",
    "Extraterrestrial horizontal irradiation": "EHrad",
    "Horizontal infrared radiation": "HIRrad",
    "Global horizontal radiation": "GHrad",
    "Direct normal radiation": "DNrad",
    "Diffuse horizontal radiation": "DifHrad",
    "Global horizontal illuminance": "GHillum",
    "Direct normal illuminance": "DNillum",
    "Diffuse horizontal illuminance": "DifHillum",
    "Zenith luminance": "Zlumi",
    "Wind direction": "Wdir",
    "Wind speed": "Wspeed",
    "Total sky cover": "Tskycover",
    "Opaque sky cover": "Oskycover",
    "Visibility": "Vis",
}

dropdown_names = {
    "Dry bulb temperature": "DBT",
    "Dew point temperature": "DPT",
    "Relative humidity": "RH",
    "Atmospheric pressure": "Apressure",
    "Extraterrestrial horizontal irradiation": "EHrad",
    "Horizontal infrared radiation": "HIRrad",
    "Global horizontal radiation": "GHrad",
    "Direct normal radiation": "DNrad",
    "Diffuse horizontal radiation": "DifHrad",
    "Global horizontal illuminance": "GHillum",
    "Direct normal illuminance": "DNillum",
    "Diffuse horizontal illuminance": "DifHillum",
    "Zenith luminance": "Zlumi",
    "Wind direction": "Wdir",
    "Wind speed": "Wspeed",
    "Total sky cover": "Tskycover",
    "Opaque sky cover": "Oskycover",
    "Visibility": "Vis",
}

more_variables_dropdown = {
    "UTCI: Sun & Wind": "utci_Sun_Wind",
    "UTCI: no Sun & Wind": "utci_noSun_Wind",
    "UTCI: Sun & no WInd": "utci_Sun_noWind",
    "UTCI: no Sun & no Wind": "utci_noSun_noWind",
    "UTCI: Sun & Wind : categories": "utci_Sun_Wind_categories",
    "UTCI: no Sun & Wind : categories": "utci_noSun_Wind_categories",
    "UTCI: Sun & no WInd : categories": "utci_Sun_noWind_categories",
    "UTCI: no Sun & no Wind : categories": "utci_noSun_noWind_categories",
    "Vapor partial pressure": "p_vap",
    "Absolute humidity": "hr",
    "Wet bulb temperature": "t_wb",
    "Dew point temperature": "t_dp",
    "Solar elevation": "elevation",
    "Solar azimuth": "azimuth",
    "Saturation pressure": "p_sat",
}

sun_cloud_tab_explore_dropdown_names = {
    "Extraterrestrial horizontal irradiation": "EHrad",
    "Horizontal infrared radiation": "HIRrad",
    "Global horizontal radiation": "GHrad",
    "Direct normal radiation": "DNrad",
    "Diffuse horizontal radiation": "DifHrad",
    "Global horizontal illuminance": "GHillum",
    "Direct normal illuminance": "DNillum",
    "Diffuse horizontal illuminance": "DifHillum",
    "Zenith luminance": "Zlumi",
    "Opaque sky cover": "Oskycover",
}

outdoor_dropdown_names = {
    "Exposed to the sun and the wind": "utci_Sun_Wind",
    "Exposed to the sun and protected from the wind": "utci_Sun_noWind",
    "Protected from the sun and exposed to the wind": "utci_noSun_Wind",
    "Protected from the sun and the wind": "utci_noSun_noWind",
}

# Global Value Ranges
range_dict = {
    "DOY": [0, 365],
    "month": [1, 12],
    "day": [1, 31],
    "hour": [1, 24],
    # Temp
    "DBT": [-40, 50],
    "DPT": [-50, 35],
    # Humidity
    "RH": [0, 100],
    # Pressure
    "Apressure": [95000, 105000],
    # Radiation
    "EHrad": [0, 1200],
    "HIRrad": [0, 500],
    "GHrad": [0, 1200],
    "DNrad": [0, 1200],
    "DifHrad": [0, 1200],
    # Illuminance
    "GHillum": [0, 120000],
    "DNillum": [0, 120000],
    "DifHillum": [0, 120000],
    # Luminance
    "Zlumi": [0, 60000],
    # Wind
    "Wdir": [0, 360],
    "Wspeed": [0, 20],
    # Clouds
    "Tskycover": [0, 10],
    "Oskycover": [0, 10],
    # Visibility
    "Vis": [0, 100],
    # Solar position
    "apparent_zenith": [0, 180],
    "zenith": [0, 180],
    "apparent_elevation": [-90, 90],
    "elevation": [-90, 90],
    "azimuth": [0, 360],
    "equation_of_time": [-20, 20],
    # utci temperatures
    "utci_Sun_Wind": [-70, 70],
    "utci_noSun_Wind": [-70, 70],
    "utci_Sun_noWind": [-70, 70],
    "utci_noSun_noWind": [-70, 70],
    # utci categories
    "utci_Sun_Wind_categories": [-5, 4],
    "utci_noSun_Wind_categories": [-5, 4],
    "utci_Sun_noWind_categories": [-5, 4],
    "utci_noSun_noWind_categories": [-5, 4],
    # other psychrometric quantities
    "p_vap": [0, 5000],
    "hr": [0, 0.03],
    "t_wb": [-40, 50],
    "t_dp": [-40, 50],
    "h": [0, 110000],
}

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
