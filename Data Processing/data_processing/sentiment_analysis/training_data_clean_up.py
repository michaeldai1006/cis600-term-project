import pandas as pd
from nltk.tokenize import WordPunctTokenizer
import re
from sentiment_analysis.sentiment_constants import TRAINING_DATA_FILE, CLEANED_TRAINING_DATA_FILE


def clean_training_data():
    cols = ['sentiment', 'id', 'date', 'query_string', 'user', 'text']
    df = pd.read_csv(TRAINING_DATA_FILE, header=None, names=cols, encoding='latin-1')

    df.drop(['id', 'date', 'query_string', 'user'], axis=1, inplace=True)

    # Data Preparation
    df['pre_clean_len'] = [len(t) for t in df.text]
    tok = WordPunctTokenizer()
    pat1 = r'@[A-Za-z0-9]+'
    pat2 = r'https?://[A-Za-z0-9./]+'
    combined_pat = r'|'.join((pat1, pat2))

    def tweet_cleaner(text):
        stripped = re.sub(combined_pat, '', text)
        try:
            clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
        except:
            clean = stripped
        letters_only = re.sub("[^a-zA-Z]", " ", clean)
        lower_case = letters_only.lower()
        # tokenize and join together to remove unnecessary white spaces
        words = tok.tokenize(lower_case)
        return (" ".join(words)).strip()

    testing = df.text[:100]
    test_result = []
    for t in testing:
        test_result.append(tweet_cleaner(t))
    test_result

    nums = [0, 400000, 800000, 1200000, 1600000]
    print("Cleaning and parsing the tweets...\n")
    clean_tweet_texts = []
    for i in range(len(nums) - 1):
        for j in range(nums[i], nums[i + 1]):
            if (j + 1) % 20000 == 0:
                print("Tweets %d of %d has been processed" % (j + 1, nums[-1]))
            clean_tweet_texts.append(tweet_cleaner(df['text'][j]))

    clean_df = pd.DataFrame(clean_tweet_texts, columns=['text'])
    clean_df['target'] = df.sentiment

    # Drop data with empty text
    clean_df.dropna(inplace=True)
    clean_df.reset_index(drop=True, inplace=True)

    clean_df.to_csv(CLEANED_TRAINING_DATA_FILE, encoding='utf-8')
