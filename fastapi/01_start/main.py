# uv pip install fastapi uvicorn
# uvicorn main:app --host=0.0.0.0 --reload # host=0.0.0.0 모두 접속 허용, reload 수정 내용 자동 적용
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return {"message":"안녕하세요 Naaak 입니다."}