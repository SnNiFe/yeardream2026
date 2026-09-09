# uv pip install uvicorn fastapi
# uvicorn main:app --reload
import time
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# /view 라는 주소로 들어오면 이건 주소가 아니라 view 폴더로 이동해라
app.mount('/view',StaticFiles(directory='view'))

@app.get("/")
def main():
    # redirect : 특정 주소로 이동
    return RedirectResponse("/view/index.html")

@app.get("/calc")
def calc(val1:int,oper:str,val2:int):
    print(f'{val1} {oper} {val2} = ?')
    time.sleep(5)
    result = 0
    if(oper=='+'):
        result = val1 + val2
    if(oper=='-'):
        result = val1 - val2
    if(oper=='*'):
        result = val1 * val2
    if(oper=='/'):
        result = val1 / val2

    return {"result": result}