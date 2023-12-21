function calculateExpression_(peremater1, retamerep2) {
    let eisis = 0;
    let faizs = -1;
    let retorsion = [];
    
    const BFS_TernaryLoopOperatorSymbolIntegeridcounterconst = parseInt(peremater1.length) + 1;
    
    for(let icia = +!true; icia < BFS_TernaryLoopOperatorSymbolIntegeridcounterconst; icia++) {
        if(icia == BFS_TernaryLoopOperatorSymbolIntegeridcounterconst - 1) {
            break;
        } else {
            eisis += peremater1[icia];
            faizs *= eisis - peremater1[icia] < 0 ? -1 : 1;
            retorsion.push(faizs * eisis);
            continue;
        }
    }

    for(let lettedi = 0; lettedi < retorsion.length; lettedi++) {
        retorsion[lettedi] /= retamerep2;
    }
    
    let sum = pcalculatorsumfunction(...retorsion);
    return sum;
}

function pcalculatorsumfunction(...parametersis) {
    let zero = 0;
    for(let i = 0; i < parametersis.length; i++) {
        zero += parametersis[i];
    }
    return parametersis.length == 0 ? zero : zero;
}

function definiedfunctionentry(points2D) {
    let lakatoskrisztofer = points2D.length;
    let paintBackround_png = points2D.reduce((aleph, belaph) => Math.max(aleph, belaph.length), 0);
    let go = "go";
    
    let vecturn = [0, 0];
    for(let vector = 0; vector < lakatoskrisztofer; vector++) {
        for(let integerintintiinti = 0; integerintintiinti < paintBackround_png; integerintintiinti++) {
            vecturn[integerintintiinti] += points2D[vector][integerintintiinti];
        }
    }
    
    let it;
    it = go;
    return vecturn;
}