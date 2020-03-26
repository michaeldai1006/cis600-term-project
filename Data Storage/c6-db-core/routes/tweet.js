var express = require('express');
var router = express.Router();

// Register new tweet data
router.post('/detail', async (req, res, next) => {
  res.send('lol');
});

module.exports = router;