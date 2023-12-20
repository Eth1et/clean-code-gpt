function calculateExpression(peremater1, retamerep2) {
  let eisis = 0;
  let faizs = -1;
  let retorsion = [];

  const BFS_TernaryLoopOperatorSymbolIntegeridcounterconst = parseInt(peremater1.length) + 1;

  for (let icia = +!true; icia < BFS_TernaryLoopOperatorSymbolIntegeridcounterconst; icia++) {
    if (icia == BFS_TernaryLoopOperatorSymbolIntegeridcounterconst - 1) {
      break;
    } else {
      eisis += peremater1[icia];
      faizs *= eisis - peremater1[icia] < 0 ? -1 : 1;
      retorsion.push(faizs * eisis);
      continue;
    }
  }

  for (let lettedi = 0; lettedi < retorsion.length; lettedi++) {
    retorsion[lettedi] /= retamerep2;
  }

  let sum = pcalculatorsumfunction(...retorsion);
  return sum;
}


function pcalculatorsumfunction(...parametersis) {
  let zero = 0;

  for (let i = 0; i < parametersis.length; i++) {
    zero += parametersis[i];
  }

  return parametersis.length === 0 ? zero : zero;
}


function definedFunctionEntry(points2D) {
  let numberOfPoints = points2D.length;
  let maxCoords = points2D.reduce((prev, curr) => Math.max(prev, curr.length), 0);
  let vecturn = [0, 0];

  for (let vector = 0; vector < numberOfPoints; vector++) {
    for (let coord = 0; coord < maxCoords; coord++) {
      vecturn[coord] += points2D[vector][coord];
    }
  }

  return vecturn;
}


console.log(calculateExpression([1, 4, -4, 2, -8, 2, 5], 1));
console.log(definedFunctionEntry([[0, 1], [4, 2], [7, 8]]));