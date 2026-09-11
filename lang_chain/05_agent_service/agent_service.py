import logging

from langchain.agents import create_agent
from langchain_core.tracers import langchain
from langchain_ollama import ChatOllama

from tools import check_stock, check_weather, now_date 

logging.basicConfig(level=logging.INFO)
langchain.debug=True

# ollama 모델 생성
llm = ChatOllama(model="gemma4:e2b")

# 도구등록
tools = [check_weather, check_stock, now_date]

# 시스템 명령
sys_prompt = """
당신은 도구를 사용할수 있는 AI 비서 입니다.
질문에 답하기 위해서 필요하다면 도구를 활용하세요.
[출력규칙]
1. 답변은 오직 한글로 해주세요.
2. 문장에 '실시간 데이터가 아니다.', 'API가 필요하다.', '가정된 결과다' 같은 불필요한 주의사항(Note) 
또는 추가설명은 붙이지 마세요.
3. 도구를 활용한 결과는 오직 결과만 깔끔하게 한국어 문장으로 정리해서 답하세요.
"""

# 에이전트 생성
agent = create_agent(llm,tools=tools, system_prompt=sys_prompt)

def start_agent(query:str): # 프롬프트 생성 + 대답 듣기
    # stream_mode="updates" <- 주요 과정이 종료될 때마다 출력
    # stream_mode="messages" <- 기본(타이핑 하듯이 출력)
    for chunk in agent.stream({"messages":[("user",query)]}, stream_mode="updates"):
        print(chunk)
        if 'model' in chunk:
            message = chunk['model']['messages'][-1].content
            # print(message,end="",flush=True)
            yield message