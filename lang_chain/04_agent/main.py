from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from agent_service import calc_bot

app = FastAPI()

app.mount("/view",StaticFiles(directory="view"))
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'])

@app.get("/")
def main():
    return RedirectResponse("/view/index.html")

@app.get("/calc")
def calc(val1:int, val2:int, oper:str):
    print(f'{val1} {oper} {val2} = ?')
    res = calc_bot(val1,val2,oper)
    print(f'{res}')
    return {"result": res}
