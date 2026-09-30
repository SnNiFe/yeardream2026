from PyPDF2 import PdfReader
import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 임베딩 함수 설정
embed_fn = OllamaEmbeddings(base_url="http://localhost:11434",model="nomic-embed-text:latest")

# chromadb 설정 + 컬렉션설정
client = chromadb.PersistentClient(path="./store")
store = Chroma(
    client=client,
    collection_name='lecture',
    embedding_function=embed_fn
)

# 데이터 저장함수
def add_data(subject:str,filename:str):
    # 특정 경로에서 파일 객체를 읽어옴
    reader = PdfReader(f'upload/{filename}')
    # 페이지별로 하나씩 텍스트를 추출
    text = ''
    for page in reader.pages:
        text += page.extract_text()

    # 청킹 객체생성(기준등을 정의) # 객체화(대문자) 및 초기화(값입력)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=30,
        length_function=len
    )

    # 청킹된 내용을 RAG 에 저장
    docs = []
    for chunk in splitter.split_text(text):
        doc = Document(page_content=chunk, metadata={"subject":subject})
        docs.append(doc)

    store.add_documents(docs)
    print(f'저장된 데이터 수 : {len(store.get()['ids'])}')