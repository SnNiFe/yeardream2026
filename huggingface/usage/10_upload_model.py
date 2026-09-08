from transformers import AutoModelForSequenceClassification, AutoTokenizer

# distilbert-base-uncased (대체용 모델)
# 1. 로컬에서 학습을 마친 모델과 토크나이저 로드
model_id = 'distilbert-base-uncased' # 샐성이 안되어 다른 모델로 대체
tokenizer =AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)

# 2. hugging face 에 PUSH
# 토큰의 권한이 write 여야 한다.
repo_id = 'KORNJ/test_upload_model_yeardream'
print('model 과 tokenizer 업로드 중...')
tokenizer.push_to_hub(repo_id)
model.push_to_hub(repo_id)
print('Upload complete!!!!')