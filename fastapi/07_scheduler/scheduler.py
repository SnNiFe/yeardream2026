from apscheduler.schedulers.asyncio import AsyncIOScheduler

from jobs import task1

def sch_start():
    # 1. 객체 생성
    sch = AsyncIOScheduler()

    # 2. 스케쥴러 객체에 할 일을 등록
    # 실행함수, 주기, 상세주기, 아이디, 매개변수
    # 2-1. 단발성 주기
    sch.add_job(task1,'date',
                run_date='2026-09-09 15:20:00',
                id='task1',
                args=['Fast API'])

    return sch # 반환