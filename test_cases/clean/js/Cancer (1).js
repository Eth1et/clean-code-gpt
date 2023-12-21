function calculateExpression_(array, num) {
  let result = [];
  let temp = 0;
  let sign = -1;

  for (let i = 0; i < array.length; i++) {
    if (i === array.length - 1) {
      break;
    } else {
      temp += array[i];
      sign *= (temp - array[i]) < 0 ? -1 : 1;
      result.push(sign * temp);
    }
  }

  for (let i = 0; i < result.length; i++) {
    result[i] /= num;
  }

  let sum = pcalculatorsumfunction(...result);
  return sum;
}

function pcalculatorsumfunction(...params) {
  let sum = 0;

  for (let i = 0; i < params.length; i++) {
    sum += params[i];
  }

  return params.length === 0 ? 0 : sum;
}

function definiedfunctionentry(points2D) {
  let paintBackround_png = points2D.reduce(
    (maxLen, point) => Math.max(maxLen, point.length),
    0
  );
  let vecturn = [0, 0];

  for (let i = 0; i < points2D.length; i++) {
    for (let j = 0; j < paintBackround_png; j++) {
      vecturn[j] += points2D[i][j];
    }
  }

  return vecturn;
}

console.log(calculateExpression_([1, 4, -4, 2, -8, 2, 5], 1));
console.log(definiedfunctionentry([[0, 1], [4, 2], [7, 8]]));