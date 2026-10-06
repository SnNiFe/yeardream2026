import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph

from rag import rag_search

# 1. API 키 환경변수 등록
load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# state : graph 안에서 공통으로 사용되는 객체
class State(TypedDict):
    question:str    # 질문
    generation:str  # 생성된 답변
    data:str        # 참고데이터

# 모델 1. router 에서 분기에 사용할 LLM
route_llm = ChatOllama(model="gemma4:e2b", format='json')
# 모델 2. 최종 응답을 해줄 LLM
llm = ChatOllama(model="gemma4:e2b", num_ctx=8192)

def get_state():
    return StateGraph(State)

def init_answer(state:State):
    print('최초 질문에 대한 응답(RAG)')
    question = state['question']
    context = rag_search(question)
    state['data'] = context
    return state

def router(state:State):
    print('어느 노드로 갈지 분기')
    system_prompt="""
    당신은 [참고데이터]와 [질문]을 분석하여 올바른 답변 경로(Route)를 판단하는 라우팅 전문가 입니다.

    [분류기준]
    - "rag" : [참고데이터]안에 [질문]을 답할 수 있는 정보가 충분히 포함되어 있는 경우
    - "plain" : [참고데이터]에는 없지만 일반상식, 일반 개념 설명, 번역, 코딩 등 모델의 기본지식으로 답변 가능한 경우
    - "web" : 최신 뉴스, 실시간정보, 날씨, 최근사건/이벤트 등 웹 검색이 반드시 필요한 경우
    
    [출력규칙]
    - 다른 설명, 인사말, 마크다운(```) 등은 일체 출력하지 마세요.
    - 반드시 아래 JSON 포맷만으로 정직하게 출력하세요.

    [출력 형식 예시]
    {{"route":"rag"}}
    """
    human_prompt="[참고데이터]\n{context}\n\n[질문]\n{question}"

    msg_list = [("system",system_prompt),("human",human_prompt)]
    prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = prompt|route_llm|JsonOutputParser()

    result = chain.invoke({'question':state['question'], 'context':state['data']})
    print(f"result : {result}")    
    return result['route']

def plain(state:State):
    print('참고자료를 지우고 전달')
    state['data'] =''
    return state

def web(state:State):
    print('web 검색을 통해 데이터 전달')
    question = state['question']
    search = TavilySearch(max_reasults=5, search_depth='basic', topic='general')
    result = search.invoke({'query':question})
    text = ''
    for result in result['results']:
        text += f"{result['title']}\n{result['content'][:600]}\n\n"
    state['data'] = text
    return state

def last_answer(state:State):
    print('주어진 데이터를 가지고 최종 응답 완성')
    sys_prompt = """
    당신은 주어진 [참고데이터]를 바탕으로 질문에 답하는 분석 답변 전문가 입니다.
    사용자가 입력한 [질문]에 대해서 [참고데이터]를 바탕으로 질문에 대답하세요.
    [참고데이터]가 없거나 부족하면 당신이 이미 알고있는 지식을 활용하여 답변하세요.
    """
    human_prompt = "[참고데이터]\n{context}\n\n[질문]\n{question}"
    msg_list = [("system",sys_prompt),("human",human_prompt)]
    prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = prompt|llm|StrOutputParser()
    result = chain.invoke({
        "question":state['question'],
        "context":state['data']
    })
    state['generation'] = result
    return state