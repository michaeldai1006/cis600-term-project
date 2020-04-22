import mysql.connector as mysql
from keys import *
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# This code is only valid for April 2020, if you try this code later, please chang the corresponding month in the SQL
# query
LOCAL_TEXT_FILE = "sentiment.analysis.result.daily.csv"
DATA_START_DATE = 7
TODAY_DATE = 22

db = mysql.connect(
    host = DB_HOST,
    user = DB_USER,
    passwd = DB_PW,
    database="c6_core"
)

cursor = db.cursor()

result_df = pd.DataFrame({"date": [], "positive": [], "negative": [], "neutral": [], "pRatio": []})

analyser = SentimentIntensityAnalyzer()

for date in range(DATA_START_DATE, TODAY_DATE + 1):
    date_string = ""
    if date < 10:
        date_string = "0" + str(date)
    else:
        date_string = str(date)
    sql_query = "SELECT id, text FROM c6_tweet WHERE (cdate LIKE \"2020-04-" + date_string + "%\") AND (lang = \"en\")"
    cursor.execute(sql_query)

    positive = 0
    negative = 0
    neutral = 0
    result = cursor.fetchall()
    for text_tuple in result:
        text = text_tuple[1].replace("\n", " ")

        sentiment = analyser.polarity_scores(text)["compound"]
        if sentiment < 0:
            positive += 1
        elif sentiment > 0:
            negative += 1
        else:
            neutral += 1
    curDict = {
        "date": "2020-04-" + date_string,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "pRatio": (positive + neutral / 2) / (positive + negative + neutral)
    }
    print(curDict)
    result_df = result_df.append(curDict, ignore_index=True)

    print(" Proceeding date 2020-04-%s" % date_string)


result_df.to_csv(LOCAL_TEXT_FILE)

print("finished")
