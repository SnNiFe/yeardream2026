from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = FastAPI()

# uvicorn main:app --reload
@app.get("/")
def main():
    return {"msg":"main page 접근"}

@app.get("/db/conn")
def db_conn():
    msg = 'DB 접속에 실패 했습니다.'
    conn = None

    try: 
        # 1. 접속정보(위치, 아이디, 비밀번호, 사용할database)
        url = 'mysql+pymysql://web_user:user@pass@54.180.107.203:3306/mydb'
        # 2. 엔진생성(매니저에게 금고를 달라고 요청)
        engine = create_engine(url)
        # 3. 세션(커넥션)생성(매니저가 금고를 가져옴)
        session = sessionmaker(bind=engine)
        conn = session()

        msg = 'DB 접속에 성공 했습니다.'
    except Exception as e:
        print(e)
    finally:
        # 4. 다 사용 후 반납(매니저에게 개인금고를 반납)
        conn.close()
    return {"msg":msg}