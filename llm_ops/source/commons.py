import os

from dotenv import load_dotenv
import opik

load_dotenv('.env')

# 공통으로 사용할 변수
LLM_MODEL = 'gemma4:e4b'
EMBED_MODEL = 'bge-m3:latest'
OLLAMA_URL = 'http://localhost:11434'
PROJECT_NAME = os.getenv('OPIK_PROJECT_NAME')
print(f"project : {PROJECT_NAME}")

# OPIK 환경설정
print('opik 환경설정')
opik.configure(
    api_key=os.getenv('OPIK_API_KEY'),
    workspace=os.getenv('OPIK_WORKSPACE'),
    use_local=False # 우리는 cloud opik 을 사용하기 때문
)