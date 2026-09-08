import evaluate
import numpy as np
from datasets import load_dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding, Trainer, TrainingArguments

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
    predict = np.argmax(logits, axis=-1)
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
    model = AutoModelForSequenceClassification.from_pretrained(model_id, num_labels=2)
    # 4. 학습 상세정보 지정(하이퍼 파라메터)
    args = TrainingArguments(
        output_dir='./results', # 결과와 체크포인트 저장 경로
        num_train_epochs=2,     # 전체 학습 수
        per_device_train_batch_size=16, # 학습당 묶음 수
        per_device_eval_batch_size=16,  # 평가당 묶음 수
        learning_rate=0.00002,          # 보폭(2e-5)
        eval_strategy="epoch",          # 평가 시점 - 학습당
        save_strategy="epoch",          # 저장 시점 - 학습당
        load_best_model_at_end=True,      # 평가가 끝난 시점에서 가장 우수한 모델을 로드
        metric_for_best_model="accuracy", # 최고의 모델을 판단하는 매트릭 기준
        logging_steps=100,                # 100번의 step마다 로그 출력
        report_to="none",                 # 외부 로깅툴 사용 여부
        dataloader_num_workers=4,         # 데이터 로딩시 사용할 스레드/프로세스 수
        ###GPU 메모리 최적화 옵션###
        # 1. Gradient Checkpoint
        gradient_checkpointing=True,
        # 2. Mixed precision 설정(GPU 사양에 맞춰서 설정)
        fp16=True, # T4, V100 등 이전세대 GPU
        # bf16=True, # A100, RTX3000/4000 시리즈 이상
        # 3. compile 을 이용한 최적화
        torch_compile=True,
        # 4. Gradient EXploding 방지를 위한 cliping
        max_grad_norm=1.0,
        # 5. Gradient Accumulation 으로 큰 배치 효과 구현(16번 모아서 한방에 처리)
        gradient_accumulation_steps=16
    )
    # 5. Trainer API 생성
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=token_ds['train'],
        eval_dataset=token_ds['test'],
        processing_class=tokenizer,
        data_collator= DataCollatorWithPadding(tokenizer=tokenizer), # 토크나이징 후 패딩설정
        compute_metrics=compute_matrics     # 평가지표함수 지정
    )

    # 6. 학습
    print('모델학습 진행 중...')
    trainer.train()

    # 7. 평가
    results = trainer.evaluate()
    print(f'평가 결과 : {results}')

    # 8. 저장
    save_path='./my_imdb_bert_model'
    trainer.save_model(save_path)
    tokenizer.save_pretrained(save_path)
    print('모델저장완료!!')

# 메인 프로세서(스레드) 만 진입해서 실행해라
if __name__ =='__main__':
    main()