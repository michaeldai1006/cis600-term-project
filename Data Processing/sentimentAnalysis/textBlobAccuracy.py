import pandas as pd
from textblob import TextBlob

TRAINING_DATA_FILE = "./clean_tweet.csv"

correct = 0
incorrect = 0
non = 0
#encoding='latin-1'
df = pd.read_csv(TRAINING_DATA_FILE)

for index, row in df.iterrows():
    sentiment = 0
    blob = TextBlob(row["text"])
    blob.noun_phrases
    for sentence in blob.sentences:
        sentiment += sentence.sentiment.polarity
    if sentiment == 0.0:
        non += 1
    elif (sentiment < 0 and row["target"] == 0) or (sentiment > 0 and row["target"] == 4):
        correct += 1
    else:
        incorrect += 1
    if index % 500 == 0:
        print("%d: correct = %d, incorrect = %d, non = %d, ratio = %f" % (index, correct, incorrect, non, correct / (correct + incorrect)))

print("correct = " + str(correct))
print("incorrect = " + str(incorrect))
print("non = " + str(non))