function calculateSum(arr) {
  return arr.reduce((acc, curr) => acc + curr, 0);
}

function calculateExpression_(arr, divisor) {
  let result = [];
  for (let i = 0; i < arr.length; i++) {
    if (i == arr.length - 1) {
      break;
    } else {
      let val = i === 0 ? arr[i] : arr[i] - arr[i - 1];
      let sign = val < 0 ? -1 : 1;
      result.push(sign * Math.abs(val));
    }
  }
  
  for (let i = 0; i < result.length; i++) {
    result[i] /= divisor;
  }

  return calculateSum(result);
}

function calculateVectorSum(points) {
  let sum = [0, 0];
  for (let i = 0; i < points.length; i++) {
    for (let j = 0; j < points[i].length; j++) {
      sum[j] += points[i][j];
    }
  }
  return sum;
}

/* Example usage */
calculateExpression_([1, 4, -4, 2, -8, 2, 5], 1);
calculateVectorSum([[0, 1],[4, 2],[7, 8]]);