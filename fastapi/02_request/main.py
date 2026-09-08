# uv pip install fastapi uvicorn
# uvicorn main:app --reload
from fastapi import FastAPI, Request
# from starlette.requests import Request # 자동완성

app = FastAPI()

@app.get("/")
def main(req:Request):
    print(f'method : {req.method}')
    print(f'url:{req.url}')
    return {"info":f"{req.method} {req.url}"}

@app.get("/setInfo") # 이게 path
def setInfo(req:Request):
    print(f'host : {req.client.host}:{req.client.port}')
    print(f'path:{req.url.path}') # domain:port 뒤에 오는 주소
    # /setInfo?userName=김지훈&gender=male&hobby=영화&hobby=게임&hobby=축구
    name = req.query_params.get("userName")
    gender = req.query_params.get("gender")
    hobby = req.query_params.getlist("hobby")
    print(f'name:{name}')
    print(f'grnder:{gender}')
    print(f'hobby:{hobby}')
    return {"msg":"OK"}
