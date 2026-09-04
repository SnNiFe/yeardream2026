# uv pip install diffusers transformers accelerate torch


# pip uninstall -y diffusers transformers huggingface-hub # 삭제
# uv pip install --no-cache-dir -U huggingface-hub transformers diffusers # (재)설치
# pip install -U accelerate safetensors


from diffusers import StableDiffusionPipeline
import torch

model_id = "sd-legacy/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
# pipe = pipe.to("cuda")

prompt = "a photo of an astronaut riding a horse on mars"
image = pipe(prompt, num_inference_steps=12).images[0]  
    
image.save("astronaut_rides_horse.png")