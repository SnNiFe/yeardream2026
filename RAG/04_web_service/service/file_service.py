import os
import shutil

from fastapi import UploadFile

FILE_PATH = './upload'

if not os.path.exists(FILE_PATH):
    print(f'{FILE_PATH} 폴더 생성 완료')
    os.makdirs(FILE_PATH)

def file_upload(file:UploadFile) -> bool:
    success = False

    path = f'{FILE_PATH}/{file.filename}'
    try:
        with open(path,'wb') as file_obj:
            shutil.copyfileobj(file.file,file_obj)
            success = True
    except Exception as e:
        print(e)
        os.remove(path)
    return success