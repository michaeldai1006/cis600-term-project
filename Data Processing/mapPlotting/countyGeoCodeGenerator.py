import pandas as pd

df = pd.read_csv("./Covid19_NY/us_county_geoid.csv")
f = open("countyGeoCode.py", "w")

f.write("geo_county = {")
count = 0
for index, row in df.iterrows():
    count += 1
    f.write("\"" + row["Geo_ID"] + "\": \"" + row["County"] + "\"")
    if count < 62:
        f.write(", ")

f.write("}")
f.close()