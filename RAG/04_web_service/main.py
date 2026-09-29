import logging
from typing import List

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/view", StaticFiles(directory="view"))
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     [%(name)s] %(message)s - %(asctime)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__) # main.py 즉 현재 모듈 네임

@app.get("/")
def main():
    logger.info("main page 접근 완료")
    return RedirectResponse("/view/index.html")

# file 과 문자열 파라메터가 섞여서 들어올 때 처리 방법
@app.post("/upload")
def upload(subject:str = Form(...), files:List[UploadFile] = File([])):
    logger.info(f"subject: {subject}")
    logger.info(f"files : {files}")
    return {'upload':''}