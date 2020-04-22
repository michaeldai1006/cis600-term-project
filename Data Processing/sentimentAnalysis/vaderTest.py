from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

# sentence = "abcd"
#
# score = analyser.polarity_scores(sentence)
#
#
# print(score)
# print(type(score['compound']))


import pandas as pd

TRAINING_DATA_FILE = "./clean_tweet.csv"

correct = 0
incorrect = 0
non = 0
#encoding='latin-1'
df = pd.read_csv(TRAINING_DATA_FILE)

for index, row in df.iterrows():
    sentiment = analyser.polarity_scores(row["text"])["compound"]
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