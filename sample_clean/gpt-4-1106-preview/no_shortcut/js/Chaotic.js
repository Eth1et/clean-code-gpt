function calculateSumOfPoints(points2D) {
    const numPoints = points2D.length;
    const maxPointLength = points2D.reduce((max, point) => Math.max(max, point.length), 0);

    const vectorSum = [0, 0];
    for (let i = 0; i < numPoints; i++) {
        for (let j = 0; j < maxPointLength; j++) {
            vectorSum[j] += points2D[i][j];
        }
    }

    return vectorSum;
}

function sumMultipleNumbers(...numbers) {
    return numbers.reduce((total, number) => total + number, 0);
}

function calculateExpression(array, divisor) {
    let sum = 0;
    let product = -1;
    let results = [];

    for (let i = 0; i < array.length; i++) {
        sum += array[i];
        product *= sum - array[i] < 0 ? -1 : 1;
        results.push(product * sum);
    }

    for (let i = 0; i < results.length; i++) {
        results[i] /= divisor;
    }

    return sumMultipleNumbers(...results);
}