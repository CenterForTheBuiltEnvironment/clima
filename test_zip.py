import urllib
import requests, zipfile, io

zip_url = 'http://climate.onebuilding.org/WMO_Region_4_North_and_Central_America/USA_United_States_of_America/CA_California/USA_CA_Oakland.Intl.AP.724930_TMY3.zip'

request = requests.get(zip_url)
zf = zipfile.ZipFile(io.BytesIO(request.content))
# Go through each file in zip file and find the epw file
for i in zf.namelist():
    if i[-3:] == 'epw':
        epw_name = i
data = zf.read(epw_name)
print(data)
