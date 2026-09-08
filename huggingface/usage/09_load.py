# uv pip install -U bitsandbytes>=0.46.1
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# 양자화 설정
# 8bit - 비교적 안정적인 추론
# 4bit - 크기가 큰 데이터의 경우 overflow 발생, 설정과 환경 호환이 중요
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,  # 4비트 양자화 사용
    bnb_4bit_quant_type="nf4", # NF4(Normal Float4)
    bnb_4bit_compute_dtype=torch.float16, # 정밀도
    bnb_4bit_use_double_quant=True, # 이중 양자화 적용(메모리 추가절감)
)
# bnb_config = BitsAndBytesConfig(load_in_8bit=True)
model_id = 'mistralai/Mistral-7B-Instruct-v0.2'

# 양자화 설정을 이용해 토크나이저, 모델 로드
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="cpu", # auto
    quantization_config=bnb_config
)

# 테스트
answer = input('간단한 질문을 넣어 보세요\n')
tokens = tokenizer(answer,return_tensors="pt") # .to("cuda")
print(tokens)

result = model.generate(**tokens, max_new_tokens=50)
print(tokenizer.decode(result[0]))