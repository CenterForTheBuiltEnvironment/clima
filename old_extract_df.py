from urllib.request import Request, urlopen
import pandas as pd

def create_df(url):
    """ Return the dataframe from the url and the location name. 
    """
    location_name = create_columns(get_data(url))
    epw_df = pd.DataFrame(
        {
            "year": year,
            "fake_year": fake_year,
            "DOY": DOY,
            "month": month,
            "month_names_long": month_names_long,
            "day": day,
            "hour": hour,
            "DBT": DBT,
            "DPT": DPT,
            "RH": RH,
            "Apressure": Apressure,
            "EHrad": EHrad,
            "HIRrad": HIRrad,
            "GHrad": GHrad,
            "DNrad": DNrad,
            "DifHrad": DifHrad,
            "GHillum": GHillum,
            "DNillum": DNillum,
            "DifHillum": DifHillum,
            "Zlumi": Zlumi,
            "Wdir": Wdir,
            "Wspeed": Wspeed,
            "Tskycover": Tskycover,
            "Oskycover": Oskycover,
            "Vis": Vis,
            "Cheight": Cheight,
            "PWobs": PWobs,
            "PWcodes": PWcodes,
            "Pwater": Pwater,
            "AsolOptD": AsolOptD,
            "SnowD": SnowD,
            "DaySSnow": DaySSnow
        }
    )
    return epw_df, location_name

def create_columns(lines):
    """ Populate the column lists.
    """
    for i, line in enumerate(lines):
        # read header and site info
        if i == 0: 
            line = line.strip()
            line01 = line.split(',')

            City = line01[1]
            Country = line01[3]
            latitude = float(line01[-4])
            longitude = float(line01[-3])
            time_zone = float(line01[-2])
            site_elevation = line01[-1]

            station = City + '_' + Country
            location = 'Location: ' + City + '_' + Country + ', Latitude:' + str(latitude) + ', Longitude:' + str(longitude) + ', Time Zone:' + str(time_zone) + ', ' + site_elevation + 'm above sea level'

        # Read all the individual data columns in the weather file
        elif i > 7 and i - 7 <= 8760: 
            epwdata = line.strip().split(",")
            
            year.append(int(epwdata[0]))
            day.append(int(epwdata[2]))
            month.append(int(epwdata[1]))
            hour.append(int(epwdata[3]))
            DBT.append(float(epwdata[6]))
            DPT.append(float(epwdata[7]))
            RH.append(float(epwdata[8]))
            Apressure.append(float(epwdata[9]))
            EHrad.append(float(epwdata[10]))
            EDNrad.append(float(epwdata[11]))
            HIRrad.append(float(epwdata[12]))
            GHrad.append(float(epwdata[13]))
            DNrad.append(float(epwdata[14]))
            DifHrad.append(float(epwdata[15]))
            GHillum.append(float(epwdata[16]))
            DNillum.append(float(epwdata[17]))
            DifHillum.append(float(epwdata[18]))
            Zlumi.append(float(epwdata[19]))
            Wdir.append(float(epwdata[20]))
            Wspeed.append(float(epwdata[21]))
            Tskycover.append(float(epwdata[22]))
            Oskycover.append(float(epwdata[23]))
            Vis.append(float(epwdata[24]))
            Cheight.append(float(epwdata[25]))
            PWobs.append(float(epwdata[26]))
            PWcodes.append(float(epwdata[27]))
            Pwater.append(float(epwdata[28]))
            AsolOptD.append(float(epwdata[29]))
            SnowD.append(float(epwdata[30]))
            DaySSnow.append(float(epwdata[31]))

    month_names = ["Jan", "Feb","Mar","Apr","May","Jun", "Jul", "Aug","Sep","Oct","Nov","Dec"]
    doy = 1
    for i, h in enumerate(hour):
        DOY.append(doy)
        fake_year.append("year")
        month_names_long.append(month_names[month[i]-1])
        if h == 24:
            doy += 1
    location_name = (City + ", " + Country)
    return location_name

def get_data(url):
    """ Return a list of the data from api call. 
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers = headers)
    epw = urlopen(req).read().decode()
    lines = epw.split("\n")
    return lines

year = []
month = []
day = []
hour = []
DBT = []
DPT = []
RH = []
Apressure = []
EHrad = []
EDNrad = []
HIRrad = []
GHrad = []
DNrad = []
DifHrad = []
GHillum = []
DNillum = []
DifHillum = []
Zlumi = []
Wdir = []
Wspeed = []
Tskycover = []
Oskycover = []
Vis = []
Cheight = []
PWobs = []
PWcodes = []
Pwater = []
AsolOptD = []
SnowD = []
DaySSnow = []
month_names_long = []
DOY = []
fake_year = []

 