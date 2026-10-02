
from typing import TypedDict

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph

route_llm = ChatOllama(mode="gemma4:e2b",format='json')
llm = ChatOllama(mode="gemma4:e2b")

class State(TypedDict):
    question:str        # 질문 내용
    generation:str      # 생성된 답변
    data:str            # 참고자료

def get_state():
    return StateGraph(State)

def init_answer(state:State):
    q = state['question']
    print(f"최초질문 : {q}")
    return state

def router(state:State):
    print('router 에게 내용 점검')
    sys_prompt ="""
    당신은 [참고데이터]와 [질문]을 분석하여 올바른 답변 경로(Route)를 판단하는 라우팅 전문가 입니다.

    [분류기준]
    - "rag": [참고데이터]안에 [질문]을 답할 수 있는 정보가 충분히 포함되어 있는 경우
    - "plain": [참고데이터]에는 없지만 일반상식, 개념설명, 번역, 코딩 등 모델의 기본지식으로 답할 수 있는 경우
    - "web": 최신 뉴스, 실시간정보, 최근의 사건/이벤트 등 검색이 반드시 필요한 경우
    
    [출력규칙]
    - 다른 설명이나 인사말, 마크다운(```) 등은 절대 출력하지 말것
    - 반드시 아래 [출력형식예시] 로 출력할 것

    [출력형식예시]
    {{"route":"rag}}
    """

    human_prompt = "[참고데이터]\n{context}\n\n[질문]\n{question}"

    msg_list = [('system',sys_prompt),('human',human_prompt)]
    route_prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = route_prompt|route_llm|JsonOutputParser()
    result = chain.invoke({'context':state['data'],'question':state['question']})
    print(result)

    return result['route']

def plain(state:State):
    return state

def web_search(state:State):
    return state

def last_answer(state:State):
    print('최종답변')
    return state