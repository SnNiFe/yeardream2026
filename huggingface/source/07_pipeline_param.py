from transformers import pipeline
# device = [0:GPU, -1:CPU(default), "cuda":사용가능한GPU]
summ = pipeline(task="summarization", model="EbanLee/kobart-summary-v3", device=-1)

text = """자연어(NLP) 처리는 컴퓨터가 인간의 언어를 이해하고 생성할 수 있도록 하는 기술 입니다.
딥러닝의 발전과 함께 다양한 모델이 제안되었으며, 실제 서비스에도 널리 활용되고 있습니다."""

result = summ(text, max_length=60, min_length=20, do_sample=False)
print(result[0]['summary_text'])

"""
inputs (str 또는 List[str]) : 요약할 원본 텍스트. 
max_length (int) : 생성될 요약문의 최대 토큰 개수.
min_length (int) : 생성될 요약문의 최소 토큰 개수.
max_new_tokens (int) : 새로 생성할 토큰 개수의 최대값.(max_length와 동시에 쓰지 않는 것을 권장)
truncation (bool) : 입력 텍스트가 최대 길이 초과시 자동으로 잘라낼지 여부.
do_sample (bool) : True - 확률적 샘플링으로 다양한 결과 생성, False - 결정적(항상 같은 결과)으로 생성
temperature (float) : 샘플링 시 결과의 무작위성 조절. 값이 높을수록 다양하고 창의적인 문장
* do_sample=True일 때만 의미 있음

top_k (int) : 샘플링 시 확률 상위 k개의 단어 후보 중에서만 다음 단어를 선택.
* do_sample=True일 때만 의미 있음
top_p (float): 누적 확률이 p 이상이 되는 단어 후보 집합 내에서만 선택 (nucleus sampling).
* do_sample=True일 때만 의미 있음

early_stopping (bool): 기본 False
True    : 설정한 상위후보 만큼 모이면 더이상 계산하지 않고 중단
False   : 설정한 상위후보 만큼 모인다 해도 계속 계산(더 높은 점수를 만날 수 있으므로...)

repetition_penalty (float): 이미 생성된 단어가 반복해서 나오지 않도록 페널티를 부여. 
* 1.0보다 크면 반복 억제(repetition_penalty=1.2)

batch_size (int): 여러 문서를 한 번에 처리할 때 GPU/CPU에 올리는 배치 크기. 
* 클수록 빠르지만 메모리 사용량 증가

clean_up_tokenization_spaces (bool): 생성 텍스트의 토큰화 과정에서 생긴 불필요한 공백 정리 여부.
return_text (bool) : 요약 결과를 텍스트 형태로 반환할지 여부.
return_tensors (bool) : 요약 결과를 디코딩된 텍스트가 아니라 토큰 ID 텐서(tensor) 형태로 반환
"""