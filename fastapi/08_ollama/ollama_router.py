# ollama model 확인방법
# 1. huggingface.co 에서 App 이 ollama 이거나 파일 뒤 GGUF 가 붙은 모델 사용
# 2. ollama.com/search
from typing import Any, Dict

from fastapi import APIRouter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

router = APIRouter(prefix="/ask",tags=["ask"])

# 모델 생성
model = ChatOllama(model="exaone3.5:2.4b")

# 프롬프트 틀 제작(system and user)
prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 쉽게 정보를 전달해주는 AI 분야 전문가 입니다. 알기쉽게 예시를 주면서 설명하세요"),
    ("user","{topic} 에 대해서 설명해 주세요.")
])

@router.post("/batch") # /ask/batch
def get_answer(info:Dict[str,Any]): # post 로 받을땐 단일 변수로 받을 수 없다.(dict 또는 class)
    # 파이프라인 조립 LCEL(Lang Chain Express Language)
    chain = prompt | model | StrOutputParser()

    # 추론 실행
    query = info['q']
    result = chain.invoke({"topic":query})
    return {"msg":result}