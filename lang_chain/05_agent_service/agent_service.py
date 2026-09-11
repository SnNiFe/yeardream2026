import logging

import langchain # from langchain_core.tracers import langchain
from langchain_ollama import ChatOllama 


logging.basicConfig(level=logging.INFO)
langchain.debug=True

# ollama 모델 생성
llm = ChatOllama(model="gemma4:e2b")

def start_agent(query:str):
    # 프롬프트 생성 + 대답 듣기
    for chunk in llm.stream(query):
    # for chunk in llm.stream({"messages":[("system","주어진 질문에 성실히 대답해 주세요"),("user",query)]}):
        print(chunk.content,end="",flush=True)