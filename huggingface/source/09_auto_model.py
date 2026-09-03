import os
import torch
from transformers import AutoTokenizer

os.environ["HF_HUB_DISABLE_SYMLINK_WARNING"] = "1"
model_id = "distilbert-base-uncased-finetuned-sst-2-english"

# 1. 토크나이저 생성
tokenizer = AutoTokenizer.from_pretrained(model_id, dtype=torch.float16)
# 2. 모델 생성
# 3. 전처리(토크나이징 -> tensor([]))
# 4. 모델 추론(추론에서는 경사 하강 알고리즘을 사용 안함)
# 5. 후처리(사람이 이해할수 있는 문자화)