class StrHelper {
    static escapeSingleQuote(str) {
        return str.replace(/'/g, "\\'");
    }
}

module.exports = StrHelper;