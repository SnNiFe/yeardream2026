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

# PDF 저장
def insert_data():
    file_name = 'RE177_2023년 국내외 인공지능 산업 동향 연구_2장.pdf'
    reader = PdfReader(f'{data_dir}/{file_name}')
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

# insert_data()