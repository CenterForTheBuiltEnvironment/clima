import io
import json
import math
import re
import zipfile
from datetime import timedelta
from urllib.request import Request, urlopen
from functools import lru_cache

import logging
import numpy as np
import pandas as pd
import requests
from pvlib import solarposition
from pythermalcomfort import psychrometrics as psy
from pythermalcomfort.models import adaptive_ashrae
from pythermalcomfort.models import solar_gain
from pythermalcomfort.models import utci
from pythermalcomfort.utilities import running_mean_outdoor_temperature
from config import UnitSystem
from pages.lib.global_scheme import month_lst
from pages.lib.utils import code_timer
from pages.lib.global_variables import Variables, VariableInfo


@code_timer
def get_data(source_url):
    """Return a list of the data from api call."""
    if source_url[-3:] == "zip" or source_url[-3:] == "all":
        request = requests.get(source_url)
        if request.status_code != 404:
            zf = zipfile.ZipFile(io.BytesIO(request.content))
            for i in zf.namelist():
                if i[-3:] == "epw":
                    epw_name = i
                    data = zf.read(epw_name)
                    data = repr(data).split("\\n")
                    return data
        else:
            print("returning none")
            return None
    else:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            req = Request(source_url, headers=headers)
            epw = urlopen(req).read().decode()
            return epw.split("\n")
        except Exception as e:
            logging.error(f"Failed to fetch EPW data: {e}")
            return None


@lru_cache(maxsize=64)
def get_global_temp_range(location: str, col_name: str) -> tuple[float, float]:
    df_all = get_data(location)  # Take the full-year data
    series = df_all[col_name].replace([np.inf, -np.inf], np.nan).dropna()
    return float(series.min()), float(series.max())


@code_timer
def get_location_info(lst, file_name):
    """Extract and clean the data. Return a pandas data from a url."""
    meta = lst[0].strip().replace("\\r", "").split(",")

    location_info = {
        "url": file_name,
        "lat": float(meta[-4]),
        "lon": float(meta[-3]),
        "time_zone": float(meta[-2]),
        "site_elevation": meta[-1],
        "city": meta[1],
        "state": meta[2],
        "country": meta[3],
        "period": None,
    }

    # from OneClimaBuilding files extract info about reference years
    try:
        location_info[Variables.PERIOD.col_name] = re.search(
            r'cord=[\'"]?([^\'" >]+);', lst[5]
        ).group(1)
    except AttributeError:
        pass

    return location_info


# ==== Unified UTCI computation and binning ====
UTCI_BINS = [-999, -40, -27, -13, 0, 9, 26, 32, 38, 46, 999]
UTCI_LABELS = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]


def utci_calc(
    df: pd.DataFrame,
    t_air_col: str,
    t_rad_col: str,
    wind_col: str,
    rh_col: str = Variables.RH.col_name,
) -> pd.Series:
    """Call utci() using values from df columns."""
    return utci(df[t_air_col], df[t_rad_col], df[wind_col], df[rh_col])


