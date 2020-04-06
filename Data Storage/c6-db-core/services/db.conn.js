const mysql = require('mysql');
const pool = mysql.createPool({
    connectionLimit: 10,
    host: process.env.C6_DB_HOST,
    user: process.env.C6_DB_USER,
    password: process.env.C6_DB_PASS,
    database: 'c6_core'
});

const performQuery = (query) => {
    // Remove undefined VARCHAR values
    query = query.replace(/'undefined'/g, 'NULL');

    return new Promise((resolve, reject) => {
        pool.getConnection((err, conn) => {
            if (err) {
                console.log(err);
                reject(err);
            } else {
                conn.query(query, (err, res) => {
                    if (err) {
                        if (err.errno === 1213) performQuery(query).then(result => resolve(result)).catch(t_err => reject(t_err)); else reject(err);
                    } else resolve(res);
                    conn.release();
                });
            }
        });
    });
};

module.exports.performQuery = performQuery;