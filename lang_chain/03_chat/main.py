from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

import chat_bot

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])
app.mount("/view",StaticFiles(directory="view"))
app.include_router(chat_bot.router)

@app.get("/")
def main():
    return RedirectResponse("/view/chat.html")