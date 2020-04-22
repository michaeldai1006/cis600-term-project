import pandas as pd

# county list
df = pd.read_csv("./Covid19_NY/us_county_geoid.csv")
f = open("countyList.py", "w")

f.write("county_list = [")
count = 0
for index, row in df.iterrows():
    count += 1
    f.write("\"" + row["Geo_ID"] + "\"")
    if count < 62:
        f.write(", ")

f.write("]")
f.close()

# county dict
df = pd.read_csv("./Covid19_NY/us_county_geoid.csv")
f = open("countyDict.py", "w")

f.write("county_dict = {")
count = 0
for index, row in df.iterrows():
    count += 1
    f.write("\"" + row["Geo_ID"] + "\": 0")
    if count < 62:
        f.write(", ")

f.write("}")
f.close()