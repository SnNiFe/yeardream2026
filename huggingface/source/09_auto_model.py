import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

os.environ["HF_HUB_DISABLE_SYMLINK_WARNING"] = "1"
model_id = "distilbert-base-uncased-finetuned-sst-2-english"

# 1. 토크나이저 생성
tokenizer = AutoTokenizer.from_pretrained(model_id)
# 2. 모델 생성
model = AutoModelForSequenceClassification.from_pretrained(model_id, torch_dtype=torch.float16)
# 3. 전처리(토크나이징 -> tensor([]))
inputs = tokenizer("Today is a greate day!!", return_tensors="pt")
print(f'inputs:{inputs}')
# 4. 모델 추론(추론에서는 경사 하강 알고리즘을 사용 안함)
with torch.no_grad():
    outputs = model(**inputs)

print(f'outputs:{outputs}')
# logits = 반환된 순수 숫자(이게 확률이 얼마나 높은건지 알 수 없다.)

# 5. 후처리(사람이 이해할수 있는 문자화)
prob = torch.softmax(outputs.logits, dim=-1).tolist()
print(f'probaaility : {prob[0]}')
print(f'POSITIVE : {round(prob[0][1]*100,2)}%')
print(f'NEGATIVE : {prob[0][0]*100:.2f}%')