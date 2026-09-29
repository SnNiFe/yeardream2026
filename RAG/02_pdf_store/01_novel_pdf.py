# 1. 임베딩 함수 지정(chromadb 의 기본 임베딩을 사용하지 않을 경우)
from PyPDF2 import PdfReader
import chromadb
from chromadb.utils import embedding_functions
import tiktoken

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="hhtp://localhost:11434",
    model_name="nomic_embed-test:latest"
)

# 2. chromadb 선언시 임베딩 함수를 지정
client = chromadb.PersistentClient(path="./store")
coll = client.get_or_create_collection(
    name="novel",
    embedding_function=ollama_ef
)

# 3. 토크나이징(쪼개기 작업)
# 3-1. 토크나이저 등록
# cl100k_base 이라는 인코딩 규칙으로 토큰을 생성하는(쪼개는) 토크나이저 부름
tokenizer = tiktoken.get_encoding("cl100k_base")

def my_tokenizer(text:str) -> int:
    text = text.strip()
    if len(text) < 2: # 2글자 미만은 토크나이징 안함
        return 0
    # 사용될 토큰 크기 반환
    return len(tokenizer.encode(text))

# 4. 데이터 저장
def insert_data(path:str) -> None:
    # 4-1. 특정 PDF 를 불러와 읽는다.
    reader = PdfReader(path)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f'{i} PAGE')
        print(text)

insert_data('data/운수좋은날.pdf')