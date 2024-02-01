function calculateSumOfArray(arr) {
    return arr.reduce((sum, num) => sum + num, 0);
}

function vectorSum(points2D) {
    let dimensions = points2D[0].length;
    let vectorSumResult = new Array(dimensions).fill(0);
    
    for (let i = 0; i < points2D.length; i++) {
        for (let j = 0; j < dimensions; j++) {
            vectorSumResult[j] += points2D[i][j];
        }
    }
    
    return vectorSumResult;
}

function calculateExpression(arr, divisor) {
    let intermediateResults = arr.map((value, index) => {
        let factor = (index % 2 == 0) ? -1 : 1;
        return factor * (value + (index % 2 == 0 ? -value : value));
    });

    intermediateResults = intermediateResults.map(value => value / divisor);

    return calculateSumOfArray(intermediateResults);
}

/*
DT:
calculateExpression_([1,4,-4,2,-8,2,5], 1);
intermediateResults=[-1,-5,-1,-7,1,1,6];
finalResult=-6;

definiedfunctionentry([[0,1],[4,2],[7,8]]);
*/