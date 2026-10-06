import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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