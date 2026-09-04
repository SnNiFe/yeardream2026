# uv pip install diffusers transformers accelerate torch


# pip uninstall -y diffusers transformers huggingface-hub # 삭제
# uv pip install --no-cache-dir -U huggingface-hub transformers diffusers # (재)설치
# pip install -U accelerate safetensors

##########

# from diffusers import StableDiffusionPipeline
# import torch

# model_id = "sd-legacy/stable-diffusion-v1-5"
# pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
# # pipe = pipe.to("cuda")

# prompt = "a photo of an astronaut riding a horse on mars"
# image = pipe(prompt, num_inference_steps=12).images[0]  
    
# image.save("astronaut_rides_horse.png")

###########

import torch
from diffusers import DPMSolverMultistepScheduler, StableDiffusionPipeline

model_id = "sd-legacy/stable-diffusion-v1-5"

pipe = StableDiffusionPipeline.from_pretrained(
    model_id, 
    torch_dtype=torch.float32,
    low_cpu_mem_usage=True
)

# 15스텝 이하에서도 이미지를 뽑아내는 고속 스케줄러로 교체
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# 메모리 절약 옵션 (필수: RAM 부족 방지)
pipe.enable_attention_slicing()

prompt = "a photo of an astronaut riding a horse on mars"

# 5스텝만 돌리기 (테스트용)
image = pipe(prompt, num_inference_steps=5).images[0]
image.save("astronaut_rides_horse.png")