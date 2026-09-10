from typing import Dict

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

router = APIRouter(prefix="/ask", tags=["ask"])
model = ChatOllama(model="exaone3.5:2.4b")

prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 어려운 기술을 알기쉽게 설명해주는 전문가 입니다."),
    ("user","{topic} 에 대해서 설명해 주세요")
])

@router.post("/stream")
def get_answer(info:Dict[str,str]):
    # content 부분은 지속적으로 데이터를 줘야 한다.
    # return 은 여러번 할 수 없다.
    # StreamingResponse 안에서 지속적으로 실행하며 데이터를 줄 함수가 필요하다.
    return StreamingResponse(output_str(info['q']),media_type="text/plain")

def output_str(q):
    chain = prompt|model|StrOutputParser()
    for chunk in chain.stream({"topic":q}):
        # print(chunk,end='',flush=True)
        yield chunk # return 후 완전히 종료된게 아니면 대기한다.