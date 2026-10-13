# ollama 를 도커에 설치(이유는? 설치와 삭제가 쉽기 때문)
# 1. 기존 ollama model 을 삭제
# ollama rm [모델명]
ollama list # 모델이 남지 않음을 확인

# ollama image 탐색 및 다운로드
docker search ollama
docker pull ollama/ollama

# GPU 지원 여부
nvidia-smi

# 컨테이너 실행
# -d : 백그라운드 실행
# --gpus=all : 가용되는 GPU 모두 사용(GPU 사용 가능 환경에서만)
# -v : 로컬경로:컨테이너내 경로
# -p : 호출포트:컨테이너에서사용포트
# --name : 컨테이너 이름
# docker run [옵션] [사용 이미지]
# docker run -d --gpus=all -v C:\ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker run -d -v C:\ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
# 실행중인 컨테이너 리스트
docker ps

# docker 내부 터미널로 들어간다
# docker exec -it [container] /bin/bash
docker exec -it ollama /bin/bash

# ollama run gemma4:e4b
# ollama run bge-m3 <- embed 모드 이기 때문에 에러가 나타남(대화가 안되므로)

# 1. fast-api 를 컨테이너에 올리기
# 대상 : $HOME/VSCODE/not_shared_study/lang_chain (D:\shared_study\lang_chain\01_start)
# 1. 대상폴더에서 .env, .idea, __pycache__ 를 제외한 모든 파일을 복사
# 2. 로컬과 컨테이너를 연결할 볼륨폴더를 생성($HOME/docker_share/fastapi/app) (c:\fastapi\app)
# 3. 복사한 파일을 이동시킨다.

# 컨테이너 실행
# 우리는 python:3.14-slim 이미지를 받은적이 없다.
# 없는 이미지를 이용해 컨테이너를 생성하려고하면 자동으로 이미지를 다운로드 받는다.
# -it 터미널로 연결하는 옵션
docker run -d -it --name fastapi -p 80:8000 -v $HOME/docker_share/fastapi/app:/app python:3.14-slim

# 실패한 컨테이너는 실패상태로 남아있게 된다. 그래서 다시 만들때 삭제해야 한다.
docker container rm -f fastapi

# -it 옵션을 넣으면 터미널 연결을 대기중이기에 fastapi 설치 등의 문구가 없어 실패하는 경우가 생기지 않는다.
# 터미널에 진입
docker exec -it fastapi /bin/bash

# app 폴더로 이동
cd /app
# 파일 리스트 점검
ls
# 라이브러리 설치
pip install -r requirements.txt

# 실행
uvicorn main:app --host 0.0.0.0 --workers 1

# 컨테이너 사이에는 도커 내부에서 사용하는 사설IP가 존재한다.
# 이 IP를 통해서 컨테이너간 통신을 해야한다.(172.17.0.1 ~ ...)
# model 을 불러오는 호출부에 ip 내용을 추가
# model = ChatOllama(base_url="172.17.0.1:11434", model="gemma4:e4b")