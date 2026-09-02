import torch
from transformers import AutoTokenizer

model_id = "google/gemma-2-2b-it"
# 토크나이저 생성
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 대화 내용을 정의
msg_list = [
    {"role":"user","content":"파이썬에서 변수가 뭐야?"},
    {"role":"assistant","content":"변수는 데이터를 저장하는 상자와 같습니다."},
    {"role":"user","content":"그럼 리스트는 뭐야?"},
]

prompt = tokenizer.apply_chat_template(
    msg_list,
    tokenize = False, # False : 토큰화 된 내용을 문자열로 반환
    add_generation_prompt = True, # True : msg_list  이후 addidtant 가 이어 쓸수 있을지 여부
)

print(f'모델에 입력될 최종 텍스트 포맷 : {prompt}')

# # 모델 생성
# model = AutoModelForCausalLM.from_pretrained(
#     model_id,
#     dtype=torch.float32,
#     device_map="cpu", # nvidia : cuda, mac : mps
# )

# # 모델 답변 생성
# with torch.no_grad(): # 경사하강법 수치 기록 삭제?
#     pass