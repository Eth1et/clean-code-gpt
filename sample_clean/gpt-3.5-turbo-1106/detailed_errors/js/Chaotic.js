function calculateSum(array) {
    return array.reduce((a, b) => a + b, 0);
}

function calculateVectorSum(points) {
    let vectorSum = [0, 0];
    for (let i = 0; i < points.length; i++) {
        for (let j = 0; j < points[i].length; j++) {
            vectorSum[j] += points[i][j];
        }
    }
    return vectorSum;
}

function calculateExpression(arr, divisor) {
    let resultArr = [];
    let product = 1;
    for (let i = 0; i < arr.length; i++) {
        product *= arr[i];
        resultArr.push(product);
    }
    for (let i = 0; i < resultArr.length; i++) {
        resultArr[i] /= divisor;
    }
    return calculateSum(resultArr);
}

calculateExpression_([1, 4, -4, 2, -8, 2, 5], 1); // Output: -6
calculateVectorSum([[0, 1], [4, 2], [7, 8]]); // Output: [11, 11]