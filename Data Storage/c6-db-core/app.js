const dotenv = require('dotenv');
dotenv.config();
var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

const tweetRoute = require('./routes/tweet.js');

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/tweet', tweetRoute);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  res.status(404).json({
    status: false,
    message: 'ROUTE NOT FOUND'
  });
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  console.log(err);
  res.status(err.status || 500);
  res.json({
    status: false,
    message: err.message || err
  });
});

module.exports = app;
