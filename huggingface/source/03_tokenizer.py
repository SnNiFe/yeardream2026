# tokenizer 를 불러와야 하는데 어떤 클래스르 쓸지 잘 모르겠다.
from transformers import AutoTokenizer

# 토크나이저 호출
model_id = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 2일 예인선 전복 사고가 발생한 부산 앞바다에서는 높은 파도 등으로 해경이 구조작업에 어려움을 겪고 있다.
# 입력 받기
user_input = input('문장 입력:\n')
print(f'1. 입력받은 문장 : {user_input}')

token = tokenizer.tokenize(user_input)
print(f'2. 토큰들 : {token}')

input_ids = tokenizer.convert_tokens_to_ids(token)
# 받은 토큰을 그대로 숫자화 한다.
print(f'3-1. AI 가 인식할 수 있는 숫자로 변환 : {input_ids}')
# 문자를 받아 자체적으로 토큰화 하고 특수토큰도 넣어서 반환([CLS][SEP])
input_ids = tokenizer.encode(user_input)
print(f'3-2. AI 가 인식할 수 있는 숫자로 변환 : {input_ids}')