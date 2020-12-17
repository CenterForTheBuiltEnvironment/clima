#########################
### Colors Dictionary ###
#########################

color_dict = {
    # TEMP
    'BlueRedYellow' : ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
    'DBT_color' : ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
    'DPT_color' : ["#00b3ff", "#000082", "#ff0000", "#ffff00"],

    # HUMIDITY
    'DryHumid' : ["#ffe600", "#00c8ff", "#0000ff"],
    'RH_color' : ["#ffe600", "#00c8ff", "#0000ff"],

    # SOLAR
    'SunColors' : ["#293a59", "#ff0000", "#ffff00", "#ffffff"],
    'GHrad_color' : ["#293a59", "#ff0000", "#ffff00", "#ffffff"],
    'DNrad_color' : ["#293a59", "#ff0000", "#ffff00", "#ffffff"],
    'DifHrad_color' : ["#293a59", "#ff0000", "#ffff00", "#ffffff"],
    'EHrad_color' : ["#293a59", "#ff0000", "#ffff00", "#ffffff"],
    'HIRrad_color' : ["#293a59", "#ff0000", "#ffff00", "#ffffff"],

    # Solar position
    'apparent_zenith_color' : ["#293a59", "#ff0000", "#ffff00", "#ffffff"],
    'zenith_color' : ["#293a59", "#ff0000", "#ffff00", "#ffffff"],
    'apparent_elevation_color' : ["#293a59", "#ff0000", "#ffff00", "#ffffff"],
    'elevation_color' : ["#293a59", "#ff0000", "#ffff00", "#ffffff"],
    'azimuth_color' : ["#293a59", "#ff0000", "#ffff00", "#ffffff"],
    'equation_of_time_color' : ["#293a59", "#ff0000", "#ffff00", "#ffffff"],

    # ILLUMINACE
    'lightColors' : ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],
    'GHillum_color' : ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],
    'DNillum_color' : ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],
    'DifHillum_color' : ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],

    # LUMINANCE
    'brightColors' : ["#730a8c", "#0d0db3", "#0f85be", "#0f85be", "#b11421", "#fdf130"],
    'Zlumi_color' : ["#730a8c", "#0d0db3", "#0f85be", "#0f85be", "#b11421", "#fdf130"],

    # WIND
    'Wspeed_color' : ["#ffffff", "#b2f2ff", "#33ddff", "#00aaff", "#0055ff", "#0000ff", "#aa00ff", "#ff00ff", "#cc0000", "#ffaa00"],
    'Wdir_color' : ["#0072dd", "#00c420", "#eded00", "#be00d5", "#0072dd"],

    # Clouds # Visibility
    'CloudColors' : ["#00aaff", "#ffffff", "#c2c2c2"],
    'Tskycover_color' : ["#00aaff", "#ffffff", "#c2c2c2"],
    'Oskycover_color' : ["#00aaff", "#ffffff", "#c2c2c2"],
    'Vis_color' : ["#00aaff", "#ffffff", "#c2c2c2"],

    'hour_color' : ["#000000", "#355e7e", "#6b5c7b", "#c06c84", "#f8b195", "#c92a42", "#c92a42", "#c92a42", "#000000"]
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
### Variable Names ###
######################
var_name_lst = [
    "DOY",
    "day",
    "month",
    "hour",
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
    "apparent",
    "zenith",
    "apparent_elevation",
    "elevation",
    "azimuth",
    "equation_of_time"
]

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

###################################
### Template and Configurations ###
###################################
template = "plotly"
config = {
    'modeBarButtonsToRemove': ['toggleSpikelines', 'hoverCompareCartesian', "pan2d", "lasso2d", "zoomIn2d", "zoomOut2d", "hoverClosestCartesian"],
    "modeBarButtonsToAdd": ["select2d"],
    'displaylogo': False,
    "displayModeBar": "hover"
}