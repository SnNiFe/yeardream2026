from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from chat_bot import chat_answer

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