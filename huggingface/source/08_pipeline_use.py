import os

from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"

# pip install accelerate
pipeline(task="text-generation", model=model_id, device_map="cpu")

q = input("아무거나 질문 하세요!\n")

msg = [{"role":"user","content":q}]

result = pipe(msg, max_new_tokens=512, do_sample=True, temperature=0.7, top_p=0.9, repetition_penalty=1.2)
print(result[0]['generated_text'])