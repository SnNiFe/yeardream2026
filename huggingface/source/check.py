# uv pip install torch
import torch
print(f'window:{torch.cuda.is_available()}')
print(torch.__version__)

# mac 버전
print(f'mac:{torch.backends.mps.is_available()}')

# CPU 버전이 설치되어 있다면 GPU 사용이 불가능 하다.
# 기존 torch 제거 하고 다시 설치
# pip uninstall torch
# pip cache purge
# CUDA 지원 버전
# uv pip install torch --index-url https://download.pytorch.org/whl/cu126
