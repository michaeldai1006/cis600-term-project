const C6TweetAction = require('../actions/tweet.action');

(async () => {
    const response = await C6TweetAction.registerTweets([{'id': 666}])
    console.log(response);
})()