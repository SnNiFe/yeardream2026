from ultralytics import YOLO

model = YOLO('yolo26n.pt')

results = model.predict(
    source="data/sample.mp4", # "data/sample.mp4" # 0:서피스뒷캠, 1:서피스앞캠
    conf=0.5,
    show=True, # 별도의 창으로 화면 보여주기
    save=False, # 탐지내용 저장 여부
    imgsz=[480,640], # 사이즈 조정
    exist_ok=True,
    verbose=False, # 프레임관련로그 출력 여부
    stream=True, # 프레임 단위로 받아오기
    classes=[0] # 인식할 클래스 지정(사람 : 0)
)

for r in results:
    boxes = r.boxes
    print(f"탐지정보 : {boxes}")