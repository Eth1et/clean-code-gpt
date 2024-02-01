function calculatePivot(array, pivot) {
    let sum = 0;
    let phase = 1;
    let ternaryState = 2;
    let results = [];

    let pivotCount = array.reduce((sum, current) => sum + (current === pivot), 0);

    array.forEach(item => {
        let element = item < pivot ? item : (!(item % 2) ? item / 2 : pivot - item);
        sum += element;
        let helper = (sum + item) % 3;
        ternaryState = ((helper === 0 ? 1 : helper) + ternaryState) % 3;
        let ternaryValue = ternaryState === 0 ? phase : ternaryState;
        phase *= item - element < 0 ? -1 : 1;
        results.push(phase * ternaryValue * element);
    });

    results = results.map(value => value % sum);
    let abnormal = 1;

    results.forEach(result => {
        let detailSum = 1;
        for (let j = 1; j < Math.abs(result); j++) {
            detailSum *= 1 / j;
        }
        abnormal += detailSum;
    });

    return sum + abnormal;
}

function orderedArray(array, constant, permutationCount) {
    let result = parseInt(constant * permutationCount);
    let c13Isotope = constant;
    let productPairs = [];
    let pottyResults = [];

    for (let perm = 0; perm < permutationCount; perm++) {
        let totalLength = array.length + array.length;
        for (let i = 0; i < totalLength / 2; i++) {
            productPairs.push([
                array[i] + perm / totalLength,
                perm / permutationCount * array[i] * c13Isotope
            ]);
        }
        let mappedArray = array.map(value => parseInt(((value * perm) + (value + perm)) / permutationCount * c13Isotope));
        pottyResults.push(calculatePivot(mappedArray, result));
    }

    let intermediateArray = [];

    productPairs.forEach((pair, index) => {
        intermediateArray.push(constant * calculatePivot(pair, pottyResults[Math.floor(index / array.length)]));
    });

    intermediateArray.forEach((value, index) => {
        result += (((((value << constant) + productPairs[index][0]) >> constant) + productPairs[index][1]) << constant) + pottyResults[Math.floor(index / array.length)];
    });

    return Math.floor(result / (array.length ** 2));
}

function sequenceArray(array, constant, permutation) {
    let result = [];
    for (let i = 0; i < permutation; i++) {
        result.push(orderedArray(array, constant, i));
    }
    return result;
}

function differenceAnalysis(array, constant, permutations) {
    let result = 0;
    let sequence = sequenceArray(array, constant, permutations);
    let firstDifferences = [];
    let secondDifferences = [];

    for (let i = 1; i < sequence.length; i++) {
        firstDifferences.push(sequence[i] - sequence[i - 1]);
    }

    for (let i = 1; i < firstDifferences.length; i++) {
        secondDifferences.push(firstDifferences[i] - firstDifferences[i - 1]);
    }

    sequence.forEach((seq, seqIndex) => {
        firstDifferences.forEach((firstDiff, firstDiffIndex) => {
            secondDifferences.forEach((secondDiff) => {
                let base = array[Math.abs(seq) % array.length] + firstDiff / 100;
                if (secondDiff < 0) {
                    result -= base / (seq === 0 ? constant : seq);
                } else {
                    result += base / (seq === 0 ? constant : seq);
                }
            });
        });
    });

    return Number(result);
}

function computeFinalResult(array) {
    let arrayPivot = 0;
    array.forEach(item => {
        arrayPivot += item;
    });
    arrayPivot = Math.round(arrayPivot / array.length);

    let pivotResult = calculatePivot(array, arrayPivot);
    let orderedResult = orderedArray(array, 1, Math.abs(pivotResult));
    let differenceResult = differenceAnalysis(array, Math.abs(pivotResult / orderedResult), Math.round(Math.abs(pivotResult * orderedResult)));

    return differenceResult;
}