const db = require('../services/db.conn');
const md5 = require('md5');

class C6Place {
    constructor(place_token, place_id, tw_place_id) {
        this.place_token = place_token;
        this.place_id = place_id;
        this.tw_place_id = tw_place_id;
    }

    async registerPlace(place_info) {
        // Verify place info
        if (!place_info) throw new Error('MISSING PLACE INFO');

        try {
            // Extract info from place info
            const { latitude1, latitude2, latitude3, latitude4, longitude1, longitude2, longitude3, longitude4, 
            tw_place_id, url, place_type, name, full_name, country_code, country } = place_info;

            // Insert query
            const insertQuery = `
                INSERT INTO c6_place(latitude1, latitude2, latitude3, latitude4, longitude1, longitude2, longitude3, longitude4, tw_place_id, url, place_type, name, full_name, country_code, country, cdate, udate, status)
                VALUSE (${latitude1}, ${latitude2}, ${latitude3}, ${latitude4}, ${longitude1}, ${longitude2}, ${longitude3}, ${longitude4}, ${tw_place_id}, '${url}', '${place_type}', '${name}', '${full_name}', '${country_code}', '${country}', NOW(), NOW(), 0)
            `;

            // Perform insert query
            const insertQueryRes = await db.performQuery(insertQuery);

            // Insert ID
            const insert_id = insertQueryRes['insertId'];
            if (!insert_id) throw new Error('INSERT PLACE RECORD FAILED');
            this.place_id = insert_id;

            // Place token
            const place_token = `PLC-${md5('' + insert_id + tw_place_id + 'isq')}`;
            this.place_token = place_token;

            // Update query: place token, udate, status
            const updateQuery = `
                UPDATE c6_place 
                SET place_token = '${place_token}', udate = NOW(), status = 1
                WHERE id = ${insert_id}
            `;

            // Perform update query
            await db.performQuery(updateQuery);

            // Place token result
            return place_token;   
        } catch (err) {
            throw err;
        }
    }

    async findPlaceDetailWithTWPlaceId() {
        // Verify tw place id
        if (!this.tw_place_id) throw new Error('MISSING TW PLACE ID');

        try {
            // Find query
            const findQuery = `
                SELECT id AS place_id, place_token, latitude1, latitude2, latitude3, latitude4, longitude1, longitude2, longitude3, longitude4, tw_place_id, url, place_type, name, full_name, country_code, country, cdate, udate, status
                FROM c6_place
                WHERE tw_place_id = '${this.tw_place_id}'
                AND status = 1
                LIMIT 0, 1
            `;

            // Perform query
            const [record] = await db.performQuery(findQuery);

            // Record not found
            if (!record) return record;

            // Place id, token for current instance
            const { place_id, place_token } = record;
            this.place_id = place_id;
            this.place_token = place_token;

            // Found instance
            return record;
        } catch(err) {
            throw err;
        }
    }
}

module.exports = C6Place;