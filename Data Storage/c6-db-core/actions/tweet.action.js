const C6User = require('../models/user.class');
const C6Place = require('../models/place.class');
const C6Tweet = require('../models/tweet.class');
const C6Hashtag = require('../models/hashtag.class');
const C6TweetHashtag = require('../models/tweet.hashtag');
const moment = require('moment');
const StrHelper = require('../helpers/str.help');

class C6TweetAction {
    static async registerTweets(record_list) {
        // Verify record list
        if (!record_list) throw new Error('MISSING RECORD LIST');
        if (!Array.isArray(record_list)) throw new Error('RECORD LIST FORMAT INVALID');
        if (record_list.length < 1 || record_list.length > 50) throw new Error('RECORD LIST HAS A SIZE LIMIT OF 1 TO 50');

        try {
            // Iterate through records
            const request_list = record_list.map(record => C6TweetAction._regitserRecord(record));

            // Make insert requests
            const result_list = await Promise.all(request_list);

            // Requests result
            return { result_list };
        } catch (err) {
            throw err;
        }
    }

    static async _regitserRecord(record) {
        // Extra parts from record
        const { id, user, place, extended_tweet, entities } = record;

        // Verify required objects
        if (!user) return `RECORD WITH ID: ${id || 'UNKNOWN'} INVALID, MISSING USER OBJECT`;

        try {
            // Register user
            const user_id = await C6TweetAction._registerUser(user);
            if (!user_id) return `REGISTER RECORD WITH ID: ${id || 'UNKNOWN'} FAILED, REGISTER USER FAILED`;

            // Register place
            let place_id = undefined;
            if (place) place_id = await C6TweetAction._registerPlace(place);

            // Register tweet
            const tweet = await C6TweetAction._registerTweet(record, user_id, place_id);
            const { tweet_id, tweet_token } = tweet;
            if (!tweet_id) return `REGISTER RECORD WITH ID: ${id || 'UNKNOWN'} FAILED, REGISTER TWEET FAILED`;
            if (!tweet_token) return `REGISTER RECORD WITH ID: ${id || 'UNKNOWN'} FAILED, REGISTER TWEET FAILED`;

            // Hashtags object
            let hashtags = undefined;
            if (extended_tweet) {
                if (extended_tweet['entities']) {
                    hashtags = extended_tweet['entities']['hashtags'];
                }
            } else if (entities) {
                if (entities['hashtags']) {
                    hashtags = entities['hashtags'];
                }
            }

            // Register hashtags
            await C6TweetAction._registerHashtag(hashtags, tweet_id);

            // Tweet token result
            return tweet_token;
        } catch (err) {
            return err.message || `UNKNOWN ERROR OCCURED WHILE REGISTERING RECORD WITH ID: ${id}`;
        }
    }

    static async _registerUser(user_data) {
        // Verify user
        const { id_str: id, name, screen_name, location, description, followers_count, friends_count, created_at } = user_data;
        if (!id) throw new Error('REGISTER USER FAILED, USER ID NOT PROVIDED');

        try {
            // Search for user from db
            const user = new C6User(undefined, undefined, id);
            const user_record = await user.findUserDetailWithTWUserId();
            if (user_record) return user.user_id;

            // Register new user record
            await user.registerUser({
                tw_user_id: id, 
                name: StrHelper.escapeSingleQuote(name), 
                screen_name: StrHelper.escapeSingleQuote(screen_name), 
                location: StrHelper.escapeSingleQuote(location), 
                description: StrHelper.escapeSingleQuote(description), 
                followers_count, 
                friends_count, 
                created_at: moment(created_at, 'dd MMM DD HH:mm:ss ZZ YYYY', 'en').utc().format('YYYY-MM-DD HH:mm:ss')
            });

            // User id result
            return user.user_id;
        } catch (err) {
            throw err;
        }
    }

    static async _registerPlace(place_data) {
        // Verify place
        let { id, bounding_box, url, place_type, name, full_name, country_code, country } = place_data;
        if (!id) throw new Error('REGISTER PLACE FAILED, PLACE ID NOT PROVIDED');

        try {
            // Search for place from db
            const place = new C6Place(undefined, undefined, id);
            const place_record = await place.findPlaceDetailWithTWPlaceId();
            if (place_record) return place.place_id;

            // Stringify bounding box
            if (bounding_box) bounding_box = JSON.stringify(bounding_box);

            // Register new place record
            await place.registerPlace({
                tw_place_id: id, 
                bounding_box: StrHelper.escapeSingleQuote(bounding_box), 
                url: StrHelper.escapeSingleQuote(url), 
                place_type: StrHelper.escapeSingleQuote(place_type), 
                name: StrHelper.escapeSingleQuote(name), 
                full_name: StrHelper.escapeSingleQuote(full_name), 
                country_code: StrHelper.escapeSingleQuote(country_code), 
                country: StrHelper.escapeSingleQuote(country)
            });

            // Place id result
            return place.place_id;
        } catch (err) {
            throw err;
        }
    }

    static async _registerTweet(tweet_data, user_id, place_id) {
        // Verify tweet
        let { id_str: id, text, extended_tweet, coordinates, lang, created_at } = tweet_data;
        if (!id) throw new Error('REGISTER TWEET FAILED, TWEET ID NOT PROVIDED');

        try {
            // Replace text with extended tweet
            if (extended_tweet) {
                if (extended_tweet['full_text']) {
                    text = extended_tweet['full_text'];
                }
            }

            // Parse coordinates
            let longitude = undefined;
            let latitude = undefined;
            if (coordinates) {
                if (coordinates['coordinates']) {
                    longitude = coordinates['coordinates'][0];
                    latitude = coordinates['coordinates'][1]
                }
            }

            // Register new place record
            const tweet = new C6Tweet(undefined, undefined);
            await tweet.registerTweet({
                tw_tweet_id: id, 
                text: StrHelper.escapeSingleQuote(text), 
                latitude, 
                longitude, 
                lang, 
                created_at: moment(created_at, 'dd MMM DD HH:mm:ss ZZ YYYY', 'en').utc().format('YYYY-MM-DD HH:mm:ss')
            }, user_id, place_id);

            // Tweet instance result
            return tweet;
        } catch (err) {
            throw err;
        }
    }

    static async _registerHashtag(hashtag_data, tweet_id) {
        // Verify hashtag data
        if (!Array.isArray(hashtag_data)) throw new Error('REGISTER HASHTAG FAILED, HASHTAG DATA INVALID');
        if (!tweet_id) throw new Error('REGISTER HASHTAG FAILED, MISSING TWEET ID');

        try {
            // Hash tag instances
            const hashtags = hashtag_data.map(hashtag => new C6Hashtag(undefined, undefined, hashtag['text']));

            // Search for hashtag records in db
            await Promise.all(hashtags.map(hashtag => hashtag.findHashtagDetailWithText()));

            // Register new hashtags
            await Promise.all(hashtags.map(hashtag => {
                if (!hashtag.hashtag_id) {
                    return hashtag.registerHashtag({ text: hashtag.text });
                } else {
                    return
                }
            }));

            // Register tweet hashtags
            await Promise.all(hashtags.map(hashtag => {
                if (hashtag.hashtag_id) {
                    const tweetHashtag = new C6TweetHashtag(tweet_id, hashtag.hashtag_id);
                    return tweetHashtag.registerTweetHashtag();
                }
            }));
        } catch (err) {
            throw err;
        }
    }
}

module.exports = C6TweetAction;