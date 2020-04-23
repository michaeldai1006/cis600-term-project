from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from sentiment_analysis.sentiment_constants import CLEANED_TRAINING_DATA_FILE


def test_vader():
    print("Testing the Accuracy of vader sentiment")

    correct = 0
    incorrect = 0
    non = 0
    df = pd.read_csv(CLEANED_TRAINING_DATA_FILE)
    analyser = SentimentIntensityAnalyzer()

    for index, row in df.iterrows():
        sentiment = analyser.polarity_scores(str(row["text"]))["compound"]
        if sentiment == 0.0:
            non += 1
        elif (sentiment < 0 and row["target"] == 0) or (sentiment > 0 and row["target"] == 4):
            correct += 1
        else:
            incorrect += 1
        if index % 50000 == 0:
            print("vaderSentiment: %d: correct = %d, incorrect = %d, non = %d, ratio = %f"
                  % (index, correct, incorrect, non, (correct + non / 2) / (correct + incorrect + non)))

    accuracy = ((correct + non / 2) / (correct + incorrect + non))
    print("correct = %d" % correct)
    print("incorrect = %d" % incorrect)
    print("non = %d" % non)
    print("vaderSentiment accuracy: %f" % accuracy)

    return accuracy
