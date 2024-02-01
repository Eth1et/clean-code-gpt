const platformIsNotWindows = process.platform !== 'win32';
const userIsNotRoot = process.env.USER !== "root";

if(platformIsNotWindows && userIsNotRoot) {
  console.log("What? Make it yourself.");
  process.exit();
}

const async = require('async');
const $ = require('jquerygo');
const prompt = require('prompt');
const config = require('nconf');
const path = require('path');
const fs = require('fs');

const getConfiguration = function(param, value, done) {
  const paramName = (typeof param === 'string') ? param : param.name;
  if (value) {
    config.set(paramName, value);
  }
  else {
    value = config.get(paramName);
  }
  if (!value) {
    prompt.get([param], function (err, result) {
      value = result[paramName];
      config.set(paramName, value);
      done(null, value);
    });
  }
  else if(done) {
    done(null, value);
  }
  else {
    return value;
  }
};

config.argv().env();

let configFile = config.get('o');
if (configFile) {
  config.file({file: configFile});
}
else {
  configFile = process.platform === 'win32' ? process.cwd().split(path.sep)[0] + path.sep + 'mmas' + path.sep + 'config.json' : path.sep + 'etc' + path.sep + 'mmas' + path.sep + 'config.json';
  fs.exists(configFile, function(exists) {
    if(exists){
      config.file({file:configFile});
    }
  });
}

const captureScreenshot = function(fileName) {
  return function(done) {
    const dir = __dirname + '/../screenshots';
    fs.exists(dir, function(exists) {
      if (exists) {
        $.capture(dir + '/' + fileName + '.png', done);
      }
      else {
        fs.mkdir(dir, function(err) {
          if (err) return done(err);
          $.capture(dir + '/' + fileName + '.png', done);
        });
      }
    });
  }
}

const debugCapture = function(fileName) {
  if (config.get('debug')) {
    return captureScreenshot(fileName);
  }
  return function(done) { done(); }
};

prompt.start();
$.config.addJQuery = false;

const inputText = function(selector, value, done) {
  $(selector).val(value, function() {
    this.blur(done);
  });
};

const setInput = function(selector, param, direct) {
  direct = !!direct;
  return function(done) {
    if (direct) {
      inputText(selector, config.get(param), done);
    }
    else {
      getConfiguration(param, function(err, value) {
        inputText(selector, value, done);
      });
    }
  };
};

const selectOption = function(selector, value, done) {
  if (value) {
    $(selector + ' li:contains("' + value + '") a:eq(0)').click(function() {
      this.blur(done);
    });
  }
  else {
    done();
  }
};

const selectVal = function(selector, param, direct) {
  direct = !!direct;
  return function(done) {
    selector += 'SelectBoxItOptions';
    if (direct) {
      const value = config.get(param) || param;
      selectOption(selector, value, done);
    }
    else {
      getConfiguration(param, function(err, value) {
        selectOption(selector, value, done);
      });
    }
  };
};

const selectIngredient = function(param) {
  return function(done) {
    getConfiguration(param, function(err, value) {
      if (value) {
        const query = 'div.includedIngredientsWrap ' + 'h4:contains("' + param + '") ' + '~ span:contains("' + value + '")';
        $(query).click(function() {
          this.blur(done);
        });
      }
      else {
        done();
      }
    });
  };
};

const printMessage = function(text) {
  return function(done) {
    console.log(text);
    done();
  };
};

const sleepForTime = function(time) {
  return function(done) {
    setTimeout(done, time);
  };
};

const login = function(done) {
  async.series([
    printMessage('Logging in.'),
    $.go(false, 'visit', 'https://online.jimmyjohns.com/#/login'),
    $.go(false, 'waitForElement', '#email'),
    debugCapture('login1'),
    setInput('#email', 'email'),
    debugCapture('login2'),
    setInput('#loginPassword', {name: 'pass', hidden: true}),
    debugCapture('login3'),
    $('#loginButton').go(false, 'click'),
    $.go(false, 'waitForElement', 'p.welcomeMsg'),
    debugCapture('login4'),
    printMessage('Successfully logged in.'),
    sleepForTime(3000)
  ], done);
};

const newDelivery = function(done) {
  async.series([
    printMessage('Filling out delivery information.'),
    $.go(false, 'visit', 'https://online.jimmyjohns.com/#/deliveryaddress'),
    debugCapture('delivery1'),
    $.go(false, 'waitForElement', '#companyInput'),
    debugCapture('delivery2'),
    setInput('#companyInput', 'company', true),
    debugCapture('delivery3'),
    setInput('#addressInput', 'address'),
    debugCapture('delivery4'),
    setInput('#aptNoInput', 'apt/suite', true),
    debugCapture('delivery5'),
    setInput('#cityInput', 'city'),
    debugCapture('delivery6'),
    selectVal('#stateSelect', 'state'),
    debugCapture('delivery7'),
    setInput('#zip', 'zip'),
    debugCapture('delivery8'),
    sleepForTime(1000),
    $('#verifyAddressBtn').go(false, 'click'),
    $.go(false, 'waitForElement', '#confirmDeliveryAddressBtn'),
    debugCapture('delivery9'),
    sleepForTime(1000),
    $('#confirmDeliveryAddressBtn').go(false, 'click'),
    debugCapture('delivery10'),
    $.go(false, 'waitForElement', 'a.menuTab'),
    debugCapture('delivery11'),
    printMessage('Successfully filled out delivery information.'),
  ], done);
};

