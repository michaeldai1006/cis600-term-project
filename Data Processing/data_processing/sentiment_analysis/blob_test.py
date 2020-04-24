import pandas as pd
from textblob import TextBlob
from sentiment_analysis.sentiment_constants import CLEANED_TRAINING_DATA_FILE


def test_blob():
    print("Testing the Accuracy of vader sentiment")

    correct = 0
    incorrect = 0
    non = 0
    df = pd.read_csv(CLEANED_TRAINING_DATA_FILE)

    for index, row in df.iterrows():
        sentiment = 0
        blob = TextBlob(str(row["text"]))
        for sentence in blob.sentences:
            sentiment += sentence.sentiment.polarity
        if sentiment == 0.0:
            non += 1
        elif (sentiment < 0 and row["target"] == 0) or (sentiment > 0 and row["target"] == 4):
            correct += 1
        else:
            incorrect += 1
        if index % 50000 == 0:
            print("textBlob: %d: correct = %d, incorrect = %d, non = %d, ratio = %f"
                  % (index, correct, incorrect, non, (correct + non / 2) / (correct + incorrect + non)))

    accuracy = ((correct + non / 2) / (correct + incorrect + non))
    print("correct = %d" % correct)
    print("incorrect = %d" % incorrect)
    print("non = %d" % non)
    print("textBlob accuracy: %f" % accuracy)

    return accuracy
