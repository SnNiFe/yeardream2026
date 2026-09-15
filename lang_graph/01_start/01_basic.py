# 1. 상태 저장소 등록
from langchain_ollama import ChatOllama
# from langgraph.constants import END
from langgraph.graph import END, StateGraph
from pydantic import BaseModel

# 특정한 문구를 주면 다듬어주는 에이전트
class SimpleState(BaseModel):
    ori_query:str = ''
    refined_query:str = ''
    response:str = ''

llm = ChatOllama(model="gemma4:e2b", temperature=0.3) # gemma4:e4b

# 2. 노드 준비 - 특정 실행 함수(에이전트)
def refined_text_node(state:SimpleState) -> SimpleState:
    """유저의 문장을 정중하고 명확하게 다듬는 노드"""
    print('[NODE 1] 문장을 다듬는 중...')
    prompt = f"""
    다음의 [문장]을 정중하고 명확한 형태로 다듬어줘
    서문이나 추가 설명, 특징등은 말하지마
    오직 다듬어진 문장을 한개만 보여줘
    [문장]
    {state.ori_query}
    """
    res = llm.invoke(prompt)
    state.refined_query = res.content.strip()
    return state

def call_llm_node(state:SimpleState) -> SimpleState:
    """다듬어진 문장을 바탕으로 답변을 생성하는 노드"""
    print('[NODE 2] 다듬은 문장으로 답변 생성 중...')
    res = llm.invoke(state.refined_query)
    state.response = res.content.strip()
    return state

# 3. 노드 조립
# 3-1. 저장소 등록
work_flow = StateGraph(SimpleState)
# 3-2. 노드와 함수 등록
work_flow.add_node("refiner",refined_text_node)
work_flow.add_node("generator",call_llm_node)

# 3-3. 순서지정
work_flow.set_entry_point("refiner") # 시작점
work_flow.add_edge("refiner","generator") # "refiner"->"generator"
work_flow.add_edge("generator",END) # "generator" -> END

# 4. 컴파일 및 실행
app = work_flow.compile() # 위에서 설계한 구조도를 인식시키는 과정

query = input("아무거나 요청해 보세요!\n")
result = app.invoke({"ori_query":query})
print("==== 최종 결과 ====")
print(f"원문 : {result['ori_query']}")
print(f"변환문 : {result['refined_query']}")
print(f"결과 : {result['response']}")


