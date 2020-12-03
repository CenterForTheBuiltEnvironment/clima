#########################
### Colors Dictionary ###
#########################
colors = {
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
# unit_dict = {
#   "DOY_unit" : DOY_unit,
#   "month_unit" : month_unit,
#   "hour_unit" : hour_unit,
#   "DBT_unit" : DBT_unit,
#   "DPT_unit" : DPT_unit,
#   "RH_unit" : RH_unit,
#   "Apressure_unit" : Apressure_unit,
#   "EHrad_unit" : EHrad_unit,
#   "HIRrad_unit" : HIRrad_unit,
#   "GHrad_unit" : GHrad_unit,
#   "DNrad_unit" : DNrad_unit,
#   "DifHrad_unit" : DifHrad_unit,
#   "GHillum_unit" : GHillum_unit,
#   "DNillum_unit" : DNillum_unit,
#   "DifHillum_unit" : DifHillum_unit,
#   "Zlumim_unit" : Zlumim_unit,
#   "Wdir_unit" : Wdir_unit,
#   "Wspeed_unit" : Wspeed_unit,
#   "Tskycover_unit" : Tskycover_unit,
#   "Oskycover_unit" : Oskycover_unit,
#   "Vis_unit" : Vis_unit,
#   "apparent_zenith_unit" : apparent_zenith_unit,
#   "zenith_unit" : zenith_unit,
#   "apparent_elevation_unit" : apparent_elevation_unit,
#   "elevation_unit" : elevation_unit,
#   "azimuth_unit" : azimuth_unit,
#   "equation_of_time_unit" : equation_of_time_unit
# }

###########################
### Global Value Ranges ###
###########################
DBT_range = [-40, 50]
DPT_range = [-50, 35]
RH_range = [0, 100]
GHrad_range = [0, 1200]
DNrad_range = GHrad_range
DifHrad_range = GHrad_range
Wspeed_range = [0, 20]


###################################
### Template and Configurations ###
###################################
template = "ggplot2"
config = {
    'modeBarButtonsToRemove': ['toggleSpikelines', 'hoverCompareCartesian', "pan2d", "lasso2d", "zoomIn2d", "zoomOut2d", "hoverClosestCartesian"],
    "modeBarButtonsToAdd": ["select2d"],
    'displaylogo': False,
    "displayModeBar": "hover"
}