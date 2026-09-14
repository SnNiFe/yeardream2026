from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from chat_bot import chat_answer, conversation_history, load_diaries, save_history

app = FastAPI()

app.mount("/view",StaticFiles(directory="view"))
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

@app.get("/")
def main():
    return RedirectResponse("/view/index.html")

@app.post("/ask/chat")
def ask_chat(info:Dict[str,str]):
    print(f'input : {info["q"]}')
    return StreamingResponse(chat_answer(info['q']),media_type="text/plain")

@app.post("/ask/chat/delete")
def delete_chat():
    conversation_history.clear()
    save_history(conversation_history)
    print("대화 기록이 초기화되었습니다.")
    return {"status": "success", "message": "대화 기록이 초기화되었습니다."}

@app.get("/load/diaries")
def get_diaries():
    diaries = load_diaries()
    sorted_diaries = sorted(diaries, key=lambda x: x.get('time', ''))
    return sorted_diaries

@app.get("/load/chat")
def get_chat():
    history_list = []
    for msg in conversation_history[-20:]:
        role = "user" if msg.type == "human" else "bot"
        history_list.append({"role": role, "content": msg.content})
    return history_list