const db = require('../services/db.conn');
const md5 = require('md5');

class C6Hashtag {
    constructor(hasttag_token, hashtag_id, text) {
        this.hasttag_token = hasttag_token;
        this.hashtag_id = hashtag_id;
        this.text = text;
    }

    async registerHashtag(hashtag_info, tweet_id) {
        // Verify hashtag info
        if (!hashtag_info) throw new Error('MISSING HASHTAG INFO');
        if (!tweet_id) throw new Error('MISSING TWEET ID');

        try {
            // Extract info from hashtag info
            const { text } = hashtag_info;

            // Insert query
            const insertQuery = `
                INSERT INTO c6_hashtag(text, tweet_id, cdate, udate, status)
                VALUSE ('${text}', ${tweet_id}, NOW(), NOW(), 0)
            `;

            // Perform insert query
            const insertQueryRes = await db.performQuery(insertQuery);

            // Insert ID
            const insert_id = insertQueryRes['insertId'];
            if (!insert_id) throw new Error('INSERT HASHTAG RECORD FAILED');
            this.hashtag_id = insert_id;

            // Hashtag token
            const hashtag_token = `HST-${md5('' + insert_id + text + 'izy')}`;
            this.hashtag_token = hashtag_token;

            // Update query: hashtag token, udate, status
            const updateQuery = `
                UPDATE c6_hashtag 
                SET hashtag_token = '${hashtag_token}', udate = NOW(), status = 1
                WHERE id = ${insert_id}
            `;

            // Perform update query
            await db.performQuery(updateQuery);

            // Hashtag token result
            return hashtag_token;   
        } catch (err) {
            throw err;
        }
    }

    async findHashtagDetailWithText() {
        // Verify text existence
        if (!this.text) throw new Error('MISSING TEXT');

        try {
            // Find query
            const findQuery = `
                SELECT id AS hashtag_id, hashtag_token, text, tweet_id, 
                FROM da_user
                WHERE user_token = '${this.user_token}'
                AND status = 2
                LIMIT 0, 1
            `;

            // Perform query
            const [record] = await db.performQuery(findQuery);
        } catch (err) {
            throw err;
        }
    }
}

module.exports = C6Hashtag;