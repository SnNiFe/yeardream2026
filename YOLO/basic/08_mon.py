# 카메라 또는 영상 에서 '사람' 이 탐지되면
# 콘솔로 '사람 탐지' 라고 출력해 보기
import datetime
import os

import cv2
from ultralytics import YOLO

# 1. 카메라 연결
cap = cv2.VideoCapture(1)
# 2. 모델 준비
model = YOLO('yolo26n.pt')

if not cap.isOpened():
    print("비디오에 문제가 있습니다.")
    exit()

dir = "C:/Users/kimna/Desktop/yeardream/shared_study/YOLO/basic/captured"
if not os.path.exists(dir):
    print(f"{dir} 폴더가 없어서 생성")
    os.makedirs(dir)

while True:
    success,frame = cap.read() # 카메라에서 프레임을 읽어오기(성공여부,이미지프레임)

    if not success: # 못 읽어올 경우 나간다.
        break

    # 3. 탐지
    results = model.predict(
        frame,
        conf=0.5,   # 0.5 이상의 정확도만 탐지하여 표시
        show=False, # 별도의 창으로 보여줄지 여부(우리는 openCV로 보여줄 예정이라 False)
        verbose=False,  # 프레임 상세 로그
        classes=[0]     # 참지할 클래스(0: 사람) results[0].names
    )
    # 4. 탐지시 출력
    if len(results[0].boxes.xyxy.tolist()) > 0:
        # print("사람 탐지")
        # 캡쳐
        now = datetime.datetime.now()
        ftime = now.strftime("%Y_%m_%d_%H%M%S")
        file_name = f"{dir}/{ftime}.jpg"
        cv2.imwrite(file_name,frame)
        print(f"{ftime}.jpg 가 저장됨")

    # openCV 에 프레임 그리기
    plot_frame = results[0].plot()
    resize_frame = cv2.resize(plot_frame,(640,480))
    cv2.imshow("monitoring...",resize_frame)
    
    if cv2.waitKey(1000) & 0xFF == ord("q"): # n/1000초 마다 q가 눌렸는지 확인
        break
    

cap.release()
cv2.destroyAllWindows()