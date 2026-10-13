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