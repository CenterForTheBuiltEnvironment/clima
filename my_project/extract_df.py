import io
import zipfile
from datetime import datetime, time, timedelta, timezone
from urllib.request import Request, urlopen

import pandas as pd
import requests
from pvlib import solarposition

default_url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw"

def get_data(url):
    """ Return a list of the data from api call. 
    """
    if url[-3:] == "zip" or url[-3:] == "all":
        request = requests.get(url)
        zf = zipfile.ZipFile(io.BytesIO(request.content))
        for i in zf.namelist():
            if i[-3:] == 'epw':
                epw_name = i
        data = zf.read(epw_name)
        data = repr(data).split("\\n")
        return data
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers = headers)
    epw = urlopen(req).read().decode()
    lines = epw.split("\n")
    return lines

def create_df(default_url):
    """ Extract and clean the data. Return a pandas data from a url. 
    """
    lst = get_data(default_url)
    meta = lst[0].strip().split(',')
    city = meta[1]
    country = meta[3]
    latitude = float(meta[-4])
    longitude = float(meta[-3])
    time_zone = float(meta[-2])
    site_elevation = meta[-1]
    location_name = (city + ", " + country)

    lst = lst[8:len(lst) - 1]
    lst = [line.strip().split(',') for line in lst]

    # Each data row exlude index 4 and 5, and everything afterdayssnow
    for line in lst:
        del line[4:6]
        del line[9]
        del line[-1]
        del line[-1]
        del line[-1]

    col_names = ['year', 'month', 'day', 'hour', 'DBT', 'DPT', 'RH', 
                'Apressure', 'EHrad', 'HIRrad', 'GHrad',
                'DNrad', 'DifHrad', 'GHillum', 'DNillum', 'DifHillum',
                'Zlumi', 'Wdir', 'Wspeed', 'Tskycover', 'Oskycover',
                'Vis', 'Cheight', 'PWobs', 'PWcodes', 'Pwater',
                'AsolOptD', 'SnowD', 'DaySSnow']

    epw_df = pd.DataFrame(columns = col_names, data = lst)

    # Add fake_year
    epw_df['fake_year'] = 'year'

    # Add in month names 
    month_look_up = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May',
            '6': 'Jun', '7': 'Jul', '8': 'Aug', '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    epw_df['month_names'] = epw_df['month'].apply(lambda x: month_look_up[x])

    # Add in DOY
    def doy_helper(row):
        """ Helper function for the DOY column.
        """
        month = int(row['month'])
        year = int(row['year'])
        day = int(row['day'])
        period = pd.Period(day = day, month = month, year = year, freq = 'D')
        return period.dayofyear

    epw_df['DOY'] = epw_df.apply(lambda row: doy_helper(row), axis = 1)

    # Change to int type
    change_to_int = ['year', 'day', 'month', 'hour']
    for col in change_to_int:
        epw_df[col] = epw_df[col].astype(int)

    # Change to float type 
    change_to_float = ['DBT', 'DPT', 'RH', 'Apressure', 'EHrad', 'HIRrad', 'GHrad', 
    'DNrad', 'DifHrad', 'GHillum', 'DNillum', 'DifHillum', 'Zlumi', 'Wdir', 'Wspeed', 'Tskycover',
    'Oskycover', 'Vis', 'Cheight', 'PWobs', 'PWcodes', 'Pwater', 'AsolOptD', 'SnowD', 'DaySSnow']
    for col in change_to_float:
        epw_df[col] = epw_df[col].astype(float)

    # Add in times df 
    date = datetime(2000, 6, 21, 12 - 1, 0, 0, 0, tzinfo = timezone.utc)
    tz = timedelta(days = 0, hours = time_zone - 1, minutes = 0)
    date = date - tz
    tz = 'UTC'
    times = pd.date_range(
                '2019-01-01 00:00:00', 
                '2020-01-01', 
                closed = 'left',
                freq = 'H', 
                tz = tz
            )
    delta = timedelta(days = 0, hours = time_zone - 1, minutes = 0)
    times = times - delta
    times_df = pd.DataFrame(times, columns = ['times'])
    epw_df = pd.concat([epw_df, times_df], axis = 1)
    epw_df.set_index("times", drop = False, append = False, inplace = True, verify_integrity = False)

    # Add in solpos df
    solpos = solarposition.get_solarposition(times, latitude, longitude)
    epw_df = pd.concat([epw_df, solpos], axis = 1)

    return epw_df, meta


