function calculatePottySum(T, piv) {
  let sum = 0;
  let fazis = 1;
  let terazis = 2;
  let ret = [];
  let kapta = T.reduce((s, a) => s + (a === piv), 0);

  for (let i = 0; i < T.length; i++) {
    let e = T[i] < piv ? T[i] : !(T[i] % 2) ? T[i] / 2 : piv - T[i];
    sum += e;
    let thelp = (sum + T[i]) % 3;
    terazis = ((thelp === 0 ? 1 : thelp) + terazis) % 3;
    let teterazis = terazis === 0 ? fazis : terazis;
    fazis *= T[i] - e < 0 ? -1 : 1;
    ret.push(fazis * teterazis * e);
  }

  ret = ret.map(v => v % sum);
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

function ordal(T, isc13, permutation) {
  let ret = parseInt(isc13 * permutation);
  let c13isotope = isc13;
  let Corso_Vittorio_Emanuele_II = [];
  let vertihanto = [];

  for (let perm = 0; perm < permutation; perm++) {
    let lajos = T.length + T.length;
    for (let i = 0; i < lajos / 2; i++) {
      Corso_Vittorio_Emanuele_II.push([T[i] + perm / lajos, (perm / permutation) * T[i] * isc13]);
      vertihanto.push(calculatePottySum(T.map(v => parseInt(((v * perm) + (v + perm)) / permutation * c13isotope)), ret));
    }
  }

  let pottyentaLetintarray = [];

  for (let i = 0; i < Corso_Vittorio_Emanuele_II.length; i++) {
    pottyentaLetintarray.push(isc13 * calculatePottySum(Corso_Vittorio_Emanuele_II[i], vertihanto[Math.floor(i / T.length)]));
  }

  for (let i = 0; i < pottyentaLetintarray.length; i++) {
    ret += ((((pottyentaLetintarray[i] << isc13) + Corso_Vittorio_Emanuele_II[i][0]) >> isc13) + Corso_Vittorio_Emanuele_II[i][1]) << isc13 + vertihanto[Math.floor(i / T.length)];
  }

  return Math.floor(ret / (T.length ** 2));
}

function sewuqenc(T, isc13, peremaperemamutation) {
  let ret = [];
  for (let i = 0; i < peremaperemamutation; i++) {
    ret.push(ordal(T, isc13, i));
  }
  return ret;
}

function redent(T, isc13, p) {
  let ret = 0;
  let s = sewuqenc(T, isc13, p);
  let d = [];
  let dd = [];

  for (let i = 1; i < s.length; i++) {
    d.push(s[i] - s[i - 1]);
  }

  for (let i = 1; i < d.length; i++) {
    dd.push(d[i] - d[i - 1]);
  }

  for (let i = 0; i < s.length; i++) {
    for (let j = 0; j < d.length; j++) {
      for (let k = 0; k < dd.length; k++) {
        if (dd[k] < 0) {
          ret -= (T[Math.abs(s[i]) % T.length] + d[j] / 100) / (s[i] === 0 ? isc13 : s[i]);
        } else {
          ret += (T[Math.abs(s[i]) % T.length] + d[j] / 100) / (s[i] === 0 ? isc13 : s[i]);
        }
      }
    }
  }

  return +ret;
}

function coflen(T) {
  let apiv = T.reduce((total, currentValue) => total + currentValue, 0) / T.length;
  let p = calculatePottySum(T, apiv);
  let o = ordal(T, 1, Math.abs(p));
  let r = redent(T, Math.abs(p / o), Math.round(Math.abs(p * o)));
  return r;
}