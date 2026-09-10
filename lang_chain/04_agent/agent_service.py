import logging

import langchain
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from tools import divide, minus, multiply, plus

# 추론 과정을 확인하기 위한 로그 설정
logging.basicConfig(level=logging.INFO)
langchain.debug = True

# 모델 불러오기
# ollama run gemma4:e4b
model_id = "gemma4:e2b"
model = ChatOllama(model=model_id, temperature=0)
# 도구 등록
tools = [plus,minus,multiply,divide]
# 에이전트 생성
agent = create_agent(model=model_id,tools=tools)

# 프롬프트 제작
# 파이프라인 조합
# 실행