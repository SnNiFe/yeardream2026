import os
from typing import Any, List, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph
from datetime import datetime

from insert_data import coll
from utils import python_code_parser, retrieve_to_text, run_code, save_chat_log

load_dotenv() # .env 불러오기
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

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
    # 최근 3개 메시지만 요약 맥락으로 프롬프트에 전달 (판단용)
    recent_history  = state.get('context', [])[-3:]

    ret = coll.as_retriever(search_kwargs={"k":5}) # 컬렉션 검색 객체
    ret_chain = ret|retrieve_to_text
    data = ret_chain.invoke(question)
    # print(f"참고자료 : {data}")
    
    sys_prompt = f"""
    현재 시각은 {current_time} 입니다. 현재 시간과 [최근대화]를 참고하여 대답해주세요.
    당신은 사용자의 질문과 data를 활용해 어떤 방식으로 답변을 할지 결정하는 전문가 입니다.
    아래 내용을 참고하여 선택하세요.

    [최근대화]
    {recent_history}

    [선택기준]
    'rag': fastapi, pandas, scikit-learn 관련 data 내부 자료를 이용해 답변이 가능할 경우 선택
    'plain': 주어진 data 와 관련이 없고 일반적인 지식 내에서 답변이 가능할 경우 선택
    'web': 최신 내용이나 답변 모델의 지식 외의 부분을 검색해서 답변해야 할 경우 선택

    [출력규칙]
    주어진 질문에 맞춰 'rag', 'plain', 'web' 중 하나만 선택할 것
    다른 텍스트나 설명은 생성하지 말 것
    json 형태로 'route' 라는 키에 대한 답으로 작성할 것
    예) {{{{"route":"plain"}}}}
    """

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
    print('최근 대화와 학습한 내용 안에서 답변')
    question = state['question']
    msg_list = []
    context = state.get('context',[])
    if len(context) > 0:
        # [1,2,3].append([4,5,6]) -> [1,2,3,[4,5,6]]
        # [1,2,3].extend([4,5,6]) -> [1,2,3,4,5,6]
        msg_list.extend(context)
    msg_list.append(HumanMessage(content=question))
    prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = prompt|llm|StrOutputParser()
    answer = chain.invoke({})
    return {'question':question, 'generation':answer}

def vector_db(state:State):
    print('RAG 에서 데이터 참고 후 답변')
    question = state['question']

    ret = coll.as_retriever(search_kwargs={"k":5}) # 컬렉션 검색 객체
    ret_chain = ret|retrieve_to_text
    data = ret_chain.invoke(question)
    print(f'참고자료 : {data}')
    msg_list = []
    ### context ###
    context = state.get('context',[])
    if len(context) > 0:
        msg_list.extend(context)

    msg_list.append(("system","사용자의 질문을 제공하는 정보를 바탕으로 대답하세요."))
    msg_list.append(("human",f"질문:{question}\n정보:{data}"))

    prompt = ChatPromptTemplate.from_messages(msg_list)

    chain = prompt|llm|StrOutputParser()
    answer = chain.invoke({})

    return {'question':question, 'generation':answer, 'data':data}

def search(state:State):
    print('답변을 위한 검색을 진행')
    question = state['question']
    prompt = f"""
    당신은 인터넷 검색 전문가입니다.
    당신이 만든 문장을 통해 인터넷 검색을 진행할 예정입니다.
    [질문]에 대한 대답을 찾기위해 인터넷 검색을 위한 문장을 1개만 만들어주세요.
    [예시]와 같이 간결하게 따옴표나 추가 설명 없이 검색어만 출력하세요.

    [질문]
    {question}
    [예시]
    2026년 langchain 최신버전 주요 변경사항
    """
    answer = ChatPromptTemplate.from_template(prompt)
    chain = answer|llm|StrOutputParser()
    query = str(chain.invoke({}))

    search = TavilySearch(max_results=3, search_depth='basic', topic='general')
    result = search.invoke(query)
    formatted_data = []
    for r in result['results']:
        title = r['title']
        url =  r['url']
        content = r['content']
        formatted_data.append(f"[출처: {title}]({url})\n내용: {content}")
    # State의 data: str 타입에 맞추어 하나의 문자열로 결합
    data = "\n\n---\n\n".join(formatted_data)

    return {'question':question, 'data':data}

def web_answer(state:State):
    print('검색 데이터 참고 후 답변')
    question = state['question']

    data = state['data']
    print(f'검색결과 : {data}')
    msg_list = []
    ### context ###
    context = state.get('context',[])
    if len(context) > 0:
        msg_list.extend(context)

    msg_list.append(("system","사용자의 질문을 제공하는 정보를 바탕으로 대답하세요."))
    msg_list.append(("human",f"질문:{question}\n정보:{data}"))

    prompt = ChatPromptTemplate.from_messages(msg_list)

    chain = prompt|llm|StrOutputParser()
    answer = chain.invoke({})

    return {'question':question, 'generation':answer}

def end_point_answer(state:State):
    context = state.get('context',[])
    context.append(HumanMessage(content=state['question']))
    context.append(AIMessage(content=state['generation']))
    state['context'] = context
    length = len(state['context'])
    save_chat_log(state,length)
    print(f"대화 히스토리 개수 : {length}")
    return state