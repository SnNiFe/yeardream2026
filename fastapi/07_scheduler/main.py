from fastapi import FastAPI

from scheduler import sch_start

app = FastAPI()
sch = sch_start()

@app.get("/")
@app.get("/start")
async def start():
    sch.start()
    return {'msg':'scheduler 실행'}