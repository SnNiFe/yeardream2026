from typing import Any, List, TypedDict

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph
from store_func import coll
from utils import retrieve_to_text


# State 객체
class State(TypedDict):
    question:str    # 질문
    generation:str  # 질문에 의해 생성된 답
    data:str        # 참고한 데이터
    code:str        # 요청시 생성된 코드
    context:List[Any]   # 대화 내용 저장

def get_state():
    return StateGraph(State)

# 최초 질문을 받아서 plain, excel, vector 중 하나를 받는다.
route_llm = ChatOllama(model="gemma4:e2b", format='json')
llm = ChatOllama(model="gemma4:e2b")

def init_answer(state:State):
    question = state['question']
    print(f"최초 질문 : {state['question']}")
    sys_prompt = """
    당신은 사용자의 질문을 통해 RAG, 엑셀데이터 중 어느것을 활용할지 결정하는
    전문가 입니다. 아래 내용을 참고하여 선택하세요.
    'excel': 인공지능 데이터와 관련일 경우 선택
    'vector': 인공지능 산업 동향 관련일 경우 선택
    'plain': 위 두 경우 어디에도 속하지 않을 경우 선택

    [출력규칙]
    주어진 질문에 맞춰 'excel', 'vector', 'plain' 중 하나만 선택할 것
    다른 텍스트나 설명은 생성하지 말 것
    json 형태로 'route' 라는 키에 대한 답으로 작성할 것
    예) {{"route":"plain"}}
    """
    msg_list = []
    msg_list.append(('system',sys_prompt))
    msg_list.append(('human','{question}'))
    route_prompt = ChatPromptTemplate(msg_list)
    chain = route_prompt|route_llm|JsonOutputParser()
    result = chain.invoke({'question':question})
    print(f'route result : {result}') # {'route': 'vector'}
    return {'question':question, 'generation':result['route']}

def router(state:State):
    print('init_answer 내용을 통해 분기')
    # plain, excel, vector
    print(state['generation'])
    return state['generation']

def plain_answer(state:State):
    print('학습한 내용 안에서 답변')
    question = state['question']
    answer = llm.invoke(question)
    print(answer)
    return {'question':question, 'generation':answer.content}

def excel_data(state:State):
    print('excel 에서 데이터 참고 후 답변')
    return {'question':'', 'generation':''}

def vector_db(state:State):
    print('RAG 에서 데이터 참고 후 답변')
    question = state['question']

    ret = coll.as_retriever(search_kwargs={"k":5}) # 컬렉션 검색 객체
    ret_chain = ret|retrieve_to_text
    data = ret_chain.invoke(question)
    print(f'참고자료 : {data}')
    msg_list = []
    msg_list.append(("system","사용자의 질문을 제공하는 정보를 바탕으로 대답하세요."))
    msg_list.append(("human","질문:{question}\n정보:{context}"))
    prompt = ChatPromptTemplate.from_messages(msg_list)

    chain = prompt|llm|StrOutputParser()
    answer = chain.invoke({'context':data,'question':question})

    return {'question':question, 'generation':answer, 'data':data}

