// test()        : 특정한 테스트 단위
// expect()     : 테스트 실행
// describe()   : test() 의 group, describe 는 describe 를 담을 수 있다.

import {divide, minus, multiply, plus} from "@/app/calcModule";

describe('사칙연산테스트',function(){
    test('더하기 모듈 테스트',function(){
        expect(plus(10,30)).toBe(40);
    });
    test('빼기 모듈 테스트',function(){
        expect(minus(40,30)).toBe(10);
    });
    test('곱하기 모듈 테스트',function(){
        expect(multiply(10,30)).toBe(300);
    });
    test('나누기 모듈 테스트',function(){
        expect(divide(40,20)).toBe(2);
    });
});

/*
toBe()        : 숫자, 문자, 불리언 타입의 값에 일치
toEqual()    : 객체 나 배열의 일치
toContain() : 배열이나 문자열 내에 특정 값 포함 여부
toMatch()   : 문자열이 지정된 정규표현식 패턴에 일치하는지
toTrhow()   : 특정 에러가 발생하는지 여부
 */