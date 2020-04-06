const db = require('../services/db.conn');
const md5 = require('md5');

class C6User {
    constructor(user_token, user_id, tw_user_id) {
        this.user_token = user_token;
        this.user_id = user_id;
        this.tw_user_id = tw_user_id;
    }

    async registerUser(user_info) {
        // Verify user info
        if (!user_info) throw new Error('MISSING USER INFO');

        try {
            // Extract info from user info
            const { tw_user_id, name, screen_name, location, description, followers_count, friends_count, created_at } = user_info;

            // Insert query
            const insertQuery = `
                INSERT INTO c6_user(tw_user_id, name, screen_name, location, description, followers_count, friends_count, created_at, cdate, udate, status)
                VALUES ('${tw_user_id}', '${name}', '${screen_name}', '${location}', '${description}', ${followers_count || 'NULL'}, ${friends_count || 'NULL'}, '${created_at}', NOW(), NOW(), 0)
            `;

            // Perform insert query
            const insertQueryRes = await db.performQuery(insertQuery);

            // Insert ID
            const insert_id = insertQueryRes['insertId'];
            if (!insert_id) throw new Error('INSERT USER RECORD FAILED');
            this.user_id = insert_id;

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

    async findUserDetailWithTWUserId() {
        // Verify tw user id
        if (!this.tw_user_id) throw new Error('MISSING TW USER ID');

        try {
            // Find query
            const findQuery = `
                SELECT id AS user_id, user_token, tw_user_id, name, screen_name, location, description, followers_count, friends_count, created_at, cdate, udate, status
                FROM c6_user
                WHERE tw_user_id = '${this.tw_user_id}'
                AND status = 1
                LIMIT 0, 1
            `;

            // Perform query
            const [record] = await db.performQuery(findQuery);

            // Record not found
            if (!record) return record;

            // User id, token for current instance
            const { user_id, user_token } = record;
            this.user_id = user_id;
            this.user_token = user_token;

            // Found instance
            return record;
        } catch (err) {
            throw err;
        }
    }
}

module.exports = C6User;