import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from constants import LINES_PER_SQL_QUERY
from sentiment_analysis.sentiment_constants import WHOLE_SENTIMENT_ANALYSIS_RESULT_FILE


def whole_sentiment_analysis(db):
    cursor = db.cursor()
    df = pd.DataFrame(columns=['text', 'sentiment'])
    df.to_csv(WHOLE_SENTIMENT_ANALYSIS_RESULT_FILE)

    cursor.execute("SELECT MAX(id) FROM c6_tweet")
    max_id = cursor.fetchall()[0][0]
    analyser = SentimentIntensityAnalyzer()

    for i in range(max_id // LINES_PER_SQL_QUERY):
        left = (i - 1) * LINES_PER_SQL_QUERY
        right = i * LINES_PER_SQL_QUERY
        sql_query = "SELECT id, text FROM c6_tweet WHERE (id BETWEEN " + str(left) + " AND " + str(
            right) + ") AND (lang = \"en\")"
        cursor.execute(sql_query)

        indices = []
        texts = []
        sentiments = []
        result = cursor.fetchall()
        for text_tuple in result:
            indices.append(text_tuple[0])

            text = text_tuple[1].replace("\n", " ")
            texts.append(text)

            sentiment = analyser.polarity_scores(text)["compound"]
            sentiments.append(sentiment)

        temp_df = pd.DataFrame({'text': texts, 'sentiment': sentiments}, index=indices)
        temp_df.to_csv(WHOLE_SENTIMENT_ANALYSIS_RESULT_FILE, mode='a', header=False)

        print(" %d items read, total amount is %d" % (i * LINES_PER_SQL_QUERY, max_id))

    print("finished")
