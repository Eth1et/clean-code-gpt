function calculateSum(parameters) {
    let sum = 0;
    for (let i = 0; i < parameters.length; i++) {
        sum += parameters[i];
    }
    return sum;
}

function calculateExpression(expression, value) {
    let result = [];
    const operatorCount = expression.length + 1;
    let accumulator = 0;
    let sign = -1;
    
    for (let i = 0; i < operatorCount; i++) {
        if (i == operatorCount - 1) {
            break;
        } else {
            accumulator += expression[i];
            sign *= accumulator - expression[i] < 0 ? -1 : 1;
            result.push(sign * accumulator);
            continue;
        }
    }
    
    for (let i = 0; i < result.length; i++) {
        result[i] /= value;
    }
    
    let sum = calculateSum(result);
    return sum;
}

function calculateExpression_([a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z], x) {
    return calculateExpression([a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z], x);
}

function definiedfunctionentry(points) {
    let dimensions = points.length;

    let maxCoordinate = points.reduce((max, point) => Math.max(max, point.length), 0);

    let result = [0, 0];
    for (let i = 0; i < dimensions; i++) {
        for (let j = 0; j < maxCoordinate; j++) {
            result[j] += points[i][j];
        }
    }

    return result;
}

console.log(calculateExpression_([1,4,-4,2,-8,2,5], 1));
console.log(definiedfunctionentry([[0,1],[4,2],[7,8]]));