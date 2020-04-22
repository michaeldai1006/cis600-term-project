import mysql.connector as mysql
from keys import *
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

LOCAL_TEXT_FILE = "sentiment.analysis,result.csv"
LINES_PER_SQL_QUERY = 1000

db = mysql.connect(
    host = DB_HOST,
    user = DB_USER,
    passwd = DB_PW,
    database="c6_core"
)

cursor = db.cursor()

# list of name, degree, score
text = []
sentiment = []

# dictionary of lists
dict = {'text': text, 'sentiment': sentiment}
df = pd.DataFrame(dict)

# saving the dataframe
df.to_csv(LOCAL_TEXT_FILE)


#
cursor.execute("SELECT MAX(id) FROM c6_tweet")
max_id = cursor.fetchall()[0][0]
analyser = SentimentIntensityAnalyzer()

for i in range(max_id // LINES_PER_SQL_QUERY):
    left = (i - 1) * LINES_PER_SQL_QUERY
    right = i * LINES_PER_SQL_QUERY
    sql_query = "SELECT id, text FROM c6_tweet WHERE (id BETWEEN " + str(left) + " AND " + str(right) + ") AND (lang = \"en\")"
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

    temp_df = pd.DataFrame({'text': texts, 'sentiment': sentiments}, index = indices)
    temp_df.to_csv(LOCAL_TEXT_FILE, mode='a', header=False)

    print(" %d items read, total amount is %d" %(i * LINES_PER_SQL_QUERY, max_id))

print("finished")