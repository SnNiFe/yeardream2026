# 카메라 또는 영상 에서 '사람' 이 탐지되면
# 콘솔로 '사람 탐지' 라고 출력해 보기
import cv2
from ultralytics import YOLO

model = YOLO('yolo26n.pt')
cap = cv2.VideoCapture(1) #('data/sample.mp4') #0뒤캠 1앞캠

if not cap.isOpened():
    print('비디오에 이상이 있습니다.')
    exit()

while True:
    success,frame = cap.read()
    if not success:
        print('프레임을 읽어올 수 없습니다.')
        break

    results = model.track( # track : 연속성이 있음(이전 프레임 기억)
        source=frame,
        persist=True, # 이전 프레임을 기억
        conf=0.5,
        imgsz=320, #[480,640], # 해상도 조정(속도 향상)
        classes=[0], # 0번:사람만 인식하도록 설정
        show=False, # 자체 팝업으로 보여주기
        verbose=False
    )

    for r in results:
        boxes = r.boxes
        if boxes.id != None:
            print("사람이 감지 되었습니다.")
            xywh_l = [f"{val:.2f}" for val in boxes.xywh.tolist()[0]]
            xyxy_l = [f"{val:.2f}" for val in boxes.xyxy.tolist()[0]]
            print(f"탐지정보 : \n xywh:{xywh_l}\n xyxy:{xyxy_l}\n")
        

    # YOLO 가 탐지한 내용을 가져와서 그리기
    yolo_frame = results[0].plot()
    resize_frame = cv2.resize(yolo_frame,(640,480)) #(480,640)) # 창 크기 줄이기
    cv2.imshow("YOLO 실시간 추적",resize_frame)

    # q 키 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()