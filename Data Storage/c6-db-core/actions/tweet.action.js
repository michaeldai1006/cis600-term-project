const C6User = require('../models/user.class');

class C6TweetAction {
    static async registerTweets(record_list) {
        // Verify record list
        if (!record_list) throw new Error('MISSING RECORD LIST');
        if (!Array.isArray(record_list)) throw new Error('RECORD LIST FORMAT INVALID');
        if (record_list.length < 1 || record_list.length > 50) throw new Error('RECORD LIST HAS A SIZE LIMIT OF 1 TO 50');

        try {
            // Iterate through records
            const request_list = record_list.map(record => C6TweetAction._regitserTweet(record));

            // Make insert requests
            const result_list = await Promise.all(request_list);

            // Requests result
            return { result_list };
        } catch (err) {
            throw err;
        }
    }

    static async _regitserTweet(record) {
        // Extra parts from record
        const { id, user } = record;

        // Verify user
        if (!user) return `RECORD WITH ID: ${id || 'UNKNOWN'} INVALID, MISSING USER OBJECT`;

        try {
            await _registerUser(user);
        } catch (err) {
            return err.message || `UNKNOWN ERROR OCCURED WHILE REGISTERING RECORD WITH ID: ${id}`;
        }
    }

    static async _registerUser(user) {

    }
}

module.exports = C6TweetAction;