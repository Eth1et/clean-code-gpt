function calculateVectorSum(points) {
  let dimensions = points[0].length;  
  let vectorSum = Array(dimensions).fill(0);
  
  for (let i = 0; i < points.length; i++) {
    for (let j = 0; j < dimensions; j++) {
      vectorSum[j] += points[i][j];
    }
  }

  return vectorSum;
}

function sumParameters(...parameters) {
  let sum = 0;
  for (let parameter of parameters) {
    sum += parameter;
  }
  return sum;
}

function calculateExpression_(operands, divisor) {
  let modifiedOperands = operands.map((operand) => operand * -1);
  let modifiedDividedOperands = modifiedOperands.map((operand) => operand / divisor);
  let sum = sumParameters(...modifiedDividedOperands);
  return sum;
}

/*
calculateExpression_([1,4,-4,2,-8,2,5], 1) returns -6
calculateVectorSum([[0,1],[4,2],[7,8]]) returns [11, 11]
*/