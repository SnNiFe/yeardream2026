from apscheduler.schedulers.asyncio import AsyncIOScheduler

from jobs import task1, task2, task3

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

    # 2-2. 주기적 실행(초,분,시)
    # seconds, minutes, hours
    sch.add_job(task2, 'interval',
                seconds=10,
                id='task2',
                args=['News 사이트'])

    # 2-3. 주기적실행(cron)
    # second=0-59, */5(매 5초마다)
    # minute=0-59, */5(매 5분마다)
    # hour=0-23
    # day_of_week= SUN-SAT
    # day=1-31
    # month=1-12
    sch.add_job(task3, 'cron',
                minute='*/1',
                day_of_week='MON-FRI',
                id='task3',
                args=['수집한 데이터'])

    return sch # 반환