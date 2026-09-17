# mariadb 설치
sudo yum install -y mariadb1011-server mariadb1011

# mariadb 실행
sudo systemctl start mariadb
# 서비스 등록(서버 켜지면 무조건 같이 켜지도록)
sudo systemctl enable mariadb

# 상태 확인
sudo systemctl status mariadb
