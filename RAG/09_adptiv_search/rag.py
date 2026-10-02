import os

from PyPDF2 import PdfReader
import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

data_dir = 'data'
# Chromadb 연결
embedding = OllamaEmbeddings(model="nomic-embed-text:latest")

client = chromadb.PersistentClient('./store')
store = Chroma(
    client=client,
    collection_name='rag_data',
    embedding_function=embedding # 저장할때와 꺼내쓸때 임베딩함수가 다르면 안된다.
)

# 데이터 입력
def insert_data():
    for file in os.listdir(data_dir):
        reader = PdfReader(f"{data_dir}/{file}")
        text = ''
        for page in reader.pages:
            text += page.extract_text()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=150,
            chunk_overlap=30,
            length_function=len
        )
        docs = []
        for chunk in text_splitter.split_text(text):
            docs.append(Document(page_content=chunk))
        store.add_documents(docs)
        print(f"{file} 저장 완료 ({len(docs)})개")

## insert_data() # 아직 실행 안함 (1회 실행 후 주석 처리 예정)

def rag_search(query:str):
    # similarity : 유사도순
    # mmr : 유사도와 다양성
    docs = store.search(query,search_type="similarity", k=5)
    text = ''
    for doc in docs:
        text += doc.page_content
    return text

# print(rag_search('fast api 의 정의'))