# OLLAMA 설치
curl -fsSL https://ollama.com/install.sh | sh

# 설치 확인
sudo systemctl status ollama

# 모델 설치
ollama run gemma4:e2b
# /bye 종료 후...

# 사용 IP 확인
sudo lsof -i :11434
# localhost:11434 (LISTEN)

# 다른 IP 에서 사용할 수 있도록 개방
sudo systemctl edit ollama.service

[Service]
Environment="OLLAMA_HOST=0.0.0.0"

# Ctrl+O -> Enter(저장) -> Ctrl+X(종료)

# Ollama 재시동
sudo systemctl daemon-reload
sudo systemctl restart ollama