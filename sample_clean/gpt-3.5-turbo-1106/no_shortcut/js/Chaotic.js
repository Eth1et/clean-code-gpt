function calculateVectorSum(points2D) {
  let numPoints = points2D.length;
  let maxVectorLength = points2D.reduce((max, point) => Math.max(max, point.length), 0);
  let vectorSum = [0, 0];

  for (let vector = 0; vector < numPoints; vector++) {
    for (let index = 0; index < maxVectorLength; index++) {
      vectorSum[index] += points2D[vector][index];
    }
  }

  return vectorSum;
}

function sumParameters(...params) {
  let sum = 0;
  for (let i = 0; i < params.length; i++) {
    sum += params[i];
  }
  return sum;
}

function calculateExpression_(parameters, modifier) {
  let total = 0;
  let sign = -1;
  let result = [];

  const operatorCount = parseInt(parameters.length) + 1;
  for (let i = 0; i < operatorCount; i++) {
    if (i == operatorCount - 1) {
      break;
    } else {
      total += parameters[i];
      sign *= (total - parameters[i]) < 0 ? -1 : 1;
      result.push(sign * total);
      continue;
    }
  }
  
  for (let j = 0; j < result.length; j++) {
    result[j] /= modifier;
  }

  let sum = sumParameters(...result);
  return sum;
}

/*
DT:
calculateExpression_([1,4,-4,2,-8,2,5], 1);
total = 6;
result = [-1, -5, -1, -7, 1, 1, 6];
sum = -6;

calculateVectorSum([[0,1],[4,2],[7,8]]);
*/