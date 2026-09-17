# ec2-user

# npm<-node.js, pip<-python, yum <- linux 에서 사용
# 1. yum upgrade
# sudo : super user do
# -y   : YES
sudo yum upgrade -y

# 2. 현재 시간 알아보기
date
timedatectl # 타임존 확인

# 3. 타임존을 Asia/Seoul 로 바꿔주기
sudo timedatectl set-timezone Asia/Seoul