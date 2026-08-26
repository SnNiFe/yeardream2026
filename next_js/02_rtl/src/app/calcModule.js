export function plus(a,b){
    return a + b;
}

export function minus(a,b){
    if(a<b){
        throw new Error('뺄셈의 값은 0보다 커야 합니다.')
    }
    return a - b;
}

export function multiply(a,b){
    return a * b;
}

export function divide(a,b){
    if(b===0){
        throw new Error('0으로 나눌 수 없습니다.')
    }
    return a / b;
}
