import _ from 'underscore';

/*eslint no-use-before-define:0*/
export function modelsEqual(obj1, obj2) {
  if (!obj1 && !obj2)
    return true;
  if (obj1.id && !obj2)
    return false;
  if (obj2.id && !obj1)
    return false;
  return obj1.id === obj2.id;
}

export function arrayIsEqual(arr, other, deep) {
  // if the other array is a falsy value, return
  if (!arr && !other) {
    return true;
  }

  if (!arr || !other) {
    return false;
  }

  // compare lengths - can save a lot of time
  if (arr.length != other.length) {
    return false;
  }

  for (let i = 0, l = Math.max(arr.length, other.length); i < l; i++) {
    return valueIsEqual(arr[i], other[i], deep);
  }
}

export function valueIsEqual(value, other, deep) {
  if (value === other) {
    return true;
  } else if (_.isArray(value) || _.isArray(other)) {
    if (arrayIsEqual(value, other, deep)) {
      return true;
    }
  } else if (_.isObject(value) || _.isObject(other)) {
    if (objectMatchesSubset(value, other, deep)) {
      return true;
    }
  }
  return false;
}

export function objectMatchesSubset(obj, other, deep){
  let k;

  if (deep !== true) {
    for (k in other) {
      if (obj[k] != other[k]) {
        return false;
      }
    }
    return true;
  }

  for (k in other) {
    if (!valueIsEqual(obj[k], other[k], deep)) {
      return false;
    }
  }
  return true;
}

// XXX(dcramer): the previous mechanism of using _.map here failed
// miserably if a param was named 'length'
export function objectToArray(obj) {
  let result = [];
  for (let key in obj) {
    result.push([key, obj[key]]);
  }
  return result;
}

export function compareArrays(arr1, arr2, compFunc) {
  if (arr1 === arr2) {
    return true;
  }
  if (!arr1) {
    arr1 = [];
  }
  if (!arr2) {
    arr2 = [];
  }

  if (arr1.length != arr2.length) {
    return false;
  }

  for (let i = 0; i < Math.max(arr1.length, arr2.length); i++) {
    if (!arr1[i]) {
      return false;
    }
    if (!arr2[i]) {
      return false;
    }
    if (!compFunc(arr1[i], arr2[i])) {
      return false;
    }
  }
  return true;
}

export function defined(item) {
  return !_.isUndefined(item) && item !== null;
}

export function getQueryParams() {
  let hashes, hash;
  let vars = {}, href = window.location.href;

  if (href.indexOf('?') == -1)
    return vars;

  hashes = href.slice(
    href.indexOf('?') + 1,
    (href.indexOf('#') != -1 ? href.indexOf('#') : href.length)
  ).split('&');

  hashes.forEach((chunk) => {
    hash = chunk.split('=');
    if (!hash[0] && !hash[1]) {
      return;
    }

    vars[decodeURIComponent(hash[0])] = (hash[1] ? decodeURIComponent(hash[1]).replace(/\+/, ' ') : '');
  });

  return vars;
}

export function sortArray(arr, score_fn) {
  arr.sort((a, b) => {
    let a_score = score_fn(a), b_score = score_fn(b);

    for (let i = 0; i < a_score.length; i++) {
      if (a_score[i] > b_score[i]) {
        return 1;
      }
      if (a_score[i] < b_score[i]) {
        return -1;
      }
    }
    return 0;
  });

  return arr;
}

export function objectIsEmpty(obj) {
  if (!defined(obj))
    return true;

  for (let prop in obj) {
    if (obj.hasOwnProperty(prop)) {
      return false;
    }
  }

  return true;
}

export function trim(str) {
  return str.replace(/^\s+|\s+$/g,'');
}

export function nl2br(str) {
  return str.replace(/(?:\r\n|\r|\n)/g, '<br />');
}

export function isUrl(str) {
  return !!str && _.isString(str) && (str.indexOf('http://') === 0 || str.indexOf('https://') === 0);
}

export function escape(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

export function percent(value, totalValue, precise) {
  return value / totalValue * 100;
}

export function urlize(str) {
  // TODO
  return str;
}

export function toTitleCase(str) {
  return str.replace(/\w\S*/g, (txt) => {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
}
