from typing import Dict

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

router = APIRouter(prefix="/ask", tags=["ask"])
# 모델 호출
model =ChatOllama(model="exaone3.5:2.4b")

conversation_history = [] # 대화저장 리스트

# 프롬프트 작성
prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 답변 전문 AI 모델 입니다. 주어진 질문에 대해서 핵심만 간단히 대답하세요"),
    MessagesPlaceholder(variable_name="history"), # 대화내용을 history 라는 이름으로 줄게
    ("user","{query}")
])

@router.post("/chat")
def get_answer(info:Dict[str,str]):
    return StreamingResponse(output_str(info['q']),media_type="text/plain")

def output_str(q):
    chain = prompt|model # 파이프라인 조립
    answer = ''
    for chunk in chain.stream({'query':q,'history':conversation_history}):
        answer += chunk.content
        yield chunk.content
    conversation_history.append(HumanMessage(content=q))
    conversation_history.append(AIMessage(content=answer))

# # 실행 및 출력
# while True:
#     query = input('\n당신> ')
#     if query == '/exit' or query == '/bye':
#         print('대화를 종료 합니다.')
#         break
#     answer = ''
#     for chunk in chain.stream({'query':query,'history':conversation_history}):
#         print(chunk.content,end='',flush=True) # StrOutputParse() 를 안써서 .content 붙이는 것
#         answer += chunk.content

#     conversation_history.append(HumanMessage(content=query))
#     conversation_history.append(AIMessage(content=answer))
#     print()
#     print(f'history length : {len(conversation_history)}')
"""
chain = prompt|model # 파이프라인 조립
def chat_answer(query:str):
    answer = ''
    for chunk in chain.stream({'query':query,'history':conversation_history}):
        answer += chunk.content
        yield chunk.content
    conversation_history.append(HumanMessage(content=query))
    conversation_history.append(AIMessage(content=answer))
    print(f'history length : {len(conversation_history)}')
"""