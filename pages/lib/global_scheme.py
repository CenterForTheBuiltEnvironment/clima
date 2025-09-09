import plotly.io as pio
from pages.lib.global_column_names import ColNames

from config import UnitSystem

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
cloud_colors = [
    "#7ec9f3",
    "#e6eae9",
    "#c2c2c2",
]
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
degrees_unit = "\u00b0deg"
temperature_unit = "\u00b0C"
thermal_stress_label = "Thermal stress"

mapping_dictionary = {
    ColNames.NONE: {ColNames.NAME: "None"},
    ColNames.DOY: {
        ColNames.NAME: "Day of the year",
        ColNames.UNIT: "days",
        ColNames.RANGE: [0, 365],
    },
    ColNames.DAY: {ColNames.NAME: "day", ColNames.RANGE: [1, 31]},
    ColNames.MONTH: {
        ColNames.NAME: "months",
        ColNames.UNIT: "months",
        ColNames.RANGE: [1, 12],
    },
    ColNames.HOUR: {
        ColNames.NAME: "Hour",
        ColNames.COLOR: [
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
        ColNames.UNIT: "h",
        ColNames.RANGE: [1, 24],
    },
    ColNames.DBT: {
        ColNames.NAME: "Dry bulb temperature",
        ColNames.COLOR: ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        UnitSystem.SI: {
            ColNames.UNIT: "°C",
            ColNames.RANGE: [-40, 50],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°F",
            ColNames.RANGE: [-40, 122],
        },
    },
    ColNames.DPT: {
        ColNames.NAME: "Dew point temperature",
        ColNames.COLOR: ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        UnitSystem.SI: {
            ColNames.UNIT: "°C",
            ColNames.RANGE: [-50, 35],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°F",
            ColNames.RANGE: [-58, 95],
        },
    },
    ColNames.RH: {
        ColNames.NAME: "Relative humidity",
        ColNames.COLOR: ["#ffe600", "#00c8ff", "#0000ff"],
        UnitSystem.SI: {
            ColNames.UNIT: "%",
            ColNames.RANGE: [0, 100],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "%",
            ColNames.RANGE: [0, 100],
        },
    },
    ColNames.P_ATM: {
        ColNames.NAME: "Atmospheric pressure",
        ColNames.COLOR: [
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
        UnitSystem.SI: {
            ColNames.UNIT: "Pa",
            ColNames.RANGE: [95000, 105000],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "Psi",
            ColNames.RANGE: [95000 * 0.000145038, 1050000.000145038],
        },
    },
    ColNames.EXTR_HOR_RAD: {
        ColNames.NAME: "Extraterrestrial horizontal irradiation",
        ColNames.COLOR: [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        UnitSystem.SI: {
            ColNames.UNIT: "Wh/m<sup>2</sup>",
            ColNames.RANGE: [0, 1200],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "Btu/ft<sup>2</sup>",
            ColNames.RANGE: [0, 1200 * 0.3169983306],
        },
    },
    ColNames.HOR_IR_RAD: {
        ColNames.NAME: "Horizontal infrared radiation",
        ColNames.COLOR: [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        UnitSystem.SI: {
            ColNames.UNIT: "Wh/m<sup>2</sup>",
            ColNames.RANGE: [0, 500],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "Btu/ft<sup>2</sup>",
            ColNames.RANGE: [0, 500 * 0.3169983306],
        },
    },
    ColNames.GLOB_HOR_RAD: {
        ColNames.NAME: "Global horizontal radiation",
        ColNames.COLOR: [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        UnitSystem.SI: {
            ColNames.UNIT: "Wh/m<sup>2</sup>",
            ColNames.RANGE: [0, 1200],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "Btu/ft<sup>2</sup>",
            ColNames.RANGE: [0, 1200 * 0.3169983306],
        },
    },
    ColNames.DIR_NOR_RAD: {
        ColNames.NAME: "Direct normal radiation",
        ColNames.COLOR: [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        UnitSystem.SI: {
            ColNames.UNIT: "Wh/m<sup>2</sup>",
            ColNames.RANGE: [0, 1200],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "Btu/ft<sup>2</sup>",
            ColNames.RANGE: [0, 1200 * 0.3169983306],
        },
    },
    ColNames.DIF_HOR_RAD: {
        ColNames.NAME: "Diffuse horizontal radiation",
        ColNames.COLOR: [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        UnitSystem.SI: {
            ColNames.UNIT: "Wh/m<sup>2</sup>",
            ColNames.RANGE: [0, 1200],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "Btu/ft<sup>2</sup>",
            ColNames.RANGE: [0, 1200 * 0.3169983306],
        },
    },
    ColNames.GLOB_HOR_ILL: {
        ColNames.NAME: "Global horizontal illuminance",
        ColNames.COLOR: ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],
        UnitSystem.SI: {
            ColNames.UNIT: "lux",
            ColNames.RANGE: [0, 120000],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "fc",
            ColNames.RANGE: [0, 120000 * 0.0929],
        },
    },
    ColNames.DIR_NOR_ILL: {
        ColNames.NAME: "Direct normal illuminance",
        ColNames.COLOR: ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],
        UnitSystem.SI: {
            ColNames.UNIT: "lux",
            ColNames.RANGE: [0, 120000],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "fc",
            ColNames.RANGE: [0, 120000 * 0.0929],
        },
    },
    ColNames.DIF_HOR_ILL: {
        ColNames.NAME: "Diffuse horizontal illuminance",
        ColNames.COLOR: ["#4d6daa", "#a0beed", "#f1e969", "#eb7d05", "#d81600"],
        UnitSystem.SI: {
            ColNames.UNIT: "lux",
            ColNames.RANGE: [0, 120000],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "fc",
            ColNames.RANGE: [0, 120000 * 0.0929],
        },
    },
    ColNames.ZLUMI: {
        ColNames.NAME: "Zenith luminance",
        ColNames.COLOR: [
            "#730a8c",
            "#0d0db3",
            "#0f85be",
            "#0f85be",
            "#b11421",
            "#fdf130",
        ],
        UnitSystem.SI: {
            ColNames.UNIT: "cd/m<sup>2</sup>",
            ColNames.RANGE: [0, 60000],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "cd/ft<sup>2</sup>",
            ColNames.RANGE: [0, 60000 * 0.0929],
        },
    },
    ColNames.WIND_DIR: {
        ColNames.NAME: "Wind direction",
        ColNames.COLOR: ["#0072dd", "#00c420", "#eded00", "#be00d5", "#0072dd"],
        UnitSystem.SI: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [0, 360],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [0, 360],
        },
    },
    ColNames.WIND_SPEED: {
        ColNames.NAME: "Wind speed",
        ColNames.COLOR: [
            "#D3D3D3",
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
        UnitSystem.SI: {
            ColNames.UNIT: "m/s",
            ColNames.RANGE: [0, 20],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "fpm",
            ColNames.RANGE: [0, 20 * 196.85039370078738],
        },
    },
    ColNames.TOT_SKY_COVER: {
        ColNames.NAME: "Total sky cover",
        ColNames.COLOR: cloud_colors,
        UnitSystem.SI: {
            ColNames.UNIT: "tenths",
            ColNames.RANGE: [0, 10],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "tenths",
            ColNames.RANGE: [0, 10],
        },
    },
    ColNames.OSKYCOVER: {
        ColNames.NAME: "Opaque sky cover",
        ColNames.COLOR: cloud_colors,
        UnitSystem.SI: {
            ColNames.UNIT: "tenths",
            ColNames.RANGE: [0, 10],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "tenths",
            ColNames.RANGE: [0, 10],
        },
    },
    ColNames.VIS: {
        ColNames.NAME: "Visibility",
        ColNames.COLOR: cloud_colors,
        UnitSystem.SI: {
            ColNames.UNIT: "km",
            ColNames.RANGE: [0, 100],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "miles",
            ColNames.RANGE: [0, 100 * 0.6215],
        },
    },
    ColNames.APPARENT_ZENITH: {
        ColNames.NAME: "Apparent zenith",
        ColNames.COLOR: [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        UnitSystem.SI: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [0, 180],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [0, 180],
        },
    },
    ColNames.ZENITH: {
        ColNames.NAME: "Zenith",
        ColNames.COLOR: [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        UnitSystem.SI: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [0, 180],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [0, 180],
        },
    },
    ColNames.APPARENT_ELEVATION: {
        ColNames.NAME: "Apparent elevation",
        ColNames.COLOR: [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        UnitSystem.SI: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [-90, 90],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [-90, 90],
        },
    },
    ColNames.ELEVATION: {
        ColNames.NAME: "Elevation",
        ColNames.COLOR: [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        UnitSystem.SI: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [-90, 90],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [-90, 90],
        },
    },
    ColNames.AZIMUTH: {
        ColNames.NAME: "Azimuth",
        ColNames.COLOR: [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        UnitSystem.SI: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [0, 360],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [0, 360],
        },
    },
    ColNames.EQUATION_OF_TIME: {
        ColNames.NAME: "Equation of time",
        ColNames.COLOR: [
            "#293a59",
            "#960c2c",
            "#ff0000",
            "#ff7b00",
            "#fffc00",
            "#ffff7b",
            "#ffffff",
        ],
        UnitSystem.SI: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [-20, 20],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°deg",
            ColNames.RANGE: [-20, 20],
        },
    },
    ColNames.UTCI_SUN_WIND: {
        ColNames.NAME: "UTCI: Sun & Wind",
        ColNames.COLOR: ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        UnitSystem.SI: {
            ColNames.UNIT: "°C",
            ColNames.RANGE: [-70, 70],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°F",
            ColNames.RANGE: [-94, 158],
        },
    },
    ColNames.UTCI_NO_SUN_WIND: {
        ColNames.NAME: "UTCI: no Sun & Wind",
        ColNames.COLOR: ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        UnitSystem.SI: {
            ColNames.UNIT: "°C",
            ColNames.RANGE: [-70, 70],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°F",
            ColNames.RANGE: [-94, 158],
        },
    },
    ColNames.UTCI_SUN_NO_WIND: {
        ColNames.NAME: "UTCI: Sun & no Wind",
        ColNames.COLOR: ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        UnitSystem.SI: {
            ColNames.UNIT: "°C",
            ColNames.RANGE: [-70, 70],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°F",
            ColNames.RANGE: [-94, 158],
        },
    },
    ColNames.UTCI_NO_SUN_NO_WIND: {
        ColNames.NAME: "UTCI: no Sun & no Wind",
        ColNames.COLOR: ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        UnitSystem.SI: {
            ColNames.UNIT: "°C",
            ColNames.RANGE: [-70, 70],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°F",
            ColNames.RANGE: [-94, 158],
        },
    },
    ColNames.UTCI_SUN_WIND_CATEGORIES: {
        ColNames.NAME: "UTCI: Sun & Wind : categories",
        ColNames.COLOR: [
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
        UnitSystem.SI: {
            ColNames.UNIT: thermal_stress_label,
            ColNames.RANGE: [-5, 4],
        },
        UnitSystem.IP: {
            ColNames.UNIT: thermal_stress_label,
            ColNames.RANGE: [-5, 4],
        },
    },
    ColNames.UTCI_NOSUN_WIND_CATEGORIES: {
        ColNames.NAME: "UTCI: no Sun & Wind : categories",
        ColNames.COLOR: [
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
        UnitSystem.SI: {
            ColNames.UNIT: thermal_stress_label,
            ColNames.RANGE: [-5, 4],
        },
        UnitSystem.IP: {
            ColNames.UNIT: thermal_stress_label,
            ColNames.RANGE: [-5, 4],
        },
    },
    ColNames.UTCI_SUN_NOWIND_CATEGORIES: {
        ColNames.NAME: "UTCI: Sun & no Wind : categories",
        ColNames.COLOR: [
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
        UnitSystem.SI: {
            ColNames.UNIT: thermal_stress_label,
            ColNames.RANGE: [-5, 4],
        },
        UnitSystem.IP: {
            ColNames.UNIT: thermal_stress_label,
            ColNames.RANGE: [-5, 4],
        },
    },
    ColNames.UTCI_NOSUN_NOWIND_CATEGORIES: {
        ColNames.NAME: "UTCI: no Sun & no Wind : categories",
        ColNames.COLOR: [
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
        UnitSystem.SI: {
            ColNames.UNIT: thermal_stress_label,
            ColNames.RANGE: [-5, 4],
        },
        UnitSystem.IP: {
            ColNames.UNIT: thermal_stress_label,
            ColNames.RANGE: [-5, 4],
        },
    },
    ColNames.P_VAP: {
        ColNames.NAME: "Vapor partial pressure",
        ColNames.COLOR: ["#ffe600", "#00c8ff", "#0000ff"],
        UnitSystem.SI: {
            ColNames.UNIT: "Pa",
            ColNames.RANGE: [0, 5000],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "Psi",
            ColNames.RANGE: [0, 5000 * 0.000145038],
        },
    },
    ColNames.P_SAT: {
        ColNames.NAME: "Saturation pressure",
        UnitSystem.SI: {
            ColNames.UNIT: "Pa",
            ColNames.RANGE: [0, 5000],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "Psi",
            ColNames.RANGE: [0, 5000 * 0.000145038],
        },
    },
    ColNames.HR: {
        ColNames.NAME: "Absolute humidity",
        ColNames.COLOR: ["#ffe600", "#00c8ff", "#0000ff"],
        UnitSystem.SI: {
            ColNames.UNIT: "g water/kg dry air",
            ColNames.RANGE: [0, 0.03 * 1000],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "lb water/klb dry air",
            ColNames.RANGE: [0, 0.03 * 1000],
        },
    },
    ColNames.T_WB: {
        ColNames.NAME: "Wet bulb temperature",
        ColNames.COLOR: ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        UnitSystem.SI: {
            ColNames.UNIT: "°C",
            ColNames.RANGE: [-40, 50],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°F",
            ColNames.RANGE: [-40, 122],
        },
    },
    ColNames.T_DP: {
        ColNames.NAME: "Dew point temperature",
        ColNames.COLOR: ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        UnitSystem.SI: {
            ColNames.UNIT: "°C",
            ColNames.RANGE: [-40, 50],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "°F",
            ColNames.RANGE: [-40, 122],
        },
    },
    ColNames.EH: {
        ColNames.NAME: "Enthalpy",
        ColNames.COLOR: ["#00b3ff", "#000082", "#ff0000", "#ffff00"],
        UnitSystem.SI: {
            ColNames.UNIT: "J/kg dry air",
            ColNames.RANGE: [0, 110000],
        },
        UnitSystem.IP: {
            ColNames.UNIT: "Btu/lb dry air",
            ColNames.RANGE: [0, 110000 * 0.000429923],
        },
    },
}

# Dropdown Names
variables_sun_cloud_tab_dropdown = [
    ColNames.NONE,
    ColNames.T_WB,
    ColNames.DPT,
    ColNames.DBT,
    ColNames.RH,
    ColNames.P_VAP,
    ColNames.HR,
    ColNames.EXTR_HOR_RAD,
    ColNames.HOR_IR_RAD,
    ColNames.GLOB_HOR_RAD,
    ColNames.DIR_NOR_RAD,
    ColNames.DIF_HOR_RAD,
    ColNames.GLOB_HOR_ILL,
    ColNames.DIR_NOR_ILL,
    ColNames.DIF_HOR_ILL,
    ColNames.ZLUMI,
    ColNames.WIND_DIR,
    ColNames.WIND_SPEED,
    ColNames.TOT_SKY_COVER,
    ColNames.OSKYCOVER,
    ColNames.VIS,
]
variables_dropdown = [
    ColNames.T_WB,
    ColNames.DPT,
    ColNames.DBT,
    ColNames.RH,
    ColNames.P_VAP,
    ColNames.HR,
    ColNames.EXTR_HOR_RAD,
    ColNames.HOR_IR_RAD,
    ColNames.GLOB_HOR_RAD,
    ColNames.DIR_NOR_RAD,
    ColNames.DIF_HOR_RAD,
    ColNames.GLOB_HOR_ILL,
    ColNames.DIR_NOR_ILL,
    ColNames.DIF_HOR_ILL,
    ColNames.ZLUMI,
    ColNames.WIND_DIR,
    ColNames.WIND_SPEED,
    ColNames.TOT_SKY_COVER,
    ColNames.OSKYCOVER,
    ColNames.VIS,
]
variables_more_variables_dropdown = [
    ColNames.UTCI_SUN_WIND,
    ColNames.UTCI_NO_SUN_WIND,
    ColNames.UTCI_SUN_NO_WIND,
    ColNames.UTCI_NO_SUN_NO_WIND,
    ColNames.UTCI_SUN_WIND_CATEGORIES,
    ColNames.UTCI_NOSUN_WIND_CATEGORIES,
    ColNames.UTCI_SUN_NOWIND_CATEGORIES,
    ColNames.UTCI_NOSUN_NOWIND_CATEGORIES,
    ColNames.T_DP,
    ColNames.ELEVATION,
    ColNames.AZIMUTH,
    ColNames.P_SAT,
]
variables_sun_cloud_tab_explore_dropdown = [
    ColNames.EXTR_HOR_RAD,
    ColNames.HOR_IR_RAD,
    ColNames.GLOB_HOR_RAD,
    ColNames.DIR_NOR_RAD,
    ColNames.DIF_HOR_RAD,
    ColNames.GLOB_HOR_ILL,
    ColNames.DIR_NOR_ILL,
    ColNames.DIF_HOR_ILL,
    ColNames.ZLUMI,
    ColNames.OSKYCOVER,
]
variables_outdoor_dropdown = [
    ColNames.UTCI_SUN_WIND,
    ColNames.UTCI_SUN_NO_WIND,
    ColNames.UTCI_NO_SUN_WIND,
    ColNames.UTCI_NO_SUN_NO_WIND,
]

sun_cloud_tab_dropdown_names = {
    mapping_dictionary[key][ColNames.NAME]: key
    for key in variables_sun_cloud_tab_dropdown
}

dropdown_names = {
    mapping_dictionary[key][ColNames.NAME]: key for key in variables_dropdown
}

more_variables_dropdown = {
    mapping_dictionary[key][ColNames.NAME]: key
    for key in variables_more_variables_dropdown
}

sun_cloud_tab_explore_dropdown_names = {
    mapping_dictionary[key][ColNames.NAME]: key
    for key in variables_sun_cloud_tab_explore_dropdown
}

outdoor_dropdown_names = {
    mapping_dictionary[key][ColNames.NAME]: key for key in variables_outdoor_dropdown
}
