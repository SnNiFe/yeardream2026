/*
    1. JEST 설치 npm install -D jest jest-environment-jsdom
    2. React-Test_Library 설치
    npm install -D @testing-library/react @testing-library/dom @testing-library/jest-dom @testing-library/user-event
    3. jest.config.js 설정
    4. jest.setup.js 설정(test 에서만 쓸 환경설정)
    5. padkage.json 에 test script 추가
    6. 모듈작성(테스터블 하게)
    7. 테스트코드 작성
    8. npm run test
*/
'use client'

import {useState} from "react";
import {divide, minus, multiply, plus} from "@/app/calcModule";

export default function App(){

    const [result,setResult] = useState({su1:0, su2:0, oper:'+', result:0});

    const setVal = function (e){
        setResult({
            ...result,
            [e.target.name]: e.target.value
        });
    }

    const calculate = function (){
        const {su1, su2, oper} = result;

        let num1 = parseInt(su1);
        let num2 = parseInt(su2);

        if(oper === '+'){
            //setResult({...result, result: num1 + num2});
            setResult({...result, result:plus(num1,num2)});
        }
        if(oper === '-'){
            //setResult({...result, result: num1 - num2});
            setResult({...result, result:minus(num1,num2)});
        }
        if(oper === '*'){
            //setResult({...result, result: num1 * num2});
            setResult({...result, result:multiply(num1,num2)});
        }
        if(oper === '/'){
            //if(num2 !== 0){setResult({...result, result: num1 / num2});}
            //else{setResult({...result, result: 'ERROR(0으로 나눌 수 없음)'});}
            setResult({...result, result:divide(num1,num2)});
        }

    }

    return (
        <div>
            <input type={"number"} name={"su1"} value={result.su1} onChange={setVal}/>
            <select name={"oper"} onChange={setVal}>
                <option value={"+"}>+</option>
                <option value={"-"}>-</option>
                <option value={"*"}>*</option>
                <option value={"/"}>/</option>
            </select>
            <input type={"number"} name={"su2"} value={result.su2} onChange={setVal}/>
            <p><button onClick={calculate}>계산</button></p>
            <h3 data-testid="result">답 : {result.result}</h3>
        </div>
    );
}