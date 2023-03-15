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
        # description
        try:
            location_info.append(
                location.split("Period of Record=")[1].split("</td>")[0]
            )
        except IndexError:
            location_info.append("not available")
        try:
            location_info.append(location.split("Elevation <b>")[1].split("</b>")[0])
        except IndexError:
            location_info.append("not available")
        try:
            location_info.append(
                location.split("Time Zone {GMT <b>")[1].split("</b>")[0]
            )
        except IndexError:
            location_info.append("not available")
        try:
            location_info.append(
                location.split("99% Heating DB <b>")[1].split("</b>")[0]
            )
        except IndexError:
            location_info.append(None)
        try:
            location_info.append(
                location.split("1% Cooling DB <b>")[1].split("</b>")[0]
            )
        except IndexError:
            location_info.append(None)

        data.append(location_info)

    df = pd.DataFrame(
        data,
        columns=[
            "lon",
            "lat",
            "name",
            "Source",
            "period",
            "elevation (m)",
            "time zone (GMT)",
            "99% Heating DB",
            "1% Cooling DB ",
        ],
    )

    try:
        df_old = pd.read_csv(f"./assets/data/one_building.csv", compression="gzip")
        df_old = pd.concat([df_old, df]).drop_duplicates()
        df_old.to_csv(
            f"./assets/data/one_building.csv", index=False, compression="gzip"
        )
    except FileNotFoundError:
        df.to_csv(f"./assets/data/one_building.csv", index=False, compression="gzip")


if __name__ == "__main__":

    import os

    directory = os.fsencode("./assets/data/")

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".kml"):
            import_kml_files(filename)
