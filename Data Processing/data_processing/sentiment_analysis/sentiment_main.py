import mysql.connector as mysql
from keys import *
from sentiment_analysis.training_data_clean_up import *
from sentiment_analysis.vader_test import *
from sentiment_analysis.blob_test import *
from sentiment_analysis.whole_sentiment_analysis import *
from sentiment_analysis.daily_sentiment_analysis import *
from sentiment_analysis.sentiment_constants import WHOLE_SENTIMENT_ANALYSIS_RESULT_FILE,\
    DAILY_SENTIMENT_ANALYSIS_RESULT_FILE


def sentiment_analysis(db):
    clean_training_data()
    vader_accuracy = test_vader()
    blob_accuracy = test_blob()
    print("accuracy for vaderSentiment is: %f" % vader_accuracy)
    print("accuracy for textBlob is: %f" % blob_accuracy)
    if vader_accuracy > blob_accuracy:
        print("vaderSentiment", end=" ")
    else:
        print("textBlob", end=" ")
    print("will be used for further analysis")
    print("---------------------------------------------------------------------------------------------------------")

    whole_sentiment_analysis(db)
    daily_sentiment_analysis(db)
    print("sentiment analysis result see: [%s]  and [%s]"
          % (WHOLE_SENTIMENT_ANALYSIS_RESULT_FILE, DAILY_SENTIMENT_ANALYSIS_RESULT_FILE))


if __name__ == '__main__':
    # data_base is our MySQL database, contact zli221su@gmail.com to apply for a keys.py file
    data_base = mysql.connect(
        host=STREAMING_DB_HOST,
        user=STREAMING_DB_USER,
        passwd=STREAMING_DB_PW,
        database="c6_core"
    )

    sentiment_analysis(data_base)
