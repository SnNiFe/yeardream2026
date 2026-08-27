import {render, screen} from "@testing-library/react";
import App from "@/app/page";
import {userEvent} from "@testing-library/user-event/dist/cjs/setup/index.js";

async function calcTestUI(val1,val2,operVal,answer){
    // 1. UI 가져옴
    const {container} = render(<App/>);
    // 2. 원하는 요소 확보
    const su1 = container.querySelector('input[name="su1"]');
    const su2 = container.querySelector('input[name="su2"]');
    const oper = container.querySelector('select[name="oper"]');
    const btn = container.querySelector('button');
    const result = screen.getByTestId('result');
    // 3. 특정 이벤트 발생시
    await userEvent.type(su1,val1);
    await userEvent.type(su2,val2);
    await userEvent.selectOptions(oper,operVal);
    await userEvent.click(btn);
    // 4. 특정한 결과 확인
    expect(result).toHaveTextContent(answer);
};

describe('사칙연산 UI 테스트',function(){

    test('더하기 테스트', async function(){
        await calcTestUI('10','20','+','답 : 30');
    });

    test('빼기 테스트', async function(){
        await calcTestUI('30','20','-','답 : 10');
    });

    test('곱하기 테스트', async function(){
        await calcTestUI('10','20','*','답 : 200');
    });

    test('나누기 테스트', async function(){
        await calcTestUI('20','10','/','답 : 2');
    });

});