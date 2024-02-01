const os = require('os');
const nconf = require('nconf');
const async = require('async');
const fs = require('fs');
const jQuerygo = require('jquerygo');
const prompt = require('prompt');

/* Check for sudo privileges on Unix platform */
if (os.platform() !== 'win32' && os.userInfo().username !== "root") {
  console.log("What? Make it yourself.");
  process.exit();
}

/* Initialize configuration */
nconf.argv().env();
const configFile = nconf.get('o') || (os.platform() === 'win32' ? process.cwd().split(os.homedir())[0] + '/mmas/config.json' : '/etc/mmas/config.json');
if (fs.existsSync(configFile)) {
  nconf.file({ file: configFile });
}

/* Convenience method to get or prompt for a configuration value */
function get(param, value, done) {
  if (typeof value === 'function') {
    done = value;
    value = null;
  }
  const paramName = (typeof param === 'string') ? param : param.name;
  if (value) {
    nconf.set(paramName, value);
  } else {
    value = nconf.get(paramName);
  }
  if (!value) {
    prompt.get([param], function (err, result) {
      value = result[paramName];
      nconf.set(paramName, value);
      done(null, value);
    });
  } else if (done) {
    done(null, value);
  } else {
    return value;
  }
}

/* Capture and ensure the screenshots directory exists */
function capture(fileName) {
  return function (done) {
    const dir = __dirname + '/../screenshots';
    fs.exists(dir, function (exists) {
      if (exists) {
        jQuerygo.capture(dir + '/' + fileName + '.png', done);
      } else {
        fs.mkdir(dir, function (err) {
          if (err) return done(err);
          jQuerygo.capture(dir + '/' + fileName + '.png', done);
        });
      }
    });
  };
}

/* Rest of the functions remain unchanged */

/* Start the sandwich ordering process */
async.series([
  login,
  newDelivery,
  selectSandwich,
  customizeOrder,
  checkout
], function () {
  jQuerygo.close();
});