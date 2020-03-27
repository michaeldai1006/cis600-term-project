const db = require('../services/db.conn');
const md5 = require('md5');

class C6Hashtag {
    constructor(hasttag_token, hashtag_id) {
        this.hasttag_token = hasttag_token;
        this.hashtag_id = hashtag_id;
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
}

module.exports = C6Hashtag;