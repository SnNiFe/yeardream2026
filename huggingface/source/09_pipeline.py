import os

from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINK_WARNING"] = "1"

clf = pipeline(task="text-classification", device=-1)
result = clf("오늘 파이프라인과 오토모델을 배웠는데 재미있었다.")
print(result)