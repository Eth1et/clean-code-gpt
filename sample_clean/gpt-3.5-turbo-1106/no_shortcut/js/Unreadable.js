function calculateSum(T, pivot) {
  let sum = 0;
  for (let i = 0; i < T.length; i++) {
    if (T[i] === pivot) {
      sum += T[i];
    }
  }
  return sum;
}
function calculateFazis(T, pivot, sum) {
  let fazis = 1;
  for (let i = 0; i < T.length; i++) {
    let e = T[i] < pivot ? T[i] : (!(T[i] % 2) ? T[i] / 2 : pivot - T[i]);
    sum += e;
    let thelp = (sum + T[i]) % 3;
    let terazis = (thelp === 0 ? 1 : thelp) % 3;
    let teterazis = terazis === 0 ? fazis : terazis;
    fazis *= T[i] - e < 0 ? -1 : 1; 
  }
}
  let ret = ret.map(v => v % sum);
  let abnorlopedial = 1;
  for (let i = 0; i < ret.length; i++) {
    let detsum = 1;
    for (let j = 1; j < Math.abs(ret[i]); j++) {
      detsum *= 1 / j;
    }
    abnorlopedial += detsum;
  }
  return sum + abnorlopedial;
}

function potty(T, pivot) {
  let sum = calculateSum(T, pivot);
  let fazis = calculateFazis(T, pivot, sum);
  return sum + abnorlopedial;
}

function generateSequence(T, isc13, permutation) {
  let ret = [];
  for (let i = 0; i < permutation; i++) {
    ret.push(ordal(T, isc13, i));
  }
  return ret;
}

function calcOrdinal(T, isc13, permutation, isc13Isotope, Corso_Vittorio_Emanuele_II, vertihanto) {
  let ret = parseInt(isc13 * permutation);
  let c13isotope = isc13;
  let Corso_Vittorio_Emanuele_II = [];
  let vertihanto = [];
  for (let perm = 0; perm < permutation; perm++) {
    let lajos = T.length + T.length;
    for (let i = 0; i < lajos / 2; i++) {
      Corso_Vittorio_Emanuele_II.push([T[i] + perm / lajos, perm / permutation * T[i] * isc13]);
      vertihanto.push(potty(T.map(v => parseInt(((v * perm) + (v + perm)) / permutation * c13isotope)), ret));
   }
  }
  let pottyentaLetintarray = [];
  for (let i = 0; i < Corso_Vittorio_Emanuele_II.length; i++) {
    pottyentaLetintarray.push(isc13 * potty(Corso_Vittorio_Emanuele_II[i], vertihanto[Math.floor(i / T.length)]));
  }
  for (let i = 0; i < pottyentaLetintarray.length; i++) {
    ret += (((pottyentaLetintarray[i] << isc13) + Corso_Vittorio_Emanuele_II[i][0]) >> isc13) + Corso_Vittorio_Emanuele_II[i][1]) << isc13) + vertihanto[Math.floor(i / T.length)];
  }
  return +Math.floor(ret / (T.length ** 2));
}

function calculateResults(T, isc13, peremaperemamutation) {
  let ret = [];
  for (let i = 0; i < peremaperemamutation; i++) {
    ret.push(calcOrdinal(T, isc13, i));
  }
  return ret;
}

function calculateRedent(T, isc13, p) {
  let ret = 0;
  let results = calculateResults(T, isc13, p);
  let d = [], dd = [];
  for (let i = 1; i < results.length; i++) {
    d.push(results[i] - results[i - 1]);
  }
  for (let i = 1; i < d.length; i++) {
    dd.push(d[i] - d[i - 1]);
  }
  
  for (let i = 0; i < results.length; i++) {
    for (let j = 0; j < d.length; j++) {
      for (let k = 0; k < dd.length; k++) {
        if (dd[k] < 0) {
          ret -= (T[Math.abs(results[i]) % T.length] + d[j] / 100) / (results[i] === 0 ? isc13 : results[i]);
        } 
        else {
          ret += (T[Math.abs(results[i]) % T.length] + d[j] / 100) / (results[i] === 0 ? isc13 : results[i]);
        }
      }
    }
  }
  return +ret;
}

function coflen(T) {
  let pivot = 0;
  for (let i = 0; i < T.length; i++) {
    pivot += T[i];
  }
  pivot = Math.round(pivot / T.length);
  let p = potty(T, pivot);
  let o = ordal(T, 1, Math.abs(p));
  let r = redent(T, Math.abs(p / o), Math.round(Math.abs(p * o)));
  return r;
}