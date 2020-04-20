#
# John D'Amaro
# CIS600 Final Project
#

## Experiment and test

## Hashtags by Date
SELECT c6_tweet.created_at AS TweetDate, c6_hashtag.text AS Hashtag, count(c6_tweet.text) AS HashtagFreq
FROM c6_tweet JOIN c6_tweet_hashtag AS link 
	ON c6_tweet.id = link.tweet_id
    JOIN c6_hashtag ON link.hashtag_id = c6_hashtag.id
WHERE DAY(c6_tweet.created_at) = 1
GROUP BY c6_hashtag.text, DAY(c6_tweet.created_at) 
ORDER BY TweetDate DESC, Hashtag

## Total Hashtag Frequency
SELECT c6_hashtag.text AS Hashtag, count(c6_tweet.text) AS HashtagFreq
FROM c6_tweet JOIN c6_tweet_hashtag AS link 
	ON c6_tweet.id = link.tweet_id
    JOIN c6_hashtag ON link.hashtag_id = c6_hashtag.id
GROUP BY c6_hashtag.text
ORDER BY HashtagFreq DESC

## Tweets by Hashtag ID
SELECT c6_tweet.text, link.tweet_id, c6_hashtag.text, link.hashtag_id
FROM c6_tweet JOIN c6_tweet_hashtag AS link 
	ON c6_tweet.id = link.tweet_id
    JOIN c6_hashtag ON link.hashtag_id = c6_hashtag.id

## Number of unique tweets a day
SELECT  created_at, COUNT(DISTINCT text) AS TweetQty
FROM c6_tweet
GROUP BY DATE_FORMAT(created_at, "%b-%d-%Y")
ORDER BY cdate DESC;

## Number of unique hashtags per Day
SELECT  cdate, COUNT(DISTINCT text) AS DistinctHashtagFreq
             , COUNT(text) AS HashtagFreq
FROM c6_hashtag
GROUP BY DATE_FORMAT(cdate, "%b-%d-%Y")
ORDER BY cdate DESC;

