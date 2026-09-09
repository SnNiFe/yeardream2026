# uv pip install fastapi uvicorn
# uvicorn main:app --reload
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# /view 라는 요청이 오면 view 폴더로 이동 시켜라
app.mount("/view",StaticFiles(directory="view"))

# CORS : Cross Origin Resource Sharing
# MiddleWare : 특정 라우트로 가기전에 접근되는 곳(함수)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"], allow_methods=["*"])

@app.get("/")
def main():
    return RedirectResponse("/view/index.html")

@app.get("/send")
def send(msg):
    print(f'msg={msg}')
    time.sleep(5)
    return {"result":f"보낸메시지-{msg}"}