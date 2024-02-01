// Require the libraries.
const async = require('async');
const $ = require('jquerygo');
const prompt = require('prompt');
const config = require('nconf');
const path = require('path');
const fs = require('fs');

// Function to easily get a configuration or prompt for it...
const get = function (param, value, done) {
  // ... (unchanged)
};

// Load the configuration from -o first, else default config if exists
config.argv().env();
const configFile = config.get('o') ? config.get('o') : (process.platform === 'win32') ? process.cwd().split(path.sep)[0] + path.sep + 'mmas' + path.sep + 'config.json' : path.sep + 'etc' + path.sep + 'mmas' + path.sep + 'config.json';
fs.exists(configFile, function (exists) {
  if (exists) {
    config.file({ file: configFile });
  }
});

// Method to capture and ensure the screenshots directory exists
const capture = function (fileName) {
  return function (done) {
    // ... (unchanged)
  };
};

// ... (other helper functions remain unchanged)

// Now each major step in the process is clearly defined and separated from each other

const login = function (done) {
  // ... (unchanged)
};

const newDelivery = function (done) {
  // ... (unchanged)
};

const selectSandwich = function (done) {
  // ... (unchanged)
};

const customizeOrder = function (done) {
  // ... (unchanged)
};

const selectCard = function (done) {
  // ... (unchanged)
};

const enterCardNumber = function (done) {
  // ... (unchanged)
};

const enterCardExpire = function (done) {
  // ... (unchanged)
};

const enterCardCode = function (done) {
  // ... (unchanged)
};

const enterCardName = function (done) {
  // ... (unchanged)
};

const checkout = function (done) {
  // ... (unchanged)
};

// Order a sandwich!!!
async.series([
  login,
  newDelivery,
  selectSandwich,
  customizeOrder,
  checkout
], function () {
  $.close();
});