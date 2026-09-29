import os

from fastapi import UploadFile

FILE_PATH = './upload'

if not os.path.exists(FILE_PATH):
    print(f'{FILE_PATH} 폴더 생성 완료')
    os.makdirs(FILE_PATH)

def file_upload(file:UploadFile) -> bool:
    success = False
    return success