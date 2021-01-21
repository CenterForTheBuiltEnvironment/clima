#########################
### Colors Dictionary ###
#########################
blue_red_yellow = ["#00b3ff", "#000082", "#ff0000", "#ffff00"]
dry_humid = ["#ffe600", "#00c8ff", "#0000ff"]
sun_colors = ["#293a59", "#ff0000", "#ffff00", "#ffffff"]
light_colors = ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"]
bright_colors = ["#730a8c", "#0d0db3", "#0f85be", "#0f85be", "#b11421", "#fdf130"]
Wspeed_color = ["#ffffff", "#b2f2ff", "#33ddff", "#00aaff", "#0055ff", "#0000ff", "#aa00ff", "#ff00ff", "#cc0000", "#ffaa00"]
Wdir_color = ["#0072dd", "#00c420", "#eded00", "#be00d5", "#0072dd"]
cloud_colors = ["#00aaff", "#ffffff", "#c2c2c2"]


color_dict = {
    # TEMP
    'DBT_color' : blue_red_yellow,
    'DPT_color' : blue_red_yellow,

    # HUMIDITY
    'DryHumid' : dry_humid,
    'RH_color' : dry_humid,

    # SOLAR
    'GHrad_color' : sun_colors,
    'DNrad_color' : sun_colors,
    'DifHrad_color' : sun_colors,
    'EHrad_color' : sun_colors,
    'HIRrad_color' : sun_colors,

    # Solar position
    'apparent_zenith_color' : sun_colors,
    'zenith_color' : sun_colors,
    'apparent_elevation_color' : sun_colors,
    'elevation_color' : sun_colors,
    'azimuth_color' : sun_colors,
    'equation_of_time_color' : sun_colors,

    # ILLUMINACE
    'GHillum_color' : light_colors,
    'DNillum_color' : light_colors,
    'DifHillum_color' : light_colors,

    # LUMINANCE
    'Zlumi_color' : bright_colors,

    # WIND
    'Wspeed_color' : Wspeed_color,
    'Wdir_color' : Wdir_color,

    # Clouds # Visibility
    'CloudColors' : cloud_colors,
    'Tskycover_color' : cloud_colors,
    'Oskycover_color' : cloud_colors,
    'Vis_color' : cloud_colors,

    'hour_color' : ["#000000", "#355e7e", "#6b5c7b", "#c06c84", "#f8b195", "#c92a42", "#c92a42", "#c92a42", "#000000"],
    "Apressure_color" : Wspeed_color,


}

########################
### Units Dictionary ###
########################

unit_dict = {
    "DOY_unit" : "days",
    "month_unit" : "months",
    "hour_unit" : "h",

    # Temp
    "DBT_unit" : "\u00B0 C", # "&#8451"
    "DPT_unit" : "\u00B0 C", # "&#8451"

    # Humidity
    "RH_unit" : "%",

    # Pressure
    "Apressure_unit" : "Pa",

    # Radiation
    "EHrad_unit" : "Wh/m<sup>2</sup>",
    "HIRrad_unit" : "Wh/m<sup>2</sup>",
    "GHrad_unit" : "Wh/m<sup>2</sup>",
    "DNrad_unit" : "Wh/m<sup>2</sup>",
    "DifHrad_unit" : "Wh/m<sup>2</sup>",

    # Illuminance
    "GHillum_unit" : "lux",
    "DNillum_unit" : "lux",
    "DifHillum_unit" : "lux",

    # Luminance
    "Zlumim_unit" : "cd/m<sup>2</sup>",

    # Wind
    "Wdir_unit" : "\u00B0 deg",
    "Wspeed_unit" : "m/s",

    # Clouds
    "Tskycover_unit" : "tenths",
    "Oskycover_unit" : "tenths",

    #Visibility
    "Vis_unit" : "Km",

    # Solar position
    "apparent_zenith_unit" : "\u00B0 deg",
    "zenith_unit" : "\u00B0 deg",
    "apparent_elevation_unit" : "\u00B0 deg",
    "elevation_unit" : "\u00B0 deg",
    "azimuth_unit" : "\u00B0 deg",
    "equation_of_time_unit" : "\u00B0 deg"
}

