import mysql.connector as mysql
from dataProcessing.sentimentAnalysis.keys import *
from dataProcessing.Qi.geoCounty import *
from dataProcessing.Qi.countyDict import *
from dataProcessing.Qi.countyList import *
import pandas as pd

# This code is only valid for April 2020, if you try this code later, please chang the corresponding month in the SQL
# query
DAILY_CASE_LOCATION_DATA = "case.location.daily.csv"
DATA_START_DATE = 7
TODAY_DATE = 22

db = mysql.connect(
    host = DB_HOST,
    user = DB_USER,
    passwd = DB_PW,
    database="c6_core"
)

cursor = db.cursor()

result_df = pd.DataFrame(columns=["Date"] + county_list)

for date in range(DATA_START_DATE, TODAY_DATE + 1):
    date_string = "2020-04-"
    if date < 10:
        date_string += "0" + str(date)
    else:
        date_string += str(date)
    sql_query = "SELECT c6_tweet.id, bounding_box FROM c6_tweet JOIN c6_place ON (c6_tweet.place_id = c6_place.id) WHERE c6_tweet.cdate LIKE \"" + date_string + "%\""
    cursor.execute(sql_query)

    result = cursor.fetchall()
    for text_tuple in result:
        bounding_box = text_tuple[1]
        point = area_to_point(bounding_box)
        geo_id, county_name = county_of(point)
        if geo_id == "":
            continue
        county_dict[geo_id] += 1

    county_dict["Date"] = date_string
    result_df = result_df.append(county_dict, ignore_index=True)

    # reset county dict
    for key in county_dict:
        if key == "Date":
            continue
        county_dict[key] = 0

    print(" Proceeding date %s" % date_string)


result_df.to_csv(DAILY_CASE_LOCATION_DATA)

print("finished")
