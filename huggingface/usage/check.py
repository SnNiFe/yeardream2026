import torch
# uv pip install torch –index-url https://download.pytorch.org/whl/cu126
print(torch.cuda.is_available())
# MAC
# print(torch.backends.mps.is_available())
print(torch.__version__)