from pathlib import Path

import torch
import torchvision
from ultralytics import YOLO

print(f"pytorch 버전 : {torch.__version__}")
print(f"pytorch vision 버전 : {torchvision.__version__}")
print(f"GPU 사용 가능 여부 : {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"사용중인 GPU 장치 이름 : {torch.cuda.get_device_name(0)}")

curr_dir = Path(__file__).resolve().parent
run_dir = f"{curr_dir}/runs/MyProject"

model = YOLO('yolo26n.pt') # YOLO 모델 받아오기
model.predict(source="https://ultralytics.com/images/bus.jpg", # 대상 파일
              save=True,    # 결과 이미지 저장 여부
              conf=0.5,     # 정확도 0.5 이상만 표시
              project=run_dir,  # runs/detect/MyProject/result 폴더 안에 저장
              name="result",
              exist_ok=True)   # 덮어쓰기 여부
print("예측 완료 runs/MyProject/result/ 안에 결과가 저장 되었어요.")