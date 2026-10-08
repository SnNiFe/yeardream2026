from pathlib import Path

from ultralytics import YOLO
import matplotlib.pylab as plt
import matplotlib.patches as patch

curr_dir = Path(__file__).resolve().parent
run_dir = f"{curr_dir}/runs/MyProject"

model = YOLO('yolo26n.pt')
results = model.predict(
    source="bus.jpg",
    conf=0.5,
    project=run_dir,
    name="result",
    exist_ok=True
)
print(f"이미지 경로 : {results[0].path}")
print(f"걸린 시간 : {results[0].speed}")
print(f"이미지 크기 : {results[0].orig_img.shape}") # orig_img : 원본 이미지 배열
print(f"분류 사전 : {results[0].names}")

# 원본 이미지 보이기
fig,ax = plt.subplots(figsize=(10,8))
ax.imshow(results[0].orig_img)

boxes = results[0].boxes
# print(boxes)
# data : 각 꼭지점 좌표(x1, y1, x2, y2), 정확도, 분류아이디
# xywh : 중심점좌표(x,y)가로,세로크기
for box in boxes:
    # 그리기 위한 주요 정보 추출
    x1,y1,x2,y2,conf,cls_id = box.data.tolist()[0]
    x,y,w,h = box.xywh.tolist()[0]
    # 분류에 따른 색상 설정
    colors = {0:'purple',5:'green'}
    # 사진에 사각형 그리기
    rect = patch.Rectangle(
        (x1,y1),w,h,    # 상단 꼭지점좌표, 너비, 높이
        linewidth=3,    # 라인 두께
        edgecolor=colors[cls_id],   # 라인 색상
        facecolor='none'    # 채우기 색상
    )
    ax.add_patch(rect)

    # 정확도 넣기
    cls_name = results[0].names[cls_id]
    label_text = f"{cls_name} ({conf:.2f})"
    ax.text(
        x1,y1-10,label_text,
        color='white',
        fontsize=12,
        weight='bold',
        backgroundcolor=colors[cls_id]
    )


plt.axis('off') # 눈금자 숨기기
plt.show() # YOLO 는 기본 색상을 RGB 가 아닌 BGR 로 인식한다.