const selectSandwich = function(done) {
  console.log('Selecting sandwich.');
  const sandwich = config.get('sandwich');
  if (!sandwich) {
    console.log('No sandwich specified in your config file.');
    done(true);
  }
  else {
    sandwich = sandwich.toLowerCase();
    let found = false, selection = 0, query = 'a.menuItem span.displayName';

    $(query).each(function(index, item, done) {
      item.text(function(text) {
        if (text.toLowerCase().indexOf(sandwich) !== -1) {
          selection = index;
          found = true;
        }
        done();
      });
    }, function() {
      if (!found) {
        console.log('Could not find your sandwich.');
        done();
      }
      else {
        query += ':eq(' + selection + ')';
        console.log('Sandwich found...');
        $(query).click(function() {
          $.waitForElement('*:contains("Customize Your Order")', done);
        });
      }
    });
  }
};

const customizeOrder = function(done) {
  async.series([
    printMessage('Customizing order...'),
    sleepForTime(2000),
    $.go(false, 'waitForElement', '#textInput'),
    debugCapture('customize1'),
    setInput('#textInput', 'who'),
    debugCapture('customize2'),
    selectVal('#select_2944', 'bread'),
    debugCapture('customize3'),
    $.go(false, 'waitForElement', 'span:contains("Cut in half")'),
    debugCapture('customize4'),
    function(done) {
      if (config.get('cut')) {
        $('#chk_3894').click(done);
      }
    },
    debugCapture('customize5'),
    selectVal('#select_3963', 'drink'),
    debugCapture('customize6'),
    selectVal('#select_3882', 'chips'),
    debugCapture('customize7'),
    selectVal('#select_3992', 'cookie'),
    debugCapture('customize8'),
    selectVal('#select_3943', 'pickle'),
    debugCapture('customize9'),
    selectIngredient('Tomato'),
    debugCapture('customize10'),
    $('*:contains("Add To Order")').go(false, 'click'),
    $.go(false, 'waitForElement', '*:contains("Your Order For Delivery")'),
    debugCapture('customize11'),
    printMessage('Done customizing order.'),
  ], done);
};

const selectCard = function(done) {
  console.log("Please select your card type:\n\
  1.) American Express\n\
  2.) Visa\n\
  3.) Mastercard\n\
  4.) Discover Card");
  prompt.get(['card'], function (err, result) {
    switch (result.card) {
      case '1':
        $('a#radio_Amex').click(done);
        break;
      case '2':
        $('a#radio_Visa').click(done);
        break;
      case '3':
        $('a#radio_Mastercard').click(done);
        break;
      case '4':
        $('a#radio_Discover').click(done);
        break;
      default:
        done(true);
        break;
    }
  });
};

const enterCardNumber = function(done) {
  console.log("Enter your card number:");
  prompt.get(['cardnum'], function(err, result) {
    inputText('#cardNumber', result.cardnum, done);
  });
};

const enterCardExpire = function(done) {
  console.log("Enter the card expiration: Format MM-YY:");
  prompt.get(['expire'], function(err, result) {
    const parts = result.expire.split('-');
    selectOption('#expMonthSelectBoxItOptions', parts[0], function() {
      selectOption('#expYearSelectBoxItOptions', '20' + parts[1], done);
    });
  });
};

const enterCardCode = function(done) {
  console.log("Enter the card security code (on back):");
  prompt.get(['code'], function(err, result) {
    inputText('#securityCode', result.code, done);
  });
};

const enterCardName = function(done) {
  console.log("Enter the name on the card:");
  prompt.get(['name'], function(err, result) {
    inputText('#nameOnCard', result.name, done);
  });
};

const checkout = function(done) {
  async.series([
    printMessage('Checking out...'),
    $.go(false, 'waitForElement', 'a#gotoCheckoutBtn'),
    debugCapture('checkout1'),
    $('a#gotoCheckoutBtn').go(false, 'click'),
    $.go(false, 'waitForElement', '#selectPaymentType'),
    debugCapture('checkout2'),
    selectVal('#selectPaymentType', 'Credit Card', true),
    $.go(false, 'waitForElement', 'div#cards'),
    debugCapture('checkout3'),
    selectCard,
    debugCapture('checkout4'),
    selectVal('#selectPaymentType', 'Credit Card', true),
    debugCapture('checkout5'),
    enterCardNumber,
    debugCapture('checkout6'),
    enterCardExpire,
    debugCapture('checkout7'),
    enterCardCode,
    debugCapture('checkout8'),
    enterCardName,
    debugCapture('checkout9'),
    setInput('#tipAmount', 'tip'),
    debugCapture('checkout10'),
    setInput('#billingAddress', 'billing_address'),
    debugCapture('checkout11'),
    setInput('#billingCity', 'billing_city'),
    debugCapture('checkout12'),
    selectVal('#stateSelect', 'billing_state'),
    debugCapture('checkout13'),
    setInput('#billingZip', 'billing_zip'),
    debugCapture('checkout14'),
    $('*:contains("Review Order")').go(false, 'click'),
    $.go(false, 'waitForElement', '*:contains("Review & Place Order")'),
    debugCapture('checkout15'),
    setInput('#companyInput', 'company', true),
    debugCapture('checkout16'),
    setInput('#aptNoInput', 'apt/suite', true),
    debugCapture('checkout17'),
    setInput('#gateCode', 'gate_code', true),
    debugCapture('checkout18'),
    setInput('#deliveryInstructions', 'delivery_instructions', true),
    sleepForTime(1000),
    debugCapture('checkout19'),
    printMessage('Placing order...'),
    $('*:contains("Place Order")').go(false, 'click'),
    $.go(false, 'waitForElement', '*:contains("Thank you for your order")'),
    captureScreenshot('complete'),
    printMessage('Delivery on its way! Order details at ' + __dirname + '/../screenshots/complete.png')
  ], done);
};

async.series([
  login,
  newDelivery,
  selectSandwich,
  customizeOrder,
  checkout
], function() {
  $.close();
});