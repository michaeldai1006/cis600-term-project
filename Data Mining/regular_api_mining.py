# This file get tweets in New York State by using Twitter Streaming API. Then print all the tweets with keyword 'virus' and 'pandemic'.

import sys
import twitter
import time
import json
import traceback
import requests
from urllib.error import URLError
from http.client import BadStatusLine
from keys import *

# Constants
SQL_STORAGE_PERCENTAGE = 0.1
SQL_API_DATA_COUNT_PER_REQUEST = 10
TWITTER_REQUEST_COUNT = 100   # max = 100
MAX_RESULTS = 190000000
CURRENT_AREA = 1  # area code is from 0 to 10

# record the oldest tweet id that have been searched (for debuging)
MAX_ID = 2000000000000000000
# MAX_ID = 1248383281097129985

# New York state is divided into 11 circles
# [latitude, longitude, radius]
ny_geocodes = [[40.577048,-74.156876,7.71],[40.707987,-73.839050,12.89],[40.800666,-73.300726,18.31],[40.857999,-72.793390,15.10],[40.946189,-72.192041,22.98],[41.598373,-74.246625,62.66],[43.837307,-74.514242,97.97],[42.730235,-76.356708,77.49],[43.078671,-78.337795,42.03],[42.240601,-78.103827,33.91],[42.302034,-79.198193,31.40]]
test_geocode = [42,-79.76,20]



f = open("regular_log.txt", "a")


twitter_api = oauth_login()

class SqlApiException (Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

def send_to_sql_api(statuses):
    if len(statuses) == 0:
        return
    statuses = statuses[0: max(1, int(len(statuses) * SQL_STORAGE_PERCENTAGE))]
    left = 0
    right = SQL_API_DATA_COUNT_PER_REQUEST
    while right <= len(statuses):
        right = min(right, len(statuses))
        post_json = {"record_list": statuses[left: right]}
        r = requests.post(DATABASE_API_URL_REGULAR, json=post_json)
        if r.status_code != 200:
            if left < (right - 2):
                right -= 2
                print("Current request entity is too large, request size reduced by 2 temporarily.\nCurrent Request Size is: %d" % (right - left))
                continue
            print("DEBUGING: left = %d, right = %d" %(left, right))
            print(json.dumps(post_json))
            raise SqlApiException(r.status_code, r.content)
        left += SQL_API_DATA_COUNT_PER_REQUEST
        right += SQL_API_DATA_COUNT_PER_REQUEST


def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):
    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):

        if wait_period > 3600:  # Seconds
            print('Too many retries. Quitting.', file=sys.stderr)
            raise e

        # See https://developer.twitter.com/en/docs/basics/response-codes
        # for common codes

        if e.e.code == 401:
            print('Encountered 401 Error (Not Authorized)', file=sys.stderr)
            return None
        elif e.e.code == 404:
            print('Encountered 404 Error (Not Found)', file=sys.stderr)
            return None
        elif e.e.code == 429:
            print('Encountered 429 Error (Rate Limit Exceeded)', file=sys.stderr)
            if sleep_when_rate_limited:
                print("Retrying in 15 minutes...ZzZ...", file=sys.stderr)
                sys.stderr.flush()
                time.sleep(60 * 5 + 5)
                print('...ZzZ...Awake now and trying again.', file=sys.stderr)
                return 2
            else:
                raise e  # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered {0} Error. Retrying in {1} seconds'.format(e.e.code, wait_period), file=sys.stderr)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function

    wait_period = 2
    error_count = 0

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError as e:
            error_count = 0
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("URLError encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise
        except BadStatusLine as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("BadStatusLine encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise





def twitter_search(twitter_api, q, geocode, max_results=200, max_id = MAX_ID, **kw):
    tweet_count = 0

    kwargs = {
        "max_id": max_id,
        "q":q,
        "geocode":"%f,%f,%dmi" % (geocode[0], geocode[1], geocode[2]),
        "count":TWITTER_REQUEST_COUNT
    }
    # search_results = twitter_api.search.tweets(**kwargs)
    search_results = make_twitter_request(twitter_api.search.tweets, max_errors=10, **kwargs)
    # print(json.dumps(search_results))
    # search_results = twitter_api.search.tweets(q = q, geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), count=100, **kw)
    statuses = search_results['statuses']
    if len(statuses) > 0:
        earliest_id = statuses[0]["id"]
    else:
        earliest_id = 0

    for _ in range(int(max_results) + 1):  # 10*100 = 1000

        tweet_count += len(statuses)
        send_to_sql_api(statuses)
        if len(statuses) > 0:
            print(json.dumps(statuses[0]))
        f.write("\n" + json.dumps(statuses))
        print(tweet_count)

        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError as e:  # No more results when next_results doesn't exist
            break

        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        next_args = dict([kv.split('=')
                       for kv in next_results[1:].split("&")])
        kwargs["max_id"] = next_args["max_id"]
        earliest_id = int(next_args["max_id"])
        # search_results = twitter_api.search.tweets(max_id = kwargs["max_id"], q = q, geocode = "%f,%f,%dkm" % (geocode[0], geocode[1], geocode[2]), count=100, **kw)
        search_results = make_twitter_request(twitter_api.search.tweets, max_errors=10, **kwargs)
        # statuses += search_results['statuses']
        statuses = search_results['statuses']

        if tweet_count >= max_results:
            break
    return earliest_id

q = ""
for i in range(len(keywords)):
    q += keywords[i]
    if i < (len(keywords) - 1):
        q += " OR "
print("q = " + q)



earliest_id = twitter_search(twitter_api, q, ny_geocodes[CURRENT_AREA], max_results=MAX_RESULTS, max_id = MAX_ID)

print("earliest_id = %d" % (earliest_id))