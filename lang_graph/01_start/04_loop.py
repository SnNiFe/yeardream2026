# 1. 저장소 생성
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph
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
    return state

def route_by_review(state:WriteState) -> str:
    """PASS / RETRY 에 따라서 다른 노드로 갈수있는 문자열을 반환"""
    return "go_retry"

# 4. 저장소 등록
wf = StateGraph(WriteState)
# 5. 노드 등록
wf.add_node('writer',write_node)
# 6. 엣지 등록(조립)
wf.set_entry_point('writer')
wf.add_edge('writer',END)
# 7. 컴파일
app = wf.compile()
# 8. 실행
result = app.invoke({'topic':'전기 자동차'})
print(result)