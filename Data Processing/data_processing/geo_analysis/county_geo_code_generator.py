import pandas as pd
from geo_analysis.geo_constants import COUNTY_GEO_CODE_FILE


def generate_county_geo_codes():
    df = pd.read_csv("./Covid19_NY/us_county_geoid.csv")
    f = open(COUNTY_GEO_CODE_FILE, "w")

    f.write("geo_county = {")
    count = 0
    for index, row in df.iterrows():
        count += 1
        f.write("\"" + row["Geo_ID"] + "\": \"" + row["County"] + "\"")
        if count < 62:
            f.write(", ")

    f.write("}")
    f.close()


if __name__ == '__main__':
    generate_county_geo_codes()
