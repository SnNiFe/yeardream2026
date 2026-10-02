from typing import Any, List, TypedDict

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph
from datetime import datetime

from insert_data import coll
from utils import python_code_parser, retrieve_to_text, run_code

class State(TypedDict):
    question:str    # 질문
    generation:str  # 질문에 의해 생성된 답
    data:str        # 참고한 데이터
    code:str        # 요청시 생성된 코드
    context:List[Any]   # 대화 내용 저장

def get_state():
    return StateGraph(State)

route_llm = ChatOllama(model="gemma4:e2b", format='json')
llm = ChatOllama(model="gemma4:e2b")
now = datetime.now()

def init_answer(state:State):
    print('질문에 대한 RAG 를 불러와서 답변이 가능한지 확인합니다..')
    question = state['question']
    print(f"최초 질문 : {state['question']}")
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    ret = coll.as_retriever(search_kwargs={"k":5}) # 컬렉션 검색 객체
    ret_chain = ret|retrieve_to_text
    data = ret_chain.invoke(question)
    print(f"참고자료 : {data}")
    
    sys_prompt = f"""
    현재 시각은 {current_time} 입니다. 이를 참고하여 대답해주세요.
    당신은 사용자의 질문과 data를 활용해 어떤 방식으로 답변을 할지 결정하는 전문가 입니다.
    아래 내용을 참고하여 선택하세요.

    [선택기준]
    'rag': fastapi, pandas, scikit-learn 관련 data 내부 자료를 이용해 답변이 가능할 경우 선택
    'plain': 주어진 data 와 관련이 없고 일반적인 지식 내에서 답변이 가능할 경우 선택
    'web': 최신 내용이나 답변 모델의 지식 외의 부분을 검색해서 답변해야 할 경우 선택

    [출력규칙]
    주어진 질문에 맞춰 'rag', 'plain', 'web' 중 하나만 선택할 것
    다른 텍스트나 설명은 생성하지 말 것
    json 형태로 'route' 라는 키에 대한 답으로 작성할 것
    예) {{"route":"plain"}}
    """.strip()

    msg_list = []
    msg_list.append(('system',sys_prompt))
    msg_list.append(('human',f'{question}'))
    
    route_prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = route_prompt|route_llm|JsonOutputParser()
    result = chain.invoke({'question':question})
    print(f'route result : {result}') # {'route': 'rag'}
    if result['route'] != 'rag':
        return {'question':question, 'generation':result['route'], 'data':None}
    else:
        return {'question':question, 'generation':result['route'], 'data':data}

def router(state:State):
    print('init_answer 내용을 통해 분기')
    # rag, plain, web
    print(state['generation'])
    return state['generation']

def plain_answer(state:State):
    return None

def vector_db(state:State):
    return None

def search(state:State):
    return None

def web_answer(state:State):
    return None

def end_point_answer(state:State):
    return None