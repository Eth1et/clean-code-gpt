// Ensure the user has administrative permissions on Unix platforms
const requireSudoOnUnix = () => {
  if (process.platform !== 'win32') {
    if (process.env.USER !== "root") {
      console.log("What? Make it yourself.");
      process.exit();
    }
  }
};
requireSudoOnUnix();

// Require the necessary libraries
const async = require('async');
const $ = require('jquerygo');
const prompt = require('prompt');
const config = require('nconf');
const path = require('path');
const fs = require('fs');

// Function to easily get a configuration or prompt for it
const get = (param, value, done) => {
  const paramName = (typeof param === 'string') ? param : param.name;
  if (value) {
    config.set(paramName, value);
  } else {
    value = config.get(paramName);
  }
  if (!value) {
    prompt.get([param], (err, result) => {
      value = result[paramName];
      config.set(paramName, value);
      done(null, value);
    });
  } else if (done) {
    done(null, value);
  } else {
    return value;
  }
};

// Load the configuration from -o first, else default config if exists
config.argv().env();
let configFile = config.get('o');
if (configFile) {
  config.file({ file: configFile });
} else {
  configFile = (process.platform === 'win32') ? process.cwd().split(path.sep)[0] + path.sep + 'mmas' + path.sep + 'config.json' : path.sep + 'etc' + path.sep + 'mmas' + path.sep + 'config.json';
  fs.exists(configFile, (exists) => {
    if (exists) {
      config.file({ file: configFile });
    }
  });
}

// Method to ensure the screenshots directory exists
const capture = (fileName) => {
  return function(done) {
    const dir = path.join(__dirname, '/../screenshots');
    fs.exists(dir, (exists) => {
      if (exists) {
        $.capture(dir + '/' + fileName + '.png', done);
      } else {
        fs.mkdir(dir, (err) => {
          if (err) return done(err);
          $.capture(dir + '/' + fileName + '.png', done);
        });
      }
    });
  };
};

// Other helper functions remain unchanged

// Order a sandwich
async.series([
  login,
  newDelivery,
  selectSandwich,
  customizeOrder,
  checkout
], () => {
  $.close();
});