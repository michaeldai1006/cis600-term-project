class StrHelper {
    static escapeSingleQuote(str) {
        if (str) {
            return str.replace(/'/g, "\\'");
        } else {
            return str;
        }
    }
}

module.exports = StrHelper;