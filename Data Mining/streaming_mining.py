# This file get tweets in New York State by using Twitter Streaming API. Then print all the tweets with keyword 'virus' and 'pandemic'.

import sys
import twitter
import time

# This login class is modified from Cookbook
def oauth_login():
    CONSUMER_KEY = '...'
    CONSUMER_SECRET = '...'
    OAUTH_TOKEN = '...'
    OAUTH_TOKEN_SECRET = '...'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

twitter_api = oauth_login()

# Reference the self.auth parameter
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

# Query terms
# Free Twitter-API users only support "OR" operation in query.
# In order to search tweets in New York "AND" contains 'virus' keywords, I use query to get tweets in such locations and then check if the text contains 'virus'.

# q = 'coronavirus' # Comma-separated list of terms
# print('Filtering the public timeline for track={0}'.format(q), file=sys.stderr)
# sys.stderr.flush()

# See https://developer.twitter.com/en/docs/tutorials/consuming-streaming-data
loc = '-79.76,42,-79.05,42.84,-79.04,42,-76.8,43.63,-76.7,42,-73.2,45,-75.3,41.2,-73.5,42.1,-74.2,40.5,-71.8,41.3'
# area for new york state
# -79.76,42
# -79.05,42.84
#
# -79.04,42
# -76.8,43.63
#
# -76.7,42
# -73.2,45
#
# -75.3,41.2
# -73.5,42.1
#
# -74.2,40.5
# -71.8,41.3
print('Filtering the public location for locations={0}'.format(loc), file=sys.stderr)
sys.stderr.flush()

# stream = twitter_stream.statuses.filter(track=q)
stream = twitter_stream.statuses.filter(locations = loc)


keywords = ['virus', 'pandemic']
total_post_count = 0
virus_post_count = 0
start_time = time.time()

for tweet in stream:
    # print(tweet)
    total_post_count += 1
    text = tweet['text']
    if 'extended_tweet' in tweet:
        text = tweet['extended_tweet']['full_text']

    if any(keyword in text for keyword in keywords):
        virus_post_count += 1
        print("Post text: {}".format(text))
    print("{:.3f}s:  virus-related posts = {}, virus-related percentage = {:.2f}%".format(time.time() - start_time, virus_post_count, virus_post_count/total_post_count * 100))

    sys.stdout.flush()

    # Save to a database in a particular collection




