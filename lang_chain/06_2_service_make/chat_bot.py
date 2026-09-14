import json
import os
from typing import Dict

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessage, HumanMessage, messages_from_dict, messages_to_dict
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

HISTORY_FILE = 'chat_history.json'
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return messages_from_dict(data)
        except Exception as e:
            print(f'기록 로드 실패, 새로 기록합니다: {e}')
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages_to_dict(history), f, ensure_ascii=False, indent=2)

conversation_history = load_history()
print(f'기록 {len(conversation_history)}개 로드 완료.')

model =ChatOllama(model="exaone3.5:2.4b")

prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 일정 정리 전문 AI 모델 입니다. 사용자의 입력을 받아 주요 키워드(시간,장소,행동)들을 정리해서 꾸밈없이 일정을 작성합니다. 부족한 부분은 사용자에게 다시 질문해주세요. 만약 사용자가 일정을 물어보면 기록 중에서 찾아서 답변해주세요."),
    MessagesPlaceholder(variable_name="history"), # 대화내용을 history 라는 이름으로 줄게
    ("user","{query}")
])

chain = prompt|model

def chat_answer(q:str):
    answer = ''
    for chunk in chain.stream({'query':q,'history':conversation_history}):
        answer += chunk.content
        yield chunk.content
    conversation_history.append(HumanMessage(content=q))
    conversation_history.append(AIMessage(content=answer))
    save_history(conversation_history)
    print(f'history length : {len(conversation_history)}')