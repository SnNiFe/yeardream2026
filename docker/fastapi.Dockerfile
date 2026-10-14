# docker pull python:3.14-slim
FROM python:3.14-slim
# docker run -d --name fastapi -p 80:8000 -v C:\fastapi\app:/app -w /app python:3.14-slim
# sh -c "pip install -r requirements.txt && uvicorn main:app --workers 4 -- host 0.0.0.0"
# -w /app
WORKDIR /app


# # sh -c "pip install -r requirements.txt && uvicorn main:app --workers 4 -- host 0.0.0.0"
CMD ["sh", "-c", "pip install -r requirements.txt && uvicorn main:app --workers 4 -- host 0.0.0.0"]

# build - dockerfile 을 이용해서 이미지 생성
# docker build -t <빌드될 이미지 이름> -f <실행될 dockerfile> <빌드위치>
# docker build -t fastapi-app -f fastapi.Dockerfile .

# run - 이미지를 이용해 컨테이너를 생성
# docker run -d --name fastapi -p 80:8000 -v C:\fastapi\app:/app fastapi-app

