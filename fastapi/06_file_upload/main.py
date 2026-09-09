# uv pip install -r requirements.txt
import logging
import os
import shutil
import traceback
from typing import List
import uuid

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 일반 print 로그의 단점
# 로그가 찍힌 시간, 위치 등을 알 수 없다.
# DEBUG > INFO > WARNING > ERROR > CRITICAL
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:     [%(name)s] %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

logger.info("logger test!!")

FILE_PATH = './upload'

# 특정 경로에 폴더 생성
if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)
    logger.info(f"{FILE_PATH} 생성!")

app.mount("/view",StaticFiles(directory="view"))
app.mount("/images",StaticFiles(directory=FILE_PATH))
app.add_middleware(CORSMiddleware,allow_origins=["*"], allow_methods=["*"])

@app.get("/")
def main():
    return RedirectResponse("/view/upload.html")

@app.post("/upload")
def upload(files:List[UploadFile]):

    msg = "파일 업로드에 실패 했습니다."

    try:
        for file in files:
            logger.info(f'file name : {file.filename}') # img.png -> 12345678.png
            ori_filename = file.filename
            # 1. 파일명과 확장자 분리
            # name,ext = ori_filename.split('.') # . 을 기준으로 나눈다.
            name,ext = os.path.splitext(ori_filename) # 확장자 기준으로 나눈다.
            logger.info(f'{name} / {ext}')
            # 2. 파일명 변경 + 3. 새로운파일명 + 확장자
            new_filename = f'{uuid.uuid4()}{ext}'
            logger.info(f'new file name = {new_filename}')
            # 4. 파일 저장
            save_path = f'{FILE_PATH}/{new_filename}'
            # open (파일을 읽는 함수)
            # w:write, r:read, b:binary, t:text, +:read&write
            # with 는? 자원을 사용한 후 로직이 종료되면 함께 닫아준다.
            with open(save_path,'wb') as file_obj:
                shutil.copyfileobj(file.file,file_obj)

            msg = "파일 업로드에 성공 했습니다."
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc()) # 상세 에러로그 보기

    return {"msg":msg}

@app.get("/files")
def files():
    # 특정 경로의 파일 리스트를 가져옴
    file_list = os.listdir(FILE_PATH)
    logger.info(file_list)
    return {"files":file_list}

@app.get("/delete")
def delete(filename:str):
    path = f'{FILE_PATH}/{filename}'
    if os.path.exists(path):
        os.remove(path)
    return RedirectResponse("/view/file_list.html")