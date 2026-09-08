import evaluate


# 1. 평가지표들 불러오기
print('평가지표 로드...')
metrics = evaluate.combine([
    evaluate.load("accuracy"),  # 정확도
    evaluate.load("f1"),        # 일치도
    evaluate.load("precision"), # 정밀도
    evaluate.load("recall")     # 재현율
])

# 2. 예측값과 정답 넣기
result = metrics.compute(
    predictions=[0,1,1,0],
    references=[0,1,0,0]
)

# 3. 결과 출력 - 각 모델에서 추출한 점수
# {'accuracy': 0.75, 'f1': 0.6666666666666666, 'precision': 0.5, 'recall': 1.0}
print(result)