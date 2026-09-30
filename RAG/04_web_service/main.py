import logging
from typing import Dict, List

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from service.file_service import file_upload
from service.llm_service import get_answer
from service.rag_service import add_data, search_obj

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
    file_list = []
    for file in files:
        # 1. 파일 업로드
        success = file_upload(file)
        logger.info('file upload : {success}')
        # 2. 성공하면...
        if success:
            # 어떤 파일이 업로드 되었는지 리스트 만들기
            file_list.append(file.filename)
            # 업로드 된 파일의 내용을 chromadb 에 저장
            add_data(subject, file.filename)

    return {'upload':file_list}

@app.post('/ask/chat')
def ask_chat(info:Dict[str,str]):
    logger.info(f'info : {info}')
    q = info['q']
    subject = info['subject']
    # chromadb 검색기 불러오기
    ret = search_obj(subject)
    # 검색기와 질문을 랭체인으로 조립해서 결과 받아오기
    return StreamingResponse(get_answer(q,ret),media_type='text/plain')