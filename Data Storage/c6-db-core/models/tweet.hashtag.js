const db = require('../services/db.conn');
const md5 = require('md5');

class C6TweetHashtag {
    constructor(tweet_id, hashtag_id, tweet_hashtag_token, tweet_hashtag_id) {
        this.tweet_id = tweet_id;
        this.hashtag_id = hashtag_id;
        this.tweet_hashtag_token = tweet_hashtag_token;
        this.tweet_hashtag_id = tweet_hashtag_id;
    }

    async registerTweetHashtag() {
        // Verify tweet hashtag info
        if (!this.tweet_id) throw new Error('MISSING TWEET ID');
        if (!this.hashtag_id) throw new Error('MISSING HASHTAG ID');

        try {
            // Insert query
            const insertQuery = `
                INSERT INTO c6_tweet_hashtag(tweet_id, hashtag_id, cdate, udate, status)
                VALUSE (${this.tweet_id}, ${this.hashtag_id}, NOW(), NOW(), 0)
            `;

            // Perform insert query
            const insertQueryRes = await db.performQuery(insertQuery);

            // Insert ID
            const insert_id = insertQueryRes['insertId'];
            if (!insert_id) throw new Error('INSERT TWEET HASHTAG RECORD FAILED');
            this.tweet_hashtag_id = insert_id;

            // Tweet hashtag token
            const tweet_hashtag_token = `THS-${md5('' + insert_id + this.tweet_id + this.hashtag_id + 'spd')}`;
            this.tweet_hashtag_token = tweet_hashtag_token;

            // Update query: tweet hashtag token, udate, status
            const updateQuery = `
                UPDATE c6_tweet_hashtag 
                SET tweet_hashtag_token = '${tweet_hashtag_token}', udate = NOW(), status = 1
                WHERE id = ${insert_id}
            `;

            // Perform update query
            await db.performQuery(updateQuery);

            // Tweet hashtag token result
            return tweet_hashtag_token;  
        } catch (err) {
            throw err;
        }
    }

    async findTweetHashtagDetailWithTweetIdHashtagId() {
        // Verify tweet hashtag info
        if (!this.tweet_id) throw new Error('MISSING TWEET ID');
        if (!this.hashtag_id) throw new Error('MISSING HASHTAG ID');

        try {
            // Find query
            const findQuery = `
                SELECT id AS tweet_hashtag_id, tweet_hashtag_token, tweet_id, hashtag_id, cdate, udate, status
                FROM c6_tweet_hashtag
                WHERE tweet_id = '${this.tweet_id}'
                AND hashtag_id = '${this.hashtag_id}'
                AND status = 1
                LIMIT 0, 1
            `;

            // Perform query
            const [record] = await db.performQuery(findQuery);

            // Record not found
            if (!record) return record;

            // Tweet hashtag id, token for current instance
            const { tweet_hashtag_id, tweet_hashtag_token } = record;
            this.tweet_hashtag_id = tweet_hashtag_id;
            this.tweet_hashtag_token = tweet_hashtag_token;

            // Found instance
            return record;
        } catch (err) {
            throw err;
        }
    }
}

module.exports = C6TweetHashtag;