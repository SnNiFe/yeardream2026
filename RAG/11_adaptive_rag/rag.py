import chromadb
from llama_index.core import Settings, SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

# 1. 모델등록, chunk size 등록
Settings.llm = Ollama(model="gemma4:e2b", request_timeout=300)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest")
Settings.chunk_size = 150
Settings.chunk_overlap = 15

# 2. chromadb 등록
client = chromadb.PersistentClient("store")
coll = client.get_or_create_collection("store")
# llama-index 와 연동
store = ChromaVectorStore(chroma_collection=coll)
# 3-1. llama-index 저장을 위한 객체
ctx = StorageContext.from_defaults(vector_store=store)
# 3. llama-index 검색을 위한 객체
index = VectorStoreIndex.from_vector_store(store)

# 4. 데이터 삽입
def insert_data():
    print('PDF 읽는중...')
    pages = SimpleDirectoryReader("data",required_exts=[".pdf"]).load_data()
    print('읽어온 데이터 인덱싱 작업(청킹+벡터화)')
    VectorStoreIndex.from_documents(pages, storage_context=ctx, show_progress=True)
    print(f"완료! 저장된 청크 수 : {coll.count()}")

# insert_data()
# print(coll.get())

# 5. 검색기 버전으로 결과값 불러오기
def rag_search(query:str):
    ret = index.as_retriever(similarity_top_k=5)
    nodes = ret.retrieve(query)
    resp = ''
    for node_with_score in nodes:
        resp += f"{node_with_score.node.get_content()}"
    return resp

# print(rag_search("next.js 와 react 를 비교해줘"))
