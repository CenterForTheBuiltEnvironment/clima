import pandas as pd
from my_project.utils import code_timer
import re


@code_timer
def import_kml_files(file_name):
    with open(f"./assets/data/{file_name}", encoding="utf8", errors="ignore") as data:
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
        df_old = pd.concat([df_old, df]).drop_duplicates()
        df_old.to_csv(f"./assets/data/one_building.csv", index=False)
    except FileNotFoundError:
        df.to_csv(f"./assets/data/one_building.csv", index=False)


if __name__ == "__main__":

    import os

    directory = os.fsencode("./assets/data/")

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".kml"):
            import_kml_files(filename)
