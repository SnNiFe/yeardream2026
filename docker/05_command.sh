# 컨테이너 생성시 쉘 명령어도 실행하도록 할 예정
# 쉘 명령어 -> cmd 에서 실행되는 명령어들
# 예) pip install -r requirements.txt
# 예) uvicorn main:app --host 0.0.0.0 --workers 4


# 1. D:\shared_study\RAG\04_web_service 를 c:\fastapi\app 으로 이동 (seivice,view,main,requiements)
# 2. model 과 ip 관련 내용 수정
# llm_service.py
model = ChatOllama(base_url="http://172.17.0.1:11434", model="gemma4:e4b", temperature=0.2)
# rag_service.py
embed_fn = OllamaEmbeddings(base_url="http://172.17.0.1:11434",model="bge-m3:latest")


# 컨테이너 실행
# -w : 특정 디렉토리에서 작업 할 거임
# sh -c : shell command
docker run -d --name fastapi -p 80:8000 -v $HOME/docker_share/fastapi/app:/app -w /app python:3.14-slim sh -c "pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0"

