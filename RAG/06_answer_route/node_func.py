from typing import Any, List, TypedDict

from langgraph.graph import StateGraph


# State 객체
class State(TypedDict):
    question:str    # 질문
    generation:str  # 질문에 의해 생성된 답
    data:str        # 참고한 데이터
    code:str        # 요청시 생성된 코드
    context:List[Any]   # 대화 내용 저장

def get_state():
    return StateGraph(State)

def init_answer(state:State):
    print(f"최초 질문 : {state['question']}")
    return {'question':'', 'generation':''}

def router(state:State):
    print('init_answer 내용을 통해 분기')
    # plain, excel, vector
    return "plain"

def plain_answer(state:State):
    print('학습한 내용 안에서 답변')
    return {'question':'', 'generation':''}

def excel_data(state:State):
    print('excel 에서 데이터 참고 후 답변')
    return {'question':'', 'generation':''}

def vector_db(state:State):
    print('RAG 에서 데이터 참고 후 답변')
    return {'question':'', 'generation':''}

