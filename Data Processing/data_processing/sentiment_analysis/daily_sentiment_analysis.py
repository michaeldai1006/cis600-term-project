import pandas as pd
import mysql.connector as mysql
from keys import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from constants import DATA_START_DATE, TODAY_DATE
from sentiment_analysis.sentiment_constants import DAILY_SENTIMENT_ANALYSIS_RESULT_FILE


# This code is only valid for April 2020, if you try this code later, please chang the corresponding month in the SQL
def daily_sentiment_analysis(db):
    cursor = db.cursor()

    result_df = pd.DataFrame({"date": [], "positive": [], "negative": [], "neutral": [], "pRatio": []})

    analyser = SentimentIntensityAnalyzer()

    for date in range(DATA_START_DATE, TODAY_DATE + 1):
        date_string = ""
        if date < 10:
            date_string = "0" + str(date)
        else:
            date_string = str(date)
        sql_query = "SELECT id, text FROM c6_tweet WHERE (created_at LIKE \"2020-04-" + date_string + "%\") AND (lang = \"en\")"
        cursor.execute(sql_query)

        positive = 0
        negative = 0
        neutral = 0
        result = cursor.fetchall()
        print("2020-04-%s: result length = %d" % (date_string, len(result)))
        for text_tuple in result:
            text = text_tuple[1].replace("\n", " ")

            sentiment = analyser.polarity_scores(text)["compound"]
            if sentiment < 0:
                positive += 1
            elif sentiment > 0:
                negative += 1
            else:
                neutral += 1
        p_ratio = 0
        if (positive + negative + neutral) != 0 :
            p_ratio = (positive + neutral / 2) / (positive + negative + neutral)
        cur_dict = {
            "date": "2020-04-" + date_string,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "pRatio": p_ratio
        }
        print(cur_dict)
        result_df = result_df.append(cur_dict, ignore_index=True)

        print(" Proceeding date 2020-04-%s" % date_string)

    result_df.to_csv(DAILY_SENTIMENT_ANALYSIS_RESULT_FILE)

    print("finished")


if __name__ == '__main__':
    data_base = mysql.connect(
        host=REGULAR_DB_HOST,
        user=REGULAR_DB_USER,
        passwd=REGULAR_DB_PW,
        database="c6_core"
    )

    daily_sentiment_analysis(data_base)
