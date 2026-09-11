import logging
import os
import shutil
from typing import List
import uuid

from fastapi import FastAPI, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from image_service import class_img, fileUpload, vision



app = FastAPI()

# logger = logging.getLogger(__name__)
# FILE_PATH = './upload'
IMG_PATH = './upload'

app.mount("/view",StaticFiles(directory="view"))

app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"])

@app.get("/")
def main():
    return RedirectResponse("/view/upload.html")

@app.post("/upload")
# def upload(files:List[UploadFile]):
#     print(files)
#     msg = '파일 처리 오류'
#     save_path = ''
#     try:
#         for file in files:
#             post_name = file.filename
#             name,ext = os.path.splitext(post_name)
#             print('post name is - ',name)
#             new_name = f'{uuid.uuid4()}{ext}'
#             save_path = f'{FILE_PATH}/{new_name}'
#             with open(save_path, 'wb') as file_obj:
#                 shutil.copyfileobj(file.file,file_obj)
#             msg = '파일 업로드 성공'
#     except Exception as e:
#         logger.error(e)
#     return (vision(save_path)[0]['label'],save_path)
def upload(files:UploadFile):
    save_path = f'{IMG_PATH}/{files.filename}'
    msg = 'file upload failed'
    if fileUpload(files.file,save_path) == 1:
        msg = 'file upload success'
        result = class_img(save_path)

    return {"upload":msg,"image":files.filename,"result":result}