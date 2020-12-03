# TEMP
BlueRedYellow = ["#00b3ff", "#000082", "#ff0000", "#ffff00"]
DBT_color = BlueRedYellow
DPT_color = DBT_color

# HUMIDITY
DryHumid = ["#ffe600", "#00c8ff", "#0000ff"]
RH_color = DryHumid

# SOLAR
SunColors = ["#293a59", "#ff0000", "#ffff00", "#ffffff"]
GHrad_color = SunColors
DNrad_color = GHrad_color
DifHrad_color = GHrad_color
EHrad_color = GHrad_color
HIRrad_color = GHrad_color

# Solar position
apparent_zenith_color = SunColors
zenith_color = SunColors
apparent_elevation_color = SunColors
elevation_color = SunColors
azimuth_color = SunColors
equation_of_time_color = SunColors

#ILLUMINACE
lightColors = ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"]
GHillum_color = lightColors
DNillum_color = lightColors
DifHillum_color = lightColors

# LUMINANCE
brightColors = ["#730a8c", "#0d0db3", "#0f85be", "#0f85be", "#b11421", "#fdf130"]
Zlumi_color = brightColors

# WIND
Wspeed_color = ["#ffffff", "#b2f2ff", "#33ddff", "#00aaff", "#0055ff", "#0000ff", "#aa00ff", "#ff00ff", "#cc0000", "#ffaa00"]
Wdir_color = ["#0072dd", "#00c420", "#eded00", "#be00d5", "#0072dd"]

# Clouds # Visibility
CloudColors = ["#00aaff", "#ffffff", "#c2c2c2"]
Tskycover_color = CloudColors
Oskycover_color = CloudColors
Vis_color = CloudColors

# Global Value Ranges
DBT_range = [-40,50]
DPT_range = [-50,35]
RH_range = [0,100]
GHrad_range = [0,1200]
DNrad_range = GHrad_range
DifHrad_range = GHrad_range
Wspeed_range = [0,20]

hour_color = ["#000000", "#355e7e", "#6b5c7b", "#c06c84", "#f8b195", "#c92a42", "#c92a42", "#c92a42", "#000000"]
template = "ggplot2"

config = {
    'modeBarButtonsToRemove': ['toggleSpikelines', 'hoverCompareCartesian', "pan2d", "lasso2d", "zoomIn2d", "zoomOut2d", "hoverClosestCartesian"],
    "modeBarButtonsToAdd": ["select2d"],
    'displaylogo': False,
    "displayModeBar": "hover"
}