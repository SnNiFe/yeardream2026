import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = 'Qwen/Qwen2.5-1.5B-Instruct'

tokenizer = AutoTokenizer.from_pretrained(model_id)

text = "SDPA 와 EAGER 중에 누가 더 빠른가? 확인해 봅시다." * 10 # 30
inputs = tokenizer(text,return_tensors="pt") # .to("cuda")
print(f"입력 토큰 수 : {inputs['input_ids'].shape[1]}개")

def benchmark(attn_type, name):
    print(f'=== [{name}] 측정 시작 ===')
    # 모델 불러오기
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True, # cpu, mem 절약
        attn_implementation=attn_type
        # ,device_map="cpu" # auto, cuda, mps(mac)
        )
    
    # 실행
    start_time = time.time()
    with torch.no_grad():
        model(inputs['input_ids'])

    # CPU 가 GPU 작업 종료까지 기다리도록 동기화 시켜 준다.
    # torch.cuda.synchronize() # GPU 쓸 경우만 사용
    end_time = time.time() - start_time
    print(f'=== [{name}] 이 걸린시간 : {end_time} ===')

# 동시 실행 하지 말 것 (메모리 때문에 정확한 결과가 안나옴)
benchmark('sdpa', "Flash Attention 방식(SDPA)")
# 21.55264449119568 , 46.96498417854309 , 72.03531742095947 , 77.38971042633057 , 62.847657442092896
# 중간값 : 약 62.85초 / 평균 : 약 56.16초, 약 64.81초 (최저 21초 제외 시)

# benchmark('eager', "Standard Attention 방식(EAGER)")
# 41.13489651679993 , 65.01534223556519 , 120.14550185203552 , 64.48245620727539 , 66.60830974578857
# 중간값 : 약 65.02초 / 평균 : 약 71.48초, 약 59.31초 (최고 120초 제외 시)