####################
### Global Names ###
####################
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
    "GHillum_name": "Global horizontal iluminance",
    "DNillum_name": "Direct normal iluminance",
    "DifHillum_name": "Diffuse horizontal iluminance",

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
    "equation_of_time_name": "Equation of time"
}

######################
### Dropdown Names ###
######################
dropdown_names = {
    "Dry bulb temperature" : "DBT",
    "Dew point temperature" : "DPT",
    "Relative humidity" : "RH",
    "Atmospheric pressure" : "Apressure",
    "Extraterrestrial horizontal irradiation" : "EHrad",
    "Horizontal infrared radiation" : "HIRrad",
    "Global horizontal radiation" : "GHrad",
    "Direct normal radiation" : "DNrad",
    "Diffuse horizontal radiation" : "DifHrad",
    "Global horizontal iluminance" : "GHillum",
    "Direct normal iluminance" : "DNillum",
    "Diffuse horizontal iluminance" : "DifHillum",
    "Zenith luminance" : "Zlumi",
    "Wind direction" : "Wdir",
    "Wind speed" : "Wspeed",
    "Total sky cover" : "Tskycover",
    "Opaque sky cover" : "Oskycover",
    "Visibility" : "Vis",
}

###########################
### Global Value Ranges ###
###########################
range_dict = {
    "DOY_range" : [0, 365],
    "month_range" : [1, 12],
    "day_range" : [1, 31],
    "hour_range" : [1, 24],

    # Temp
    "DBT_range" : [-40, 50],
    "DPT_range" : [-50, 35],

    # Humidity
    "RH_range" : [0, 100],

    # Pressure
    "Apressure_range" : [95000, 105000],

    # Radiation
    "EHrad_range" : [0, 1200],
    "HIRrad_range" : [0, 500],
    "GHrad_range" : [0, 1200],
    "DNrad_range" : [0, 1200],
    "DifHrad_range" : [0, 1200],

    # Illuminance
    "GHillum_range" : [0,120000],
    "DNillum_range" : [0,120000],
    "DifHillum_range" : [0,120000],

    # Luminance
    "Zlumi_range" : [0,60000],

    # Wind
    "Wdir_range" : [0,360],
    "Wspeed_range" : [0,20],

    # Clouds
    "Tskycover_range" : [0,10],
    "Oskycover_range" : [0,10],

    # Visibility
    "Vis_range" : [0,100],

    # Solar position
    "apparent_zenith_range" : [0,180],
    "zenith_range" : [0,180],
    "apparent_elevation_range" : [-90,90],
    "elevation_range" : [-90,90],
    "azimuth_range" : [0,360],
    "equation_of_time_range" : [-20,20],
}

#############
### Misc. ###
#############
month_lst = ["Jan","Feb","Mar","Apr","May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

"""
template = "plotly"
config = {
    'modeBarButtonsToRemove': ['toggleSpikelines', 'hoverCompareCartesian', "pan2d", "lasso2d", "zoomIn2d", "zoomOut2d", "hoverClosestCartesian"],
    "modeBarButtonsToAdd": ["select2d"],
    'displaylogo': False,
    "displayModeBar": "hover"
}

"""

import plotly.io as pio

clima_template = "plotly_white"

pio.templates.default = clima_template
template=clima_template

config={
    'modeBarButtonsToRemove': 
    ['toggleSpikelines','hoverCompareCartesian',"select2d","zoom2d",
     "autoScale2d","resetScale2d","pan2d","lasso2d",
     "zoomIn2d","zoomOut2d","hoverClosestCartesian"],
    'displaylogo': False,
     "displayModeBar": "hover",
     'toImageButtonOptions': {
    'format': 'svg',
    'filename': "Clima tool graph"}
}