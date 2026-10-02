from PyPDF2 import PdfReader
import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


data_dir = 'data'

embed_fn = OllamaEmbeddings(base_url='http://localhost:11434', model='nomic-embed-text:latest')
client = chromadb.PersistentClient(path='store')
coll = Chroma(client=client,collection_name='rag_data',embedding_function=embed_fn)

def insert_data():
    file_names = ['FASTAPI.pdf', 'pandas.pdf', 'scikit_learn.pdf']

    for file in file_names:
        print(f"{file} 데이터 저장 시작!")
        reader = PdfReader(f'{data_dir}/{file}')
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

        coll.add_documents(docs)
        print(f"{len(coll.get()['ids'])} 개 문서 저장!")

# insert_data() # 일회성으로 저장한 후 주석처리 예정