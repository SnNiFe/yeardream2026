import os

from transformers import pipeline

# window 경고메시지 지우기(선택사항)
os.environ["HF_HUB_DISABLE_SYMLINK_WARNING"] = "1"

# 텍스트 분류
"""
clf = pipeline(task="text-classification")
print(f'model_name : {clf.model.name_or_path}')
print(clf('Hugging Face is Amazing!!'))
"""

# 질의응답
# 모델명을 넣었더니 해당 task 가 pipeline 에 없다고 한다.
# transformers 의 버전을 낮춰주면 가능하다.
# pip install transformers==4.57.6
# pip show transformers
"""
qa = pipeline(model='monologg/koelectra-base-v3-finetuned-korquad')

result = qa(
    question="대한민국의 수도는 어디입니까?",
    context="대한민국의 수도는 서울 입니다."
)
print(result)
"""

# 이미지 분류
# uv pip install pillow torchvision
vision = pipeline(model="google/vit-base-patch16-224")
print(vision('dog.png'))