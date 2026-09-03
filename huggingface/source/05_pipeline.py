"""
전처리      : 사람의 글자를 컴퓨터가 인식하기 좋게 쪼개고 숫자화 시키는 과정(tokenizing)
모델 추론   : 이 숫자들(ids)을 딥러닝 모델에 넣어서 계산
후처리      : 모델로부터 받아온 숫자를 사람이 알수있는 문자로 변환하는 과정
"""

from transformers import pipeline

# 1. task 와 model 명을 입력해서 원하는 모델 불러오기
# task 만 입력해도 관련된 모델을 자동으로 불러온다.
model = pipeline(task="text-classification")

# 2. 불러온 모델 이름 확인(선택)
model_name = model.model.name_or_path
print(f'사용되는 기본 모델 이름 : {model_name}')
# 2-2. 모델의 타입 정보 확인(선택)
print(f'모델 클래스 타입 : {type(model.model)}')

# 3. 모델 추론 후 결과 받기
result = model("오늘 hugging face 를 공부하는 둘째날 인데, 신기하다.")
# 4. 디코딩 필요 없이 출력
print(result)