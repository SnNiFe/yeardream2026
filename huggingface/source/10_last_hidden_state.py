import torch
from transformers import AutoTokenizer, AutoModel

model_id = "klue/bert-base" # task=fill-mask
# 1. 토크나이저 불러오기
tokenizer = AutoTokenizer.from_pretrained(model_id)
# 2. 모델 불러오기
model = AutoModel.from_pretrained(model_id)
# 3. 토큰화
text = "파이썬 이라는 언어는 참 재미있습니다."
inputs = tokenizer(text, return_tensors="pt")
# print(f'token화 된 tensor : {inputs}')
# 4. 모델 추론
with torch.no_grad():
    # output_hidden_states=True 로 하면 오든 레이어의 hidden state 를 받는다.
    outputs = model(**inputs, output_hidden_states=False)

# last_hidden_state
lhs = outputs.last_hidden_state
print(f'last_hidden_state shape : {lhs.shape}') # [1, 13, 768]
# 1 : 문장 1개
# 13 : special token 을 포함한 토큰의 수
# 768 : BERT 모델의 표현 차원

# 5. 활용예시 - 특정 단어의 벡터 가져오기
print(inputs['input_ids'][0])
tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
print(tokens)

# 토큰별로 768차원의 벡터를 가져와보기(앞 3차원만...)
for idx, token in enumerate(tokens):
    # lhs[0][idx][:3] == lhs[0,idx,:3] # 텐서나 넘파이에서..
    vect = lhs[0, idx, :3].tolist()
    print(f'{idx}:{token} -> vector:{vect}...')
    # 768 개의 배열에는 무엇이 들어있는가?
    # 단어를 구분할 수 있는 기준 조건(Feature)
    # 단일 단어 뿐 아니라 인근의 단어들과의 관계도 포함이 된다.

# last_hidden_state 는 문장안의 모든 각 단어의 의미를 ㄹ담은 벡터를 확인할 때


### pooler_output?