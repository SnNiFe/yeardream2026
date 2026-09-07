# uv pip install evaluate scikit-learn
import evaluate

# 1. 평가지표 로딩
acc = evaluate.load('accuracy')

# 2. 예측값과 정답을 주고 결과 계산
result = acc.compute(
    predictions=[0,1,1,0], # 예측 값들
    references =[0,1,0,0] # 정답
)
print(result)