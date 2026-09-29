# 1. 임베딩 함수 지정(chromadb 의 기본 임베딩을 사용하지 않을 경우)
from PyPDF2 import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
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
    print(f"text:{text}")
    token_len = len(tokenizer.encode(text))
    print(f'token_size : {token_len}')
    return token_len

# 4. 데이터 저장
def insert_data(path:str) -> None:
    # 4-1. 특정 PDF 를 불러와 읽는다.
    reader = PdfReader(path)
    text = ''
    for i, page in enumerate(reader.pages): # PDF 페이지들을 한장씩 꺼내서
        text += page.extract_text() # 텍스트를 추출 후 text 변수에 누적시킨다.
        # print(f'{i} PAGE')
        # print(text)

    # 9페이지짜리 문자를 통으로 넣을 수 없기에 잘라줘야한다.(chunking 작업)
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=800, # 최대 청크 크기
        chunk_overlap=50, # 청크간 전후 문맥 파악을 위해 겹쳐지는 수
        length_function=my_tokenizer, # 토큰의 길이를 뭘로 정해?
    )
    # 데이터 끊어주기
    chunks = text_spliter.split_text(text)
    print(f'chinks = {chunks}')

insert_data('data/운수좋은날.pdf')