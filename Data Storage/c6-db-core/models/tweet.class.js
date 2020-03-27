const db = require('../services/db.conn');
const md5 = require('md5');

class C6Tweet {
    constructor(tweet_token, tweet_id) {
        this.tweet_token = tweet_token;
        this.tweet_id = tweet_id;
    }

    async registerTweet(tweet_info, user_id, place_id) {
        // Verify tweet info
        if (!tweet_info) throw new Error('MISSING TWEET INFO');
        if (!user_id) throw new Error('MISSING USER ID INFO');

        try {
            // Extract info from tweet info
            const { tw_tweet_id, text, latitude, longitude, lang, created_at } = tweet_info;

            // Insert query
            const insertQuery = `
                INSERT INTO c6_tweet (tw_tweet_id, text, latitude, longitude, lang, created_at, user_id, place_id, cdate, udate, status)
                VALUSE (${tw_tweet_id}, '${text}', ${latitude}, ${longitude}, '${lang}', ${created_at}, ${user_id}, ${place_id}, NOW(), NOW(), 0)
            `;

            // Perform insert query
            const insertQueryRes = await db.performQuery(insertQuery);

            // Insert ID
            const insert_id = insertQueryRes['insertId'];
            if (!insert_id) throw new Error('INSERT TWEET RECORD FAILED');
            this.tweet_id = insert_id;


            // Tweet token
            const tweet_token = `TWT-${md5('' + insert_id + tw_tweet_id + 'dsk')}`;
            this.tweet_token = tweet_token;

            // Update query: tweet token, udate, status
            const updateQuery = `
                UPDATE c6_tweet 
                SET tweet_token = '${tweet_token}', udate = NOW(), status = 1
                WHERE id = ${insert_id}
            `;

            // Perform update query
            await db.performQuery(updateQuery);

            // Tweet token result
            return tweet_token;
        } catch (err) {
            throw err;
        }
    }
}

module.exports = C6Tweet;