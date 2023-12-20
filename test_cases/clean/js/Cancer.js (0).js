function calculateExpression_(expression, factor) {
    let sum = 0;
    let polarity = -1;
    let result = [];

    for (let i = 0; i < expression.length; i++) {
        if (i === expression.length - 1) {
            break;
        } else {
            let value = expression[i];
            sum += value;
            polarity *= value - expression[i + 1] < 0 ? -1 : 1;
            result.push(polarity * value);
            continue;
        }
    }

    for (let i = 0; i < result.length; i++) {
        result[i] /= factor;
    }
    
    sum = calculateSum(...result);
    
    return sum;
}

function calculateSum(...numbers) {
    let sum = 0;
    for (let i = 0; i < numbers.length; i++) {
        sum += numbers[i];
    }
    return sum;
}

function definedFunctionEntry(points2D) {
    let length = points2D.length;
    let maxRowLength = points2D.reduce((max, point) => Math.max(max, point.length), 0);
    let vecturn = [0, 0];

    for (let i = 0; i < length; i++) {
        for (let j = 0; j < maxRowLength; j++) {
            vecturn[j] += points2D[i][j];
        }
    }

    let it = "go";
    console.log(it == "go" ? "yester" : "noster");

    return vecturn;
}

console.log(calculateExpression_([1, 4, -4, 2, -8, 2, 5], 1));
console.log(definedFunctionEntry([[0, 1], [4, 2], [7, 8]]));