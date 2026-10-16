import os

from dotenv import load_dotenv
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from opik.integrations.llama_index import LlamaIndexCallbackHandler
import opik
from llama_index.core.callbacks import CallbackManager

load_dotenv('.env')

# 공통으로 사용할 변수
LLM_MODEL = 'gemma4:e4b'
EMBED_MODEL = 'bge-m3:latest'
OLLAMA_URL = 'http://localhost:11434'
PROJECT_NAME = os.getenv('OPIK_PROJECT_NAME')
JUDGE_MODEL = f"ollama_chat/{LLM_MODEL}"
print(f"project : {PROJECT_NAME}")

# OPIK 환경설정
print('opik 환경설정')
opik.configure(
    api_key=os.getenv('OPIK_API_KEY'),
    workspace=os.getenv('OPIK_WORKSPACE'),
    use_local=False # 우리는 cloud opik 을 사용하기 때문
)

# llama-index 는 검색+대답 형태이기 때문에 다른 형태로 opik callbacks 를 등록한다.
def use_llama_index():
    # 1) opik callback 을 등록(llama-index 의 실행들이 자동으로 기록)
    Settings.callback_manager = CallbackManager([
        LlamaIndexCallbackHandler(
            project_name=PROJECT_NAME, 
            skip_index_construction_trace=True # 문서 인덱싱 과정 생략여부, 질문만 기록
        )
    ])

    # 2) 답변 모델 지정
    # ollama 를 지정하지 않으면 OpenAi 모델을 사용
    Settings.llm = Ollama(
        model=LLM_MODEL,
        base_url=OLLAMA_URL,
        request_timeout=600,    # 요청 지연시간(답변이 안와도 10분은 기다려준다.)
        context_window=8192,    # 문맥에 대한 저장 공간
        thinking=False,         # 추론 내용의 출력을 제한 답만 하도록(메모리와 속도 문제)
        keep_alive='30m'        # 메모리에 모델을 30분간 유지시켜둠
    )

    # 3) 임베딩모델 지정
    Settings.embed_model = OllamaEmbedding(model_name=EMBED_MODEL, base_url=OLLAMA_URL)

def build_query_engine(k:int):
    # text 문서 읽기
    documents = SimpleDirectoryReader('data').load_data()
    # 검색용 인덱스 만들기
    index = VectorStoreIndex.from_documents(documents)
    # 쿼리엔진으로 답변
    return index.as_query_engine(similarity_top_k=k)