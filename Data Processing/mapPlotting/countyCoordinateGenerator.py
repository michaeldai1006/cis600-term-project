import urllib.request, json

data = None
with urllib.request.urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as url:
    data = json.loads(url.read().decode())

features = data["features"]
count = 0
f = open("countyCoordinates.py", "w")
f.write("county_coordinates = {")

for feature in features:
    if feature["properties"]["STATE"] == "36":
        count += 1
        f.write("\"" + feature["properties"]["GEO_ID"] + "\": ")
        coord = feature["geometry"]["coordinates"][0]
        while (type(coord[0][0]) is not float):
            coord = coord[0]
        f.write(str(coord))
        # New York State have 62 counties
        if count < 62:
            f.write(", ")

f.write("}")
print(count)