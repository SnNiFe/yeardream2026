import logging

import langchain
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from tools import divide, minus, multiply, plus

# 추론 과정을 확인하기 위한 로그 설정
logging.basicConfig(level=logging.INFO)
langchain.debug = True

# 모델 불러오기
# ollama run gemma4:e4b
model_id = "gemma4:e2b"
model = ChatOllama(model=model_id, temperature=0)
tools = [plus,minus,multiply,divide] # 도구 등록
agent = create_agent(model=model,tools=tools) # 에이전트 생성

# 프롬프트 제작
# 3+3 은?
# a=5, b=10 일 경우 a+b를 계산해줘
msg = input('사칙 연산을 해 보세요. 예) 3 + 3\n')
prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 사칙연산 전문가 입니다. 값 a 와 값 b, 연산자가 주어지면 연산 후 답을 반환하는 작업을 수행하세요."),
    ("user","{message}")
])

chain = prompt|agent # 파이프라인 조합
resp = chain.invoke({"message",msg}) # 실행

print('---AI의 생각 과정 및 도구 실행 모니터링---')
for i,message in enumerate(resp['messages']):
    print(f'[STEP{i}]     {message}')

print(resp['messages'][-1].content)