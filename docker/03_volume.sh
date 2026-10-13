# local 과 docker 사이의 공용 폴더를 설정
# C:/database 와 docker 의 /home/app/mesql 을 연결
# 장점 1. 컨테이너가 지워져도 로컬에 데이터가 남는다.(이후 컨테이너 설치시 데이터가 그대로 보존)
# 장점 2. 로컬과 컨테이너 사이에 파일교환이 수월하다.
# -v [로컬저장경로]:[컨테이너 내 저장경로]
docker run -d --name mariadb -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root@admin -v C:\db:/var/lib/mysql mariadb:11.8.3

# DB 에서 해야할 일
# 캐릭터셋 확인
SHOW VARIABLES LIKE 'character_set%';
SHOW VARIABLES LIKE 'collation%';

# 유저 생성
CREATE USER 'web_user'@'%' IDENTIFIED BY 'admin@pass';
SELECT * FROM mysql.user;
# 권한 부여
GRANT ALL PRIVILEGES ON *.* TO 'web_user';