from fastapi import FastAPI

from scheduler import sch_start

app = FastAPI()
sch = sch_start()

@app.get("/")
@app.get("/start")
async def start():
    if not sch.running:
        sch.start()
    else:
        sch.resume()
    return {'msg':'scheduler 실행'}

@app.get("/stop")
async def stop():
    sch.pause() # 일시정지
    # sch.shutdown() # 완전히 닫는다.
    return {'msg':'scheduler 정지'}

@app.get("/pause/{task_id}")
async def pause_job(task_id:str):
    sch.pause_job(task_id)
    return {'msg':f'{task_id} 일시정지'}

@app.get("/resume/{task_id}")
async def resume_job(task_id:str):
    sch.resume_job(task_id)
    return {'msg':f'{task_id} 다시실행'}