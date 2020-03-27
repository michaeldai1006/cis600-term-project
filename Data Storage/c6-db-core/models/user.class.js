const db = require('../services/db.conn');
const md5 = require('md5');

class C6User {
    constructor(user_token, user_id) {
        this.user_token = user_token;
        this.user_id = user_id;
    }

    async registerUser(user_info) {
        // Verify user info
        if (!user_info) throw new Error('MISSING USER INFO');

        try {
            // Extract info from user info
            const { tw_user_id, user_name, screen_name, location, description, followers_count, friends_count, created_at } = user_info;

            // Insert query
            const insertQuery = `
                INSERT INTO c6_user(tw_user_id, user_name, screen_name, location, description, followers_count, friends_count, created_at, cdate, udate, status)
                VALUSE (${tw_user_id}, '${user_name}', '${screen_name}', '${location}', '${description}', ${followers_count}, ${friends_count}, '${created_at}', NOW(), NOW(), 0)
            `;

            // Perform insert query
            const insertQueryRes = await db.performQuery(insertQuery);

            // Insert ID
            const insert_id = insertQueryRes['insertId'];
            if (!insert_id) throw new Error('INSERT USER RECORD FAILED');
            this.tweet_id = insert_id;


            // User token
            const user_token = `USR-${md5('' + insert_id + tw_user_id + 'kud')}`;
            this.user_token = user_token;

            // Update query: user token, udate, status
            const updateQuery = `
                UPDATE c6_user 
                SET user_token = '${user_token}', udate = NOW(), status = 1
                WHERE id = ${insert_id}
            `;

            // Perform update query
            await db.performQuery(updateQuery);

            // User token result
            return user_token;   
        } catch (err) {
            throw err;
        }
    }
}

module.exports = C6User;