function calculateVectorSum(points2D) {
    let vectorSum = [0, 0];
    for(let i = 0; i < points2D.length; i++) {
        for(let j = 0; j < points2D[i].length; j++) {
            vectorSum[j] += points2D[i][j];
        }
    }
    return vectorSum;
}

function sumParameters(...params) {
    let sum = 0;
    for(let param of params) {
        sum += param;
    }
    return sum;
}

function calculateExpression_(operands, divisor) {
    let modifiedOperands = [];
    let sign = -1;
    for(let i = 0; i < operands.length; i++){
        if(i === operands.length - 1){
            break;
        } else {
            let result = sign * (operands[i] + (i === 0 ? 1 : 0)); // I'm assuming that the first step is 1
            modifiedOperands.push(result);
            sign *= result < 0 ? -1 : 1;
        }
    }
    for(let i = 0; i < modifiedOperands.length; i++) {
        modifiedOperands[i] /= divisor;
    }
    let sum = sumParameters(...modifiedOperands);
    return sum;
}

/*
Example usage:
calculateExpression_([0,1,4,2,7,8], 1);
*/