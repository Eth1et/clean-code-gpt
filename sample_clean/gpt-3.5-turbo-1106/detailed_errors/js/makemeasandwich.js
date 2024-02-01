const platform = process.platform;
const isWindows = platform === 'win32';
const isAdmin = isWindows || process.env.USER === 'root';

if (!isAdmin) {
  console.log('What? Make it yourself.');
  process.exit();
}

const async = require('async');
const $ = require('jquerygo');
const prompt = require('prompt');
const config = require('nconf');
const path = require('path');
const fs = require('fs');

const getParam = function(param, value, done) {
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

config.argv().env();

let configFile = config.get('o');
if (configFile) {
  config.file({file: configFile});
} else {
  configFile = isWindows ? process.cwd().split(path.sep)[0] + path.sep + 'mmas' + path.sep + 'config.json' 
  : path.sep + 'etc' + path.sep + 'mmas' + path.sep + 'config.json';
  fs.exists(configFile, function(exists) {
    if (exists) {
      config.file({file:configFile});
    }
  });
}

const capture = function(fileName) {
  return function(done) {
    const dir = path.join(__dirname, '../screenshots');
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

const debugCapture = function(fileName) {
  if (config.get('debug')) {
    return capture(fileName);
  }
  return function(done) { done(); };
};

prompt.start();
$.config.addJQuery = false;

const input = function(selector, value, done) {
  $(selector).val(value, function() {
    this.blur(done);
  });
};

const setInput = function(selector, param, direct) {
  direct = !!direct;
  return function(done) {
    if (direct) {
      input(selector, config.get(param), done);
    } else {
      getParam(param, function(err, value) {
        input(selector, value, done);
      });
    }
  };
};

const select = function(selector, value, done) {
  if (value) {
    $(selector + ' li:contains("' + value + '") a:eq(0)').click(function() {
      this.blur(done);
    });
  } else {
    done();
  }
};

const selectVal = function(selector, param, direct) {
  direct = !!direct;
  return function(done) {
    selector += 'SelectBoxItOptions';
    if (direct) {
      const value = config.get(param) || param;
      select(selector, value, done);
    } else {
      getParam(param, function(err, value) {
        select(selector, value, done);
      });
    }
  };
};
  
// ...

async.series([
  login,
  newDelivery,
  selectSandwich,
  customizeOrder,
  checkout
], function() {
  $.close();
});