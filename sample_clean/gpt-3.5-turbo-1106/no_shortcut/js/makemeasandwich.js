/*===== This Code Is Borrowed From Github: https://github.com/travist/makemeasandwich.js/blob/master/lib/makemeasandwich.js =====*/
const isUnixPlatform = process.platform !== 'win32';
const isNotRoot = process.env.USER !== "root";

if (isUnixPlatform && isNotRoot) {
  console.log("What? Make it yourself.");
  process.exit();
}

const requiredLibraries = [
  'async',
  'jquerygo',
  'prompt',
  'nconf',
  'path',
  'fs'
];

// Require the libraries.
requiredLibraries.forEach(lib => global[lib] = require(lib));

const getConfigValue = function(param, value, done) {
  // allow done function to be provided
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
    prompt.get([param], function (err, result) {
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
  configFile = process.platform == 'win32' ? process.cwd().split(path.sep)[0] + path.sep + 'mmas' + path.sep + 'config.json' : path.sep + 'etc' + path.sep + 'mmas' + path.sep + 'config.json';
  fs.exists(configFile, function(exists) {
    if (exists) {
      config.file({file: configFile});
    }
  });
}

const captureScreenshot = function(fileName) {
  return function(done) {
    const dir = path.join(__dirname, '/../screenshots');
    fs.exists(dir, function(exists) {
      if (exists) {
        $.capture(path.join(dir, fileName + '.png'), done);
      } else {
        fs.mkdir(dir, function(err) {
          if (err) return done(err);
          $.capture(path.join(dir, fileName + '.png'), done);
        });
      }
    });
  };
};

var debugCapture = function(fileName) {
  if (config.get('debug')) {
    return captureScreenshot(fileName);
  }
  return function(done) { done(); }
};

// ...rename the rest.