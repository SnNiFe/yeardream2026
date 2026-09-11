from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from agent_service import start_agent
from chat_model import ChatModel


app = FastAPI()
app.mount("/view",StaticFiles(directory="view"))

@app.get("/")
def index():
    return RedirectResponse("/view/chat.html")

@app.post("/ask/chat")
def ask_chat(param:ChatModel):
    print(param.q)
    return StreamingResponse(start_agent(param.q),media_type="text/plain")