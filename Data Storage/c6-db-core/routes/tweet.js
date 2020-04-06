var express = require('express');
var router = express.Router();
const C6TweetAction = require('../actions/tweet.action');

// Register new tweet data
router.post('/detail', async (req, res, next) => {
  try {
    // Tweet record list
    const { record_list } = req.body;
    const payload = await C6TweetAction.registerTweets(record_list);

    // Response
    res.json({
      status: true,
      message: 'REGISTER TWEETS SUCCEED',
      payload
      });
  } catch (err) {
    next(err);
  }
});

module.exports = router;