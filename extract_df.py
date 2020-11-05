from urllib.request import Request, urlopen
import pandas as pd

default_url = "https://energyplus.net/weather-download/north_and_central_america_wmo_region_4/USA/CA/USA_CA_Oakland.Intl.AP.724930_TMY/USA_CA_Oakland.Intl.AP.724930_TMY.epw"

def get_data(url):
    """ Return a list of the data from api call. 
    """
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
    location_name = (city + ", " + country)

    lst = lst[8:len(lst) - 1]
    lst = [line.strip().split(',') for line in lst]

    # Each data row exlude index 4 and 5, and everything afterdayssnow
    for line in lst:
        del line[4:6]
        del line[-1]
        del line[-1]
        del line[-1]

    col_names = ['year', 'month', 'day', 'hour', 'DBT', 'DPT', 'RH', 
                'Apressure', 'EHrad', 'EDNrad', 'HIRrad', 'GHrad',
                'DNrad', 'DifHrad', 'GHillum', 'DNillum', 'DifHillum',
                'Zlumi', 'Wdir', 'Wspeed', 'Tskycover', 'Oskycover',
                'Vis', 'Cheight', 'PWobs', 'PWcodes', 'Pwater',
                'AsolOptD', 'SnowD', 'DaySSnow']

    epw_df = pd.DataFrame(columns = col_names, data = lst)

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
    epw_df['year'] = epw_df['year'].astype(int)
    epw_df['day'] = epw_df['day'].astype(int)
    epw_df['month'] = epw_df['month'].astype(int)
    epw_df['hour'] = epw_df['hour'].astype(int)

    # Change to float type 
    epw_df['DBT'] = epw_df['DBT'].astype(float)
    epw_df['DPT'] = epw_df['DPT'].astype(float)
    epw_df['RH'] = epw_df['RH'].astype(float)
    epw_df['Apressure'] = epw_df['Apressure'].astype(float)
    epw_df['EHrad'] = epw_df['EHrad'].astype(float)
    epw_df['EDNrad'] = epw_df['EDNrad'].astype(float)
    epw_df['HIRrad'] = epw_df['HIRrad'].astype(float)
    epw_df['GHrad'] = epw_df['GHrad'].astype(float)
    epw_df['DNrad'] = epw_df['DNrad'].astype(float)
    epw_df['DifHrad'] = epw_df['DifHrad'].astype(float)
    epw_df['GHillum'] = epw_df['GHillum'].astype(float)
    epw_df['DNillum'] = epw_df['DNillum'].astype(float)
    epw_df['DifHillum'] = epw_df['DifHillum'].astype(float)
    epw_df['Zlumi'] = epw_df['Zlumi'].astype(float)
    epw_df['Wdir'] = epw_df['Wdir'].astype(float)
    epw_df['Wspeed'] = epw_df['Wspeed'].astype(float)
    epw_df['Tskycover'] = epw_df['Tskycover'].astype(float)
    epw_df['Oskycover'] = epw_df['Oskycover'].astype(float)
    epw_df['Vis'] = epw_df['Vis'].astype(float)
    epw_df['Cheight'] = epw_df['Cheight'].astype(float)
    epw_df['PWobs'] = epw_df['PWobs'].astype(float)
    epw_df['PWcodes'] = epw_df['PWcodes'].astype(float)
    epw_df['Pwater'] = epw_df['Pwater'].astype(float)
    epw_df['AsolOptD'] = epw_df['AsolOptD'].astype(float)
    epw_df['SnowD'] = epw_df['SnowD'].astype(float)
    epw_df['DaySSnow'] = epw_df['DaySSnow'].astype(float)

    return epw_df, meta


# month_names_long, fake_year 
# because in og code months_name_long is same as month_names
# and fake year is just a string 'year'
