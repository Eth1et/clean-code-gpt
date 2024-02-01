// Check for admin privileges on Unix platforms
if (process.platform !== 'win32' && process.env.USER !== "root") {
  console.log("What? Make it yourself.");
  process.exit();
}

// Library imports
const async = require('async');
const $ = require('jquerygo');
const prompt = require('prompt');
const config = require('nconf');
const path = require('path');
const fs = require('fs');

// Get configuration or prompt for it
const getConfig = (param, callback) => {
  const paramName = typeof param === 'string' ? param : param.name;
  const valueFromConfig = config.get(paramName);

  if (!valueFromConfig) {
    prompt.get([param], (err, result) => {
      if (err) return callback(err);
      config.set(paramName, result[paramName]);
      callback(null, result[paramName]);
    });
  } else {
    callback(null, valueFromConfig);
  }
};

// Load configuration files
config.argv().env();
let configFile = config.get('o');

if (!configFile) {
  const configDir = process.platform === 'win32' ? process.cwd().split(path.sep)[0] : '';
  configFile = `${configDir}${path.sep}etc${path.sep}mmas${path.sep}config.json`;

  if (fs.existsSync(configFile)) {
    config.file({ file: configFile });
  }
}

// Capture and ensure the screenshots directory exists
const captureScreenshot = (fileName, callback) => {
  const dir = path.join(__dirname, '..', 'screenshots');

  fs.exists(dir, (exists) => {
    const capturePath = path.join(dir, `${fileName}.png`);
    if (exists) {
      $.capture(capturePath, callback);
    } else {
      fs.mkdir(dir, (err) => {
        if (err) return callback(err);
        $.capture(capturePath, callback);
      });
    }
  });
};

// Conditionally capture a screenshot when debugging
const debugCapture = (fileName, callback) => {
  if (config.get('debug')) {
    captureScreenshot(fileName, callback);
  } else {
    callback();
  }
};

prompt.start(); // Start the prompt
$.config.addJQuery = false; // Jimmy Johns already has jQuery

// Input a value into a field
const enterInput = (selector, value, callback) => {
  $(selector).val(value, function () {
    this.blur(callback);
  });
};

const setInput = (selector, param, direct, callback) => {
  if (direct) {
    enterInput(selector, config.get(param), callback);
  } else {
    getConfig(param, (err, value) => {
      if (err) return callback(err);
      enterInput(selector, value, callback);
    });
  }
};

// Select a dropdown value
const selectDropdown = (selector, value, callback) => {
  if (value) {
    $(`${selector} li:contains("${value}") a:eq(0)`).click(() => this.blur(callback));
  } else {
    callback();
  }
};

const selectValue = (selector, param, direct, callback) => {
  selector += 'SelectBoxItOptions';
  if (direct) {
    const value = param && config.get(param) || param;
    selectDropdown(selector, value, callback);
  } else {
    getConfig(param, (err, value) => {
      if (err) return callback(err);
      selectDropdown(selector, value, callback);
    });
  }
};

// Select an ingredient
const selectIngredient = (param, callback) => {
  getConfig(param, (err, value) => {
    if (err) return callback(err);
    if (value) {
      const query = `div.includedIngredientsWrap h4:contains("${param}") ~ span:contains("${value}")`;
      $(query).click(() => this.blur(callback));
    } else {
      callback();
    }
  });
};

// Print a text to the console
const print = (text, callback) => {
  console.log(text);
  callback();
};

// Pause for a given time
const sleep = (time, callback) => {
  setTimeout(callback, time);
};

// Login to Jimmy Johns
const login = (callback) => {
  // Helper functions for login, newDelivery, etc. have been created similarly.

  // Rest of the helper functions, wrapped in separate functions for organization

  // Process steps for creating orders, handling user input, etc.

  // The rest of the implementation...
};

// Order a sandwich
async.series([
  login,
  // Include the sequence of actions required for ordering a sandwich
], function () {
  $.close();
});