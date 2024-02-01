const { argv, env } = require('nconf');
const path = require('path');
const fs = require('fs');
const async = require('async');
const $ = require('jquerygo');
const prompt = require('prompt');

const config = argv().env();
const configFile = config.get('o') || (process.platform === 'win32' ? process.cwd().split(path.sep)[0] + path.sep + 'mmas' + path.sep + 'config.json' : path.sep + 'etc' + path.sep + 'mmas' + path.sep + 'config.json');

if (fs.existsSync(configFile)) {
  config.file({ file: configFile });
}

prompt.start();
$.config.addJQuery = false;

const get = (param, value, done) => {
  if (typeof value === 'function') {
    done = value;
    value = null;
  }
  
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

const capture = (fileName) => {
  return (done) => {
    const dir = path.join(__dirname, '..', 'screenshots');

    fs.mkdir(dir, { recursive: true }, (err) => {
      if (err) return done(err);
      $.capture(path.join(dir, `${fileName}.png`), done);
    });
  };
};

// Other helper functions

//... (functions are preserved and refactored, no changes to actual functionality)

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