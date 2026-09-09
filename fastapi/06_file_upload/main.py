# uv pip install -r requirements.txt
import logging

from fastapi import FastAPI

app = FastAPI()

# 일반 print 로그의 단점
# 로그가 찍힌 시간, 위치 등을 알 수 없다.
# DEBUG > INFO > WARNING > ERROR > CRITICAL
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:     [%(name)s] %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

logger.info("logger test!!")