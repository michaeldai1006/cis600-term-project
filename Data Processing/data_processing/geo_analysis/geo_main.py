import mysql.connector as mysql
from keys import *
from geo_analysis.county_geo_code_generator import *
from geo_analysis.county_coordinate_generator import *
from geo_analysis.county_dict_generator import *
from geo_analysis.location_map import *


def geo_main(db):
    generate_county_list()
    generate_county_dict()
    generate_county_coordinate()
    generate_county_geo_codes()
    map_daily_tweets_to_counties(db)


if __name__ == '__main__':
    # data_base is our MySQL database, contact zli221su@gmail.com to apply for a keys.py file
    data_base = mysql.connect(
        host=STREAMING_DB_HOST,
        user=STREAMING_DB_USER,
        passwd=STREAMING_DB_PW,
        database="c6_core"
    )

    geo_main(data_base)