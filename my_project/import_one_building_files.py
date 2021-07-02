import pandas as pd
from my_project.utils import code_timer
import re


@code_timer
def import_kml_files(file_name):
    with open(f"./assets/data/{file_name}.kml", encoding="utf8") as data:
        text = data.read()

    locations = re.findall(r"<Placemark>[\s\S]*?<\/Placemark>", text)

    data = []
    for location in locations:
        # print(location)
        location_info = []
        # lat
        location_info.append(
            re.findall(r"<coordinates>(.+?)<\/coordinates>", location)[0].split(",")[0]
        )
        # long
        location_info.append(
            re.findall(r"<coordinates>(.+?)<\/coordinates>", location)[0].split(",")[1]
        )
        # name
        location_info.append(re.findall(r"<name>(.+?)<\/name>", location)[0])
        # url
        location_info.append(
            "<a href="
            + re.findall(r"<td>URL (.+?)<\/td>", location)[0]
            + ' style="color: #fff">Climate.OneBuilding.Org</a>'
        )

        data.append(location_info)

    df = pd.DataFrame(data, columns=["lon", "lat", "name", "Source"])

    try:
        df_old = pd.read_csv(f"./assets/data/one_building.csv")
        df_old = df_old.append(df).drop_duplicates()
        df_old.to_csv(f"./assets/data/one_building.csv", index=False)
    except FileNotFoundError:
        df.to_csv(f"./assets/data/one_building.csv", index=False)


if __name__ == "__main__":

    import_kml_files("Region1_Africa_EPW_Processing_locations")
    import_kml_files("Region7_Antarctica_EPW_Processing_locations")
    import_kml_files("Region3_South_America_EPW_Processing_locations")
    import_kml_files("Region2_Region6_Russia_EPW_Processing_locations")
    import_kml_files("Region2_Asia_EPW_Processing_locations")
    import_kml_files("Region4_CaliforniaClimateZones_EPW_Processing_locations")
    import_kml_files("Region4_NA_CA_Caribbean_EPW_Processing_locations")
    import_kml_files("Region4_USA_EPW_Processing_locations")
    import_kml_files("Region4_Canada_EPW_Processing_locations")
    import_kml_files("Region6_Europe_EPW_Processing_locations")
    import_kml_files("Region5_Southwest_Pacific_EPW_Processing_locations")
