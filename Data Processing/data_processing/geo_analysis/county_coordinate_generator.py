import urllib.request
import json
from geo_analysis.geo_constants import COUNTY_GEO_CODE_JSON_LINK, COUNTY_COORDINATES_FILE


def generate_county_coordinate():
    data = None
    with urllib.request.urlopen(COUNTY_GEO_CODE_JSON_LINK) as url:
        data = json.loads(url.read().decode())

    features = data["features"]
    count = 0
    f = open(COUNTY_COORDINATES_FILE, "w")
    f.write("county_coordinates = {")

    for feature in features:
        if feature["properties"]["STATE"] == "36":
            count += 1
            f.write("\"" + feature["properties"]["GEO_ID"] + "\": ")
            coord = feature["geometry"]["coordinates"][0]
            while type(coord[0][0]) is not float:
                coord = coord[0]
            f.write(str(coord))
            # New York State have 62 counties
            if count < 62:
                f.write(", ")

    f.write("}")


if __name__ == '__main__':
    generate_county_coordinate()
