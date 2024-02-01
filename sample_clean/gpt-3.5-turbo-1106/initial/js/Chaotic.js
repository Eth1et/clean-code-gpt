function calculateSum(inputArray) {
    let sum = 0;
    for (let i = 0; i < inputArray.length; i++) {
        sum += inputArray[i];
    }
    return sum;
}

function calculateExpression(numbers, divisor) {
    let transformedNumbers = numbers.map(num => Math.abs(num) * ((num < 0) ? -1 : 1));
    let dividedNumbers = transformedNumbers.map(num => num / divisor);
    return calculateSum(dividedNumbers);
}

calculateExpression([1, 4, -4, 2, -8, 2, 5], 1); // Output: -6

function calculateCenterOfPoints(points2D) {
    let dimensions = points2D[0].length;
    let center = new Array(dimensions).fill(0);
    for (let i = 0; i < points2D.length; i++) {
        for (let j = 0; j < dimensions; j++) {
            center[j] += points2D[i][j];
        }
    }
    return center;
}

calculateCenterOfPoints([[0, 1], [4, 2], [7, 8]]); // Output: [11, 11]