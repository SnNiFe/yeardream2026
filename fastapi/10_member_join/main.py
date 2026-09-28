import logging
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from db import get_conn


app = FastAPI()
app.mount("/view", StaticFiles(directory="view"))

# logger 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:     [%(name)s] %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@app.get("/")
def main():
    return RedirectResponse("/view/index.html")

@app.get("/overlay")
def overlay(id:str):
    cnt = 1
    logger.info(id)

    #connection - DB를 사용할 수 있는 객체(금고)
    conn = get_conn()
    # query 문 준비
    sql = text('SELECT COUNT(id) AS cnt FROM member WHERE id = :id');
    # query 문 실행
    result = conn.execute(sql,{'id':id}).mappings().fetchone()
    # 결과 받기
    logger.info(f'result: {result}')
    # 해당 결과 보내기
    cnt = result['cnt']
    # 사용한 connection 닫아주기
    conn.close()

    return {"use":cnt}

@app.post("/join")
def join(info:Dict[str,Any]): # POST 방식은 파라메터를 Dict 또는 class 로 받아야 한다.
    logger.info(f'info={info}')
    # DB 접속
    conn = get_conn()

    # 쿼리문 준비
    sql = text("""INSERT INTO member(id,pw,name,age,gender,email)
                VALUES(:id,:pw,:name,:age,:gender,:email)""")

    try:
        result = conn.execute(sql,info) # 실행
        # 결과확인(쿼리 실행 결과를 담은 객체)
        logger.info(f"result={result.rowcount}")
        pass
    except Exception as e:
        logger.error(e)
    finally:
        conn.close() # DB 접속 종료

    
    return None