def add_utci_variants(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate the four UTCI variants:
      - noSun_Wind   : DBT + DBT + wind_speed_utci
      - noSun_noWind : DBT + DBT + wind_speed_utci_0
      - Sun_Wind     : DBT + MRT + wind_speed_utci
      - Sun_noWind   : DBT + MRT + wind_speed_utci_0
    """
    recipes = {
        Variables.UTCI_NO_SUN_WIND.col_name: (
            Variables.DBT.col_name,
            Variables.DBT.col_name,
            Variables.WIND_SPEED_UTCI.col_name,
        ),
        Variables.UTCI_NO_SUN_NO_WIND.col_name: (
            Variables.DBT.col_name,
            Variables.DBT.col_name,
            Variables.WIND_SPEED_UTCI_0.col_name,
        ),
        Variables.UTCI_SUN_WIND.col_name: (
            Variables.DBT.col_name,
            Variables.MRT.col_name,
            Variables.WIND_SPEED_UTCI.col_name,
        ),
        Variables.UTCI_SUN_NO_WIND.col_name: (
            Variables.DBT.col_name,
            Variables.MRT.col_name,
            Variables.WIND_SPEED_UTCI_0.col_name,
        ),
    }
    for out_col, (t_air, t_rad, wind) in recipes.items():
        df[out_col] = utci_calc(df, t_air, t_rad, wind)
    return df


def add_utci_categories(df: pd.DataFrame) -> pd.DataFrame:
    """Bin the four UTCI columns into categories."""
    mapping = {
        Variables.UTCI_NO_SUN_WIND.col_name: Variables.UTCI_NOSUN_WIND_CATEGORIES.col_name,
        Variables.UTCI_NO_SUN_NO_WIND.col_name: Variables.UTCI_NOSUN_NOWIND_CATEGORIES.col_name,
        Variables.UTCI_SUN_WIND.col_name: Variables.UTCI_SUN_WIND_CATEGORIES.col_name,
        Variables.UTCI_SUN_NO_WIND.col_name: Variables.UTCI_SUN_NOWIND_CATEGORIES.col_name,
    }
    for src_col, dst_col in mapping.items():
        df[dst_col] = pd.cut(x=df[src_col], bins=UTCI_BINS, labels=UTCI_LABELS)
    return df


@code_timer
def create_df(lst, file_name):
    """Extract and clean the data. Return a pandas data from a url."""
    meta = lst[0].strip().replace("\\r", "").split(",")

    location_info = {
        "url": file_name,
        "lat": float(meta[-4]),
        "lon": float(meta[-3]),
        "time_zone": float(meta[-2]),
        "site_elevation": meta[-1],
        "city": meta[1],
        "state": meta[2],
        "country": meta[3],
        "period": None,
    }

    # from OneClimaBuilding files extract info about reference years
    try:
        location_info[Variables.PERIOD.col_name] = re.search(
            r'cord=[\'"]?([^\'" >]+);', lst[5]
        ).group(1)
    except AttributeError:
        pass

    lst = lst[8:8768]
    lst = [line.strip().split(",") for line in lst]

    # Each data row exclude index 4 and 5, and everything after days now
    for line in lst:
        del line[4:6]
        del line[9]
        del line[-1]
        del line[-1]
        del line[-1]

    col_names = [
        Variables.YEAR.col_name,
        Variables.MONTH.col_name,
        Variables.DAY.col_name,
        Variables.HOUR.col_name,
        Variables.DBT.col_name,
        Variables.DPT.col_name,
        Variables.RH.col_name,
        Variables.P_ATM.col_name,
        Variables.EXTR_HOR_RAD.col_name,
        Variables.HOR_IR_RAD.col_name,
        Variables.GLOB_HOR_RAD.col_name,
        Variables.DIR_NOR_RAD.col_name,
        Variables.DIF_HOR_RAD.col_name,
        Variables.GLOB_HOR_ILL.col_name,
        Variables.DIR_NOR_ILL.col_name,
        Variables.DIF_HOR_ILL.col_name,
        Variables.ZLUMI.col_name,
        Variables.WIND_DIR.col_name,
        Variables.WIND_SPEED.col_name,
        Variables.TOT_SKY_COVER.col_name,
        Variables.OPAQUE_SKY_COVER.col_name,
        Variables.VIS.col_name,
        Variables.CLOUD_HEIGHT.col_name,
        Variables.PRECIPITATION_OBSERVATION.col_name,
        Variables.PRECIPITATION_CODES.col_name,
        Variables.PRECIPITATION_WATER.col_name,
        Variables.AEROSOL_OPTICAL_DEPTH.col_name,
        Variables.SNOW_DEPTH.col_name,
        Variables.DAILY_SNOW.col_name,
    ]

    # assign column names, if fewer cols are there than supposed assign 9999 to that col
    if len(lst[0]) < len(col_names):
        epw_df = pd.DataFrame(columns=col_names[: len(lst[0])], data=lst)
        for col in [x for ix, x in enumerate(col_names) if ix >= len(lst[0])]:
            epw_df[col] = 9999
    else:
        epw_df = pd.DataFrame(columns=col_names, data=lst)

    # from EnergyPlus files extract info about reference years
    if not location_info[Variables.PERIOD.col_name]:
        years = epw_df[Variables.YEAR.col_name].astype("int").unique()
        if len(years) == 1:
            year_rounded_up = int(math.ceil(years[0] / 10.0)) * 10
            location_info[Variables.PERIOD.col_name] = (
                f"{year_rounded_up - 10}-{year_rounded_up}"
            )
        else:
            min_year = int(math.floor(min(years) / 10.0)) * 10
            max_year = int(math.ceil(max(years) / 10.0)) * 10
            location_info[Variables.PERIOD.col_name] = f"{min_year}-{max_year}"

    # Add fake_year
    epw_df[Variables.FAKE_YEAR.col_name] = Variables.YEAR.col_name

    # Add in month names
    month_look_up = {ix + 1: month for ix, month in enumerate(month_lst)}
    epw_df[Variables.MONTH_NAMES.col_name] = (
        epw_df[Variables.MONTH.col_name].astype("int").map(month_look_up)
    )

    # Change to int type
    epw_df[
        [
            Variables.YEAR.col_name,
            Variables.DAY.col_name,
            Variables.MONTH.col_name,
            Variables.HOUR.col_name,
        ]
    ] = epw_df[
        [
            Variables.YEAR.col_name,
            Variables.DAY.col_name,
            Variables.MONTH.col_name,
            Variables.HOUR.col_name,
        ]
    ].astype(
        int
    )

    # Add in DOY
    df_doy = (
        epw_df.groupby([Variables.MONTH.col_name, Variables.DAY.col_name])[
            Variables.HOUR.col_name
        ]
        .count()
        .reset_index()
    )
    df_doy[Variables.DOY.col_name] = df_doy.index + 1
    epw_df = pd.merge(
        epw_df,
        df_doy[
            [Variables.MONTH.col_name, Variables.DAY.col_name, Variables.DOY.col_name]
        ],
        on=[Variables.MONTH.col_name, Variables.DAY.col_name],
        how="left",
    )

    change_to_float = [
        Variables.DBT.col_name,
        Variables.DPT.col_name,
        Variables.RH.col_name,
        Variables.P_ATM.col_name,
        Variables.EXTR_HOR_RAD.col_name,
        Variables.HOR_IR_RAD.col_name,
        Variables.GLOB_HOR_RAD.col_name,
        Variables.DIR_NOR_RAD.col_name,
        Variables.DIF_HOR_RAD.col_name,
        Variables.GLOB_HOR_ILL.col_name,
        Variables.DIR_NOR_ILL.col_name,
        Variables.DIF_HOR_ILL.col_name,
        Variables.ZLUMI.col_name,
        Variables.WIND_DIR.col_name,
        Variables.WIND_SPEED.col_name,
        Variables.TOT_SKY_COVER.col_name,
        Variables.OPAQUE_SKY_COVER.col_name,
        Variables.VIS.col_name,
        Variables.CLOUD_HEIGHT.col_name,
        Variables.PRECIPITATION_OBSERVATION.col_name,
        Variables.PRECIPITATION_CODES.col_name,
        Variables.PRECIPITATION_WATER.col_name,
        Variables.AEROSOL_OPTICAL_DEPTH.col_name,
        Variables.SNOW_DEPTH.col_name,
        Variables.DAILY_SNOW.col_name,
    ]
    epw_df[change_to_float] = epw_df[change_to_float].astype(float)

    # Add in times df
    times = pd.date_range(
        "2019-01-01 00:00:00", "2020-01-01", inclusive="left", freq="h", tz="UTC"
    )
    epw_df[Variables.UTC_TIME.col_name] = pd.to_datetime(times)
    delta = timedelta(
        days=0, hours=location_info[Variables.TIME_ZONE.col_name] - 1, minutes=0
    )
    times = times - delta
    epw_df[Variables.TIMES.col_name] = times
    epw_df.set_index(
        Variables.TIMES.col_name,
        drop=False,
        append=False,
        inplace=True,
        verify_integrity=False,
    )

    # Add in solar position df
    solar_position = solarposition.get_solarposition(
        times,
        location_info[Variables.LAT.col_name],
        location_info[Variables.LON.col_name],
    )
    epw_df = pd.concat([epw_df, solar_position], axis=1)

    # Add in UTCI
    sol_altitude = epw_df[Variables.ELEVATION.col_name].mask(
        epw_df[Variables.ELEVATION.col_name] <= 0, 0
    )
    sharp = expand_to_hours(45)
    sol_radiation_dir = epw_df[Variables.DIR_NOR_RAD.col_name]
    sol_transmittance = expand_to_hours(1)  # CHECK VALUE
    f_svv = expand_to_hours(1)  # CHECK VALUE
    f_bes = expand_to_hours(1)  # CHECK VALUE
    asw = expand_to_hours(0.7)  # CHECK VALUE
    posture = expand_to_hours("standing")
    floor_reflectance = expand_to_hours(0.6)  # EXPOSE AS A VARIABLE?

    mrt = np.vectorize(solar_gain)(
        sol_altitude,
        sharp,
        sol_radiation_dir,
        sol_transmittance,
        f_svv,
        f_bes,
        asw,
        posture,
        floor_reflectance,
    )
    mrt_df = pd.DataFrame.from_records(mrt)
    mrt_df[Variables.DELTA_MRT.col_name] = mrt_df[Variables.DELTA_MRT.col_name].mask(
        mrt_df[Variables.DELTA_MRT.col_name] >= 70, 70
    )
    mrt_df = mrt_df.set_index(epw_df.times)

    epw_df = epw_df.join(mrt_df)

    epw_df[Variables.MRT.col_name] = (
        epw_df[Variables.DELTA_MRT.col_name] + epw_df[Variables.DBT.col_name]
    )
    epw_df[Variables.WIND_SPEED_UTCI.col_name] = epw_df[Variables.WIND_SPEED.col_name]
    epw_df[Variables.WIND_SPEED_UTCI.col_name] = epw_df[
        Variables.WIND_SPEED_UTCI.col_name
    ].mask(epw_df[Variables.WIND_SPEED_UTCI.col_name] >= 17, 16.9)
    epw_df[Variables.WIND_SPEED_UTCI.col_name] = epw_df[
        Variables.WIND_SPEED_UTCI.col_name
    ].mask(epw_df[Variables.WIND_SPEED_UTCI.col_name] <= 0.5, 0.6)
    epw_df[Variables.WIND_SPEED_UTCI_0.col_name] = epw_df[
        Variables.WIND_SPEED_UTCI.col_name
    ].mask(epw_df[Variables.WIND_SPEED_UTCI.col_name] >= 0, 0.5)

    epw_df = add_utci_variants(epw_df)

    epw_df = add_utci_categories(epw_df)

    # Add psy values
    ta_rh = np.vectorize(psy.psy_ta_rh)(
        epw_df[Variables.DBT.col_name], epw_df[Variables.RH.col_name]
    )
    psy_df = pd.DataFrame.from_records(ta_rh)
    psy_df = psy_df.set_index(epw_df.times)
    epw_df = epw_df.join(psy_df)

    # calculate adaptive data
    dbt_day_ave = (
        epw_df.groupby([Variables.DOY.col_name])[Variables.DBT.col_name]
        .mean()
        .to_list()
    )
    n = 7
    epw_df[Variables.ADAPTIVE_COMFORT.col_name] = np.nan
    epw_df[Variables.ADAPTIVE_CMF_80_LOW.col_name] = np.nan
    epw_df[Variables.ADAPTIVE_CMF_80_UP.col_name] = np.nan
    epw_df[Variables.ADAPTIVE_CMF_90_LOW.col_name] = np.nan
    epw_df[Variables.ADAPTIVE_CMF_90_UP.col_name] = np.nan
    epw_df[Variables.ADAPTIVE_CMF_RMT.col_name] = np.nan
    for day in epw_df.DOY.unique():
        i = day - 1
        if i < n:
            last_days = dbt_day_ave[-n + i :] + dbt_day_ave[0:i]
        else:
            last_days = dbt_day_ave[i - n : i]
        last_days.reverse()
        rmt = running_mean_outdoor_temperature(last_days, alpha=0.9)

        if rmt > 40:
            rmt = 40.1
        elif rmt < 10:
            rmt = 9.9
        r = adaptive_ashrae(
            tdb=dbt_day_ave[i],
            tr=dbt_day_ave[i],
            t_running_mean=rmt,
            v=0.5,
            limit_inputs=False,
        )
        epw_df.loc[epw_df.DOY == day, Variables.ADAPTIVE_CMF_RMT.col_name] = rmt
        epw_df.loc[epw_df.DOY == day, Variables.ADAPTIVE_COMFORT.col_name] = r[
            Variables.TMP_CMF.col_name
        ]
        epw_df.loc[epw_df.DOY == day, Variables.ADAPTIVE_CMF_80_LOW.col_name] = r[
            Variables.TMP_CMF_80_LOW.col_name
        ]
        epw_df.loc[epw_df.DOY == day, Variables.ADAPTIVE_CMF_80_UP.col_name] = r[
            Variables.TMP_CMF_80_UP.col_name
        ]
        epw_df.loc[epw_df.DOY == day, Variables.ADAPTIVE_CMF_90_LOW.col_name] = r[
            Variables.TMP_CMF_90_LOW.col_name
        ]
        epw_df.loc[epw_df.DOY == day, Variables.ADAPTIVE_CMF_90_UP.col_name] = r[
            Variables.TMP_CMF_90_UP.col_name
        ]

    return epw_df, location_info


# convert function
def convert_SI_to_IP(df: pd.DataFrame, name: str) -> None:
    """Convert SI to IP based on column name."""
    if name not in df.columns:
        print(
            f"[convert_SI_to_IP] Column '{name}' not found in DataFrame. Skipping conversion."
        )
        return
    match name:
        case (
            Variables.DBT.col_name
            | Variables.DPT.col_name
            | Variables.T_WB.col_name
            | Variables.T_DP.col_name
            | Variables.UTCI_SUN_WIND.col_name
            | Variables.UTCI_NO_SUN_WIND.col_name
            | Variables.UTCI_SUN_NO_WIND.col_name
            | Variables.UTCI_NO_SUN_NO_WIND.col_name
            | Variables.ADAPTIVE_COMFORT.col_name
            | Variables.ADAPTIVE_CMF_80_LOW.col_name
            | Variables.ADAPTIVE_CMF_80_UP.col_name
            | Variables.ADAPTIVE_CMF_90_LOW.col_name
            | Variables.ADAPTIVE_CMF_90_UP.col_name
        ):
            df[name] = df[name] * 1.8 + 32

        case (
            Variables.P_ATM.col_name
            | Variables.P_VAP.col_name
            | Variables.P_SAT.col_name
        ):
            df[name] = df[name] * 0.000145038

        case (
            Variables.EXTR_HOR_RAD.col_name
            | Variables.HOR_IR_RAD.col_name
            | Variables.GLOB_HOR_RAD.col_name
            | Variables.DIR_NOR_RAD.col_name
            | Variables.DIF_HOR_RAD.col_name
        ):
            df[name] = df[name] * 0.3169983306

        case (
            Variables.GLOB_HOR_ILL.col_name
            | Variables.DIR_NOR_ILL.col_name
            | Variables.DIF_HOR_ILL.col_name
        ):
            df[name] = df[name] * 0.0929

        case Variables.ZLUMI.col_name:
            df[name] = df[name] * 0.0929

        case Variables.WIND_SPEED.col_name:
            df[name] = df[name] * 196.85039370078738

        case Variables.VIS.col_name:
            df[name] = df[name] * 0.6215

        case Variables.EH.col_name:
            df[name] = df[name] * 0.000429923

        case _:
            # No conversion needed for this column
            pass


def convert_df_units(df: pd.DataFrame, unit_system: str) -> pd.DataFrame:
    """Convert DataFrame columns to the specified unit system."""
    if unit_system != UnitSystem.IP:
        return df  # Currently we only support SI → IP

    df_converted = df.copy()

    for attr in dir(Variables):
        if attr.isupper():
            var = getattr(Variables, attr)
            if isinstance(var, VariableInfo):
                col = var.col_name
                convert_SI_to_IP(df_converted, col)

    return df_converted


def convert_data(df, mapping_json):
    mapping_dict = json.loads(mapping_json)
    for key in mapping_dict:
        convert_SI_to_IP(df, key)
    return mapping_json


def expand_to_hours(value: any, hours: int = 8760) -> list[any]:
    """Return a list with the input value repeated for a given number of hours.

    Args:
        value: The value to repeat.
        hours: Number of repetitions. Defaults to 8760 (hours in a year).

    Returns:
        A list containing the value repeated `hours` times.
    """
    return [value] * hours


if __name__ == "__main__":
    # fmt: off
    test_url = "https://www.energyplus.net/weather-download/europe_wmo_region_6/ITA//ITA_Bologna-Borgo.Panigale.161400_IGDG/all"
    other_url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw"
    # fmt: on

    # -----
    lines = get_data(source_url=test_url)
    df, location_data = create_df(lst=lines, file_name=test_url)
