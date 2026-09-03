import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

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

# print(f'모델에 입력될 최종 텍스트 포맷 : {prompt}')

# 문자열화된 토큰을 숫자(ids)로 변환
inputs = tokenizer(prompt, return_tensors="pt") # .to("cuda") # .to("mps")
print(f'{prompt} \n\n {inputs}')

# 모델 호출
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype=torch.float16, # 16(저사양), 32(쭝간), 64(고사양) 등..
    device_map="cpu", # auto, nvidia : cuda, mac : mps
)


# 답변을 생성
# pip install accelerate

with torch.no_grad():
    outputs = model.generate(
        **inputs, # ** <- dict
        max_new_tokens=256, # 생성할 최대 토큰수
        temperature=0.7,    # 창의성(0:있는 그대로 ~ 1:창의적)
        do_sample=True      # 창의성 관련
    )

print(outputs[0])
resp_text = tokenizer.decode(outputs[0],skip_special_tokens=True)
# 현재 resp_text 는 질문내용 + 답변의 형태이다.
# 답변만 출력하고 싶다면 outputs[0][입력내용제외한 나머지] 형태로 해야 한다.
print(resp_text)






# # 모델 답변 생성
# with torch.no_grad(): # 경사하강법 수치 기록 삭제?
#     pass