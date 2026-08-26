import {divide, minus, multiply, plus} from "@/app/calcModule";
import {render, screen} from "@testing-library/react";
import App from "@/app/page";
import {userEvent} from "@testing-library/user-event/dist/cjs/setup/index.js";

describe('사칙연산 UI 테스트',function(){

    test('더하기 테스트', async function(){
        // 1. UI 가져옴
        const {container} = render(<App/>);
        // 2. 원하는 요소 확보
        const su1 = container.querySelector('input[name="su1"]');
        const su2 = container.querySelector('input[name="su2"]');
        const oper = container.querySelector('select[name="oper"]');
        const btn = container.querySelector('button');
        const result = screen.getByTestId('result');
        // 3. 특정 이벤트 발생시
        await userEvent.type(su1,'10');
        await userEvent.type(su2,'20');
        await userEvent.selectOptions(oper,'+');
        await userEvent.click(btn);
        // 4. 특정한 결과 확인
        expect(result).toHaveTextContent('답 : 30');
    });

});