# This file get tweets in New York State by using Twitter Streaming API. Then print all the tweets with keyword 'virus' and 'pandemic'.

import sys
import twitter
import time
import json
import traceback
import requests
from keys import *

# Constants
POST_JSON_LEN = 4


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

while True:
    # stream = twitter_stream.statuses.filter(track=q)
    stream = twitter_stream.statuses.filter(locations = loc)


    f = open("log.txt","a")
    keywords = ["virus", "pandemic","COVID", "Coronavirus", "COVID-19","Quarantine","mask","StayHome"]
    total_post_count = 0
    virus_post_count = 0
    start_time = time.time()
    post_json_body_list = []

    try:
        for tweet in stream:
            # print(tweet)
            total_post_count += 1
            if 'text' not in tweet:
                continue
            text = tweet['text']
            if 'extended_tweet' in tweet:
                text = tweet['extended_tweet']['full_text']

            if any(keyword in text for keyword in keywords):
                virus_post_count += 1
                print(time.strftime("%H:%M:%S", time.localtime()))
                print("Post text: {}".format(text))
                print(json.dumps(tweet))

                post_json_body_list.append(tweet)
                f.write("\n" + json.dumps(tweet))

                if len(post_json_body_list) == POST_JSON_LEN:
                    post_json = {"record_list": post_json_body_list}
                    print(json.dumps(post_json))
                    r = requests.post(DATABASE_API_URL, json=post_json)
                    print(r.status_code)
                    print(r.text)

                    post_json_body_list.clear()

            print("{:.3f}s:  virus-related posts = {}, virus-related percentage = {:.2f}%".format(time.time() - start_time, virus_post_count, virus_post_count/total_post_count * 100))
            sys.stdout.flush()
    except:
        f.write("\nAn exception occurred")
        exceptf = open("exception.txt", "a")
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(file=exceptf)
        exceptf.close()
    finally:
        f.close()

    print("streaming API not responding, sleep for 5 min.........................")
    time.sleep(60*5 + 5)




