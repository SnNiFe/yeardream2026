# 1. python 설치
sudo yum install -y python3.14 python3.14-pip
python3.14 --version

# 현재 경로
pwd
# 현재 디렉토리의 리스트
ls -al
# 2. 디렉토리 생성
mkdir app
# 생성된 디렉토리로 들어가기
cd app

# 3. 가상환경 생성 및 실행
python3.14 -m venv venv
source venv/bin/activate

# pip 업그레이드 / uv 설치
pip install --upgrade pip
pip install uv

# requirements.txt 생성 및 수정
vim requirements.txt
# i 수정
fastapi
uvicorn
# ESC -> :wq
cat requiremnents.txt

# 가살환경 종료
deactivate