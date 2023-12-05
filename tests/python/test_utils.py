import requests

from my_project.utils import summary_table_tmp_rh_tab
from my_project.extract_df import get_data, create_df
import pandas as pd
import os


def save_epw_test(path_file):
    test_url = "http://climate.onebuilding.org/WMO_Region_6_Europe/ITA_Italy/ER_Emilia-Romagna/ITA_ER_Bologna-Marconi.AP.161400_TMYx.2004-2018.zip"

    lines = get_data(source_url=test_url)
    df, _ = create_df(lst=lines, file_name=test_url)

    df.to_pickle(path_file, compression="gzip")


def import_epw_test():
    epw_test_file_path = "epw_test.pkl"

    if not os.path.isfile(epw_test_file_path):
        save_epw_test(path_file=epw_test_file_path)

    return pd.read_pickle(epw_test_file_path, compression="gzip")


def test_summary_table_tmp_rh_tab():
    try:
        # check tha the climate.onebuilding website is on
        print(requests.get("https://climate.onebuilding.org", timeout=2))
        df = import_epw_test()
        data_table = summary_table_tmp_rh_tab(df, "RH", "si")

        assert data_table.data[0]["month"] == "Jan"
    except requests.exceptions.ConnectionError:
        pass
