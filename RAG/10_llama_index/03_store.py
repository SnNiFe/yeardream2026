# 1. AI 모델 등록(임베딩,LLM)
import chromadb
from llama_index.core import Settings, SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest")
Settings.llm = Ollama(model="gemma4:e2b", request_timeout=300)
# 2. chunk 사이즈 등록
Settings.chunk_size=300
Settings.chunk_overlap=30

# 3. chromadb 등록(langchain 보다 간결하게 하기위해 순수 chroma 사용)
client = chromadb.PersistentClient("store")
coll = client.get_or_create_collection("my_collection")
# ollama-index 와 연동
store = ChromaVectorStore(chroma_collection=coll)
ctx = StorageContext.from_defaults(vector_store=store)

# 4. PDF 읽기 -> 인덱싱 -> 저장
if coll.count() == 0:
    pages = SimpleDirectoryReader("data",required_exts=[".pdf"]).load_data()
    print(f"{len(pages)} 페이지 문서를 읽었음")
    # 문서, 어디에 저장?, 진행사항 보여줄지 여부
    VectorStoreIndex.from_documents(pages,storage_context=ctx,show_progress=True)
    print("저장 완료")

print(coll.count())