from utils import summary_table_tmp_rh_tab
from extract_df import get_data, create_df
import pandas as pd
import os


def save_epw_test(path_file):
    test_url = "http://climate.onebuilding.org/WMO_Region_6_Europe/ITA_Italy/ER_Emilia-Romagna/ITA_ER_Bologna-Marconi.AP.161400_TMYx.2004-2018.zip"

    lines = get_data(url=test_url)
    df, location_data = create_df(lst=lines, file_name=test_url)

    df.to_pickle(path_file, compression="gzip")


def import_epw_test():
    epw_test_file_path = "epw_test.pkl"

    if not os.path.isfile(epw_test_file_path):
        save_epw_test(path_file=epw_test_file_path)

    return pd.read_pickle(epw_test_file_path, compression="gzip")


def test_summary_table_tmp_rh_tab():
    df = import_epw_test()
    df_summary = summary_table_tmp_rh_tab(df, "RH")

    assert df_summary.iloc[0, 0] == "Jan"
    assert df_summary.iloc[0, 1] == 80.34


def test_solar_global_radiation():
    df = import_epw_test()

    assert df["GHrad"].sum() == 1546122.0
