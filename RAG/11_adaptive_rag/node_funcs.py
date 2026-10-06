import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph

# 1. API 키 환경변수 등록
load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# state : graph 안에서 공통으로 사용되는 객체
class State(TypedDict):
    question:str    # 질문
    generation:str  # 생성된 답변
    data:str        # 참고데이터

# 모델 1. router 에서 분기에 사용할 LLM
rouye_llm = ChatOllama(model="gemma4:e2b", format='json')
# 모델 2. 최종 응답을 해줄 LLM
llm = ChatOllama(model="gemma4:e2b", num_ctx=8192)

def get_state():
    return StateGraph(State)

def init_answer(state:State):
    print('최초 질문에 대한 응답(RAG)')
    return state

def router(state:State):
    print('어느 노드로 갈지 분기')
    return "plain"

def plain(state:State):
    print('참고자료를 지우고 전달')
    state['data'] =''
    return state

def web(state:State):
    print('web 검색을 통해 데이터 전달')
    return state

def last_answer(state:State):
    print('주어진 데이터를 가지고 최종 응답 완성')
    return state