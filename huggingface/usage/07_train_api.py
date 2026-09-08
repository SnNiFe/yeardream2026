import evaluate
import numpy as np
from datasets import load_dataset
from transformers import AutoTokenizer

# 1. 토크나이저 로드
model_id = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 2. 토크나이저 함수 정의
"""
def pre_proc(item):
    return tokenizer(item['text'], truncatioin=True, max_length=512)
"""

# 3. 평가 함수 정의
accuracy_metric = evaluate.load("accuracy")
def compute_matrics(eval_pred):
    logits,labels = eval_pred
    predict = np.argmax(logits, dim=-1)
    return accuracy_metric.compute(predictions=predict, references=labels)

def main():
    # 1. 데이터셋 불러오기
    print('데이터셋 로딩 중...')
    dataset = load_dataset(
        'stanfordnlp/imdb',
        split={"train":"train[:2000]","test":"test[:500]"}
    )
    # 2. 토크나이징 진행
    # item=> tokenizer(item['text'], truncatioin=True, max_length=512)
    print('토크나이징 진행중...')
    token_ds = dataset.map(
        lambda item: tokenizer(item['text'], truncatioin=True, max_length=512),
        batched=True,
        num_proc=4,
        remove_columns=["text"]
    )
    # print(token_ds)

    # 3. 모델 생성
    # 4. 학습 상세정보 지정(하이퍼 파라메터)
    # 5. Trainer API 생성
    # 6. 학습
    # 7. 평가
    # 8. 저장
    pass

# 메인 프로세서(스레드) 만 진입해서 실행해라
if __name__ =='__main__':
    main()