from pathlib import Path

from ultralytics import YOLO

# 1. 모델 불러오기
model = YOLO('data/best.pt')
# 2. 테스트할 파일 경로
test_image = 'fasion_mnist/test/Bag/18.jpg' # Shirt/4.jpg
# 3. 예측
curr_dir = Path(__file__).resolve().parent

results = model.predict(
    source=test_image,
    save=True,
    project=f"{curr_dir}/runs/predict",
    name="test_result",
    exist_ok=True
)
print('예측 성공')
print(results[0])