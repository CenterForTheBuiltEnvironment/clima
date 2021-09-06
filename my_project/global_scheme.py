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
Wspeed_color = [
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
Wdir_color = ["#0072dd", "#00c420", "#eded00", "#be00d5", "#0072dd"]
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
    "DBT_color": blue_red_yellow,
    "DPT_color": blue_red_yellow,
    # HUMIDITY
    "DryHumid": dry_humid,
    "RH_color": dry_humid,
    # SOLAR
    "GHrad_color": sun_colors,
    "DNrad_color": sun_colors,
    "DifHrad_color": sun_colors,
    "EHrad_color": sun_colors,
    "HIRrad_color": sun_colors,
    # Solar position
    "apparent_zenith_color": sun_colors,
    "zenith_color": sun_colors,
    "apparent_elevation_color": sun_colors,
    "elevation_color": sun_colors,
    "azimuth_color": sun_colors,
    "equation_of_time_color": sun_colors,
    # ILLUMINACE
    "GHillum_color": light_colors,
    "DNillum_color": light_colors,
    "DifHillum_color": light_colors,
    # LUMINANCE
    "Zlumi_color": bright_colors,
    # WIND
    "Wspeed_color": Wspeed_color,
    "Wdir_color": Wdir_color,
    # Clouds # Visibility
    "CloudColors": cloud_colors,
    "Tskycover_color": cloud_colors,
    "Oskycover_color": cloud_colors,
    "Vis_color": cloud_colors,
    "hour_color": [
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
    "Apressure_color": Wspeed_color,
    # UTCI temperatures
    "utci_Sun_Wind_color": blue_red_yellow,
    "utci_noSun_Wind_color": blue_red_yellow,
    "utci_Sun_noWind_color": blue_red_yellow,
    "utci_noSun_noWind_color": blue_red_yellow,
    # UTCI categories
    "utci_Sun_Wind_categories_color": utci_categories_color,
    "utci_noSun_Wind_categories_color": utci_categories_color,
    "utci_Sun_noWind_categories_color": utci_categories_color,
    "utci_noSun_noWind_categories_color": utci_categories_color,
    # other psychrometric quantities
    "p_vap_color": dry_humid,
    "hr_color": dry_humid,
    "t_wb_color": blue_red_yellow,
    "t_dp_color": blue_red_yellow,
    "h_color": blue_red_yellow,
}

# Units Dictionary
degrees_unit = "\u00B0deg"
temperature_unit = "\u00B0C"
radiation_unit = "Wh/m<sup>2</sup>"
thermal_stress_label = "Thermal stress"

unit_dict = {
    "DOY_unit": "days",
    "month_unit": "months",
    "hour_unit": "h",
    # Temp
    "DBT_unit": temperature_unit,  # "&#8451"
    "DPT_unit": temperature_unit,  # "&#8451"
    # Humidity
    "RH_unit": "%",
    # Pressure
    "Apressure_unit": "Pa",
    # Radiation
    "EHrad_unit": radiation_unit,
    "HIRrad_unit": radiation_unit,
    "GHrad_unit": radiation_unit,
    "DNrad_unit": radiation_unit,
    "DifHrad_unit": radiation_unit,
    # Illuminance
    "GHillum_unit": "lux",
    "DNillum_unit": "lux",
    "DifHillum_unit": "lux",
    # Luminance
    "Zlumi_unit": "cd/m<sup>2</sup>",
    # Wind
    "Wdir_unit": degrees_unit,
    "Wspeed_unit": "m/s",
    # Clouds
    "Tskycover_unit": "tenths",
    "Oskycover_unit": "tenths",
    # Visibility
    "Vis_unit": "Km",
    # Solar position
    "apparent_zenith_unit": degrees_unit,
    "zenith_unit": degrees_unit,
    "apparent_elevation_unit": degrees_unit,
    "elevation_unit": degrees_unit,
    "azimuth_unit": degrees_unit,
    "equation_of_time_unit": degrees_unit,
    # UTCI temperatures
    "utci_Sun_Wind_unit": temperature_unit,  # "&#8451",
    "utci_noSun_Wind_unit": temperature_unit,  # "&#8451",
    "utci_Sun_noWind_unit": temperature_unit,  # "&#8451",
    "utci_noSun_noWind_unit": temperature_unit,  # "&#8451",
    # UTCI categories
    "utci_Sun_Wind_categories_unit": thermal_stress_label,
    "utci_noSun_Wind_categories_unit": thermal_stress_label,
    "utci_Sun_noWind_categories_unit": thermal_stress_label,
    "utci_noSun_noWind_categories_unit": thermal_stress_label,
    # other psychrometric values
    "p_vap_unit": "Pa",
    "hr_unit": "kg water/kg dry air",
    "t_wb_unit": temperature_unit,  # "&#8451"
    "t_dp_unit": temperature_unit,  # "&#8451"
    "h_unit": "J/kg dry air",
}

# Global Names
name_dict = {
    "DOY_name": "Day of the year",
    "day_name": "day",
    "month_name": "months",
    "hour_name": "hours of the day",
    # Temp
    "DBT_name": "Dry bulb temperature",
    "DPT_name": "Dew point temperature",
    # Humidity
    "RH_name": "Relative humidity",
    # Pressure
    "Apressure_name": "Atmospheric pressure",
    # Radiation
    "EHrad_name": "Extraterrestrial horizontal irradiation",
    "HIRrad_name": "´Horizontal infrared radiation",
    "GHrad_name": "Global horizontal radiation",
    "DNrad_name": "Direct normal radiation",
    "DifHrad_name": "Diffuse horizontal radiation",
    # Illuminance
    "GHillum_name": "Global horizontal illuminance",
    "DNillum_name": "Direct normal illuminance",
    "DifHillum_name": "Diffuse horizontal illuminance",
    # Luminance
    "Zlumi_name": "Zenith luminance",
    # Wind
    "Wdir_name": "Wind direction",
    "Wspeed_name": "Wind speed",
    # Clouds
    "Tskycover_name": "Total sky cover",
    "Oskycover_name": "Opaque sky cover",
    # Visibility
    "Vis_name": "Visibility",
    # Solar position
    "apparent_zenith_name": "Apparent zenith",
    "zenith_name": "Zenith",
    "apparent_elevation_name": "Apparent elevation",
    "elevation_name": "Elevation",
    "azimuth_name": "Azimuth",
    "equation_of_time_name": "Equation of time",
    # UTCI temperatures
    "utci_Sun_Wind_name": "UTCI: Sun & Wind",
    "utci_noSun_Wind_name": "UTCI: no Sun & Wind",
    "utci_Sun_noWind_name": "UTCI: Sun & no WInd",
    "utci_noSun_noWind_name": "UTCI: no Sun & no Wind",
    # UTCI categories
    "utci_Sun_Wind_categories_name": "UTCI: Sun & Wind : categories",
    "utci_noSun_Wind_categories_name": "UTCI: no Sun & Wind : categories",
    "utci_Sun_noWind_categories_name": "UTCI: Sun & no WInd : categories",
    "utci_noSun_noWind_categories_name": "UTCI: no Sun & no Wind : categories",
    # psychrometric variables
    "p_vap_name": "Vapor partial pressure",
    "hr_name": "Absolute humidity",
    "t_wb_name": "Wet bulb temperature",
    "t_dp_name": "Dew point temperature",
    "h_name": "Enthalpy",
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
    "DOY_range": [0, 365],
    "month_range": [1, 12],
    "day_range": [1, 31],
    "hour_range": [1, 24],
    # Temp
    "DBT_range": [-40, 50],
    "DPT_range": [-50, 35],
    # Humidity
    "RH_range": [0, 100],
    # Pressure
    "Apressure_range": [95000, 105000],
    # Radiation
    "EHrad_range": [0, 1200],
    "HIRrad_range": [0, 500],
    "GHrad_range": [0, 1200],
    "DNrad_range": [0, 1200],
    "DifHrad_range": [0, 1200],
    # Illuminance
    "GHillum_range": [0, 120000],
    "DNillum_range": [0, 120000],
    "DifHillum_range": [0, 120000],
    # Luminance
    "Zlumi_range": [0, 60000],
    # Wind
    "Wdir_range": [0, 360],
    "Wspeed_range": [0, 20],
    # Clouds
    "Tskycover_range": [0, 10],
    "Oskycover_range": [0, 10],
    # Visibility
    "Vis_range": [0, 100],
    # Solar position
    "apparent_zenith_range": [0, 180],
    "zenith_range": [0, 180],
    "apparent_elevation_range": [-90, 90],
    "elevation_range": [-90, 90],
    "azimuth_range": [0, 360],
    "equation_of_time_range": [-20, 20],
    # utci temperatures
    "utci_Sun_Wind_range": [-70, 70],
    "utci_noSun_Wind_range": [-70, 70],
    "utci_Sun_noWind_range": [-70, 70],
    "utci_noSun_noWind_range": [-70, 70],
    # utci categories
    "utci_Sun_Wind_categories_range": [-5, 4],
    "utci_noSun_Wind_categories_range": [-5, 4],
    "utci_Sun_noWind_categories_range": [-5, 4],
    "utci_noSun_noWind_categories_range": [-5, 4],
    # other psychrometric quantities
    "p_vap_range": [0, 5000],
    "hr_range": [0, 0.03],
    "t_wb_range": [-40, 50],
    "t_dp_range": [-40, 50],
    "h_range": [0, 110000],
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
