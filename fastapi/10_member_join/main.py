import logging
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from bcrypt_utils import encode_pass, get_token, matches, verify_token
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
    return RedirectResponse("/view/login.html")

@app.post("/login")
def login(info:Dict[str,str], req:Request):
    json = {'success':False, 'token':''}
    logger.info(f'info={info}')
    # 이 사람이 회원이라는 것을 어떻게 증명?
    # 1. 입력받은 id 를 통해 pw 가져옴
    conn = get_conn()
    sql = text("SELECT pw FROM member WHERE id = :id")

    try:
        # 2. 입력받은 pw 와 가져온 pw 를 비교
        result = conn.execute(sql,{"id":info['id']}).mappings().fetchone()
        # 아이디 비밀번호가 모두 일치 하면 True, 아니면 False
        success = matches(info['pw'],result['pw'])
        # 3. True 일 경우 로그인 성공으로 가정
        if success:
            token = get_token({"id":info["id"],"ip":req.client.host})
            json.update({'success':success,'token':token})
    except Exception as e:
        logger.error(e)
    finally:
        conn.close()


    return json

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
    row = 0

    # pw 를 암호화 하여 넣어줘야 한다.
    info['pw'] = encode_pass(info['pw'])

    # 쿼리문 준비
    sql = text("""INSERT INTO member(id,pw,name,age,gender,email)
                VALUES(:id,:pw,:name,:age,:gender,:email)""")

    try:
        result = conn.execute(sql,info) # 실행
        # 결과확인(쿼리 실행 결과를 담은 객체)
        logger.info(f"result={result.rowcount}")
        row = result.rowcount
        if row > 0:
            conn.commit()
        pass
    except Exception as e:
        logger.error(e)
        conn.rollback()
    finally:
        conn.close() # DB 접속 종료
    return {'row':row}

@app.get("/list/{page}")
def list_page(page:int, req:Request):
    logger.info(f'page={page}')
    login_id = req.query_params.get("id")
    client_ip = req.client.host
    token = req.headers.get("Authorization")

    logger.info(f"id={login_id}")
    logger.info(f"ip={client_ip}")
    logger.info(f"token={token}")
    msg = "로그인이 필요한 서비스 입니다."

    try:
        payload = verify_token(token)
        logger.info(f"payload : {payload}")
        if payload is not None:
            if payload.get("id") == login_id and payload.get("ip") == client_ip:
                msg = "로그인된 회원이 맞습니다. 계속 진행"
        else:
            msg = "토큰 정보가 일치하지 않습니다."

    except Exception as e:
        logger.error(e) # 비밀키가 변경되거나 토큰 만료시간이 지났을때
        msg = "토큰이 만료 되었습니다. 다시 로그인을 해 주세요."

    return {"msg":msg}