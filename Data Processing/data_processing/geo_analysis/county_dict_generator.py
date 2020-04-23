import pandas as pd
from geo_analysis.geo_constants import COUNTY_LIST_FILE, COUNTY_DICT_FILE, COUNTY_GEO_ID_FILE


def generate_county_list():
    df = pd.read_csv(COUNTY_GEO_ID_FILE)
    f = open(COUNTY_LIST_FILE, "w")

    f.write("county_list = [")
    count = 0
    for index, row in df.iterrows():
        count += 1
        f.write("\"" + row["Geo_ID"] + "\"")
        if count < 62:
            f.write(", ")

    f.write("]")
    f.close()


def generate_county_dict():
    df = pd.read_csv(COUNTY_GEO_ID_FILE)
    f = open(COUNTY_DICT_FILE, "w")

    f.write("county_dict = {")
    count = 0
    for index, row in df.iterrows():
        count += 1
        f.write("\"" + row["Geo_ID"] + "\": 0")
        if count < 62:
            f.write(", ")

    f.write("}")
    f.close()


if __name__ == '__main__':
    generate_county_list()
    generate_county_dict()
