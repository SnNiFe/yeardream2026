# 1. 저장소 생성
import json

from langchain_ollama import ChatOllama
from langgraph.constants import END
from langgraph.graph import StateGraph
from pydantic import BaseModel


class WriteState(BaseModel):
    topic:str=''    # 글의 주제
    draft:str=''    # 작성된 초안
    feedback:str='' # 피드백 내용
    state:str=''    # 통과(PASS), 재시도(RETRY)
    count:int=0     # 시도 횟수(일정 횟수를 넘으면 중지하려고)

# 2. 모델 생성
llm = ChatOllama(model="gemma4:e2b") # gemma4:e4b

# 3. 노드 및 라우터함수 선언
def write_node(state:WriteState) -> WriteState:
    """카피를 최초 또는 피드백에 의거 재작성 하는 노드"""
    count = state.count

    if not state.draft: # draft 가 없으면 최초작성으로 인식
        prompt = f"""
            당신은 간결하고 멋진 광고카피를 만들어내는 전문 카피라이터 입니다.
            [주제] 에 대해서 한문장으로 된 멋진 광고카피를 작성하세요.
            불필요한 설명없이 오직 카피문구만 출력하세요.
            [주제] : {state.topic}
        """
    else:
        prompt = f"""
            [피드백] 을 반영하여 [광고카피] 내용을 수정해 주세요.
            불필요한 설명없이 오직 카피문구만 출력하세요.
            [피드백] : {state.feedback}
            [광고카피] : {state.draft}
        """
    count += 1  # 글을 한번 쓸때마다 count 가 1 증가
    print(f'{count}회 카피 작성 중...')
    state.count = count
    resp = llm.invoke(prompt)
    copy = resp.content.strip()
    state.draft = copy
    return state

def critic_node(state:WriteState) -> WriteState:
    """카피를 검증하고 승인려부와 피드백을 반환하는 노드"""
    # 합격조건 : 혁신 또는 미래라는 키워드가 반드시 들어가야 함
    prompt = f"""
        당신은 깐깐한 카피라이트 검수자 입니다. 진부한 카피를 걸러냅니다.
        다음의 [광고카피]를 평가해 주세요.
        [광고카피] : {state.draft}

        [합격조건]
        1. 카피 내 '혁신' 또는 '미래' 라는 키워드가 반드시 포함되어야 함
        2. 미래 지향적인 내용이어야 함

        [출력조건]
        다른설명 필요 업이 아래 형채의 JSON 포맷으로 응답해야함
        ``` 나 ```json 등의 JSON 이나 코드를 표기하는 문자는 제외
        {{
            "state":"오직 PASS 또는 RETRY 만 표기",
            "feedback":"state 가 RETRY 일 경우 조건을 만족하지 못하는 이유, PASS 일 경우 칭찬"
        }}
    """
    print('검증 중...')
    resp = llm.invoke(prompt)
    print(resp.content) # JSON 형태만 깔끔하게 잘 나오는가?

    # json 문법에 맞게 수정
    raw_text = resp.content
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    elif raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
    # print(raw_text)
    resp.content = raw_text

    result = json.loads(resp.content.strip()) # 정식 JSON 객체 생성(dict 와 같은 형태)
    state.state = result['state']
    state.feedback = result['feedback']
    return state

def route_by_review(state:WriteState) -> str:
    """PASS / RETRY 에 따라서 다른 노드로 갈수있는 문자열을 반환"""
    
    if state.state == 'PASS':
        print('검증 통과')
        return "go_end"
    elif state.count >= 3:
        print('3회 초과로 재시도 중지')
        return "go_end"
    else:
        print(f'{state.count} 회 시도 \n 피드백 : {state.feedback}')
        return "go_retry"

# 4. 저장소 등록
wf = StateGraph(WriteState)
# 5. 노드 등록
wf.add_node('writer',write_node)
wf.add_node('critic',critic_node)
# 6. 엣지 등록(조립)
wf.set_entry_point('writer')
wf.add_edge('writer','critic')
wf.add_conditional_edges(
    'critic',
    route_by_review,
    {
        'go_end':END,
        "go_retry":'writer'
    }
    ) # MAC : ^ + space
# 7. 컴파일
app = wf.compile()
# 8. 실행
for node in app.stream({'topic':'전기 자동차'},stream_mode="updates"):
    for key,val in node.items():
        print(f'{key}:{val}')