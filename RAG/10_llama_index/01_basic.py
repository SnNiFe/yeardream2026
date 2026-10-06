# 1. 임베디드함수 선언 + 올라마 연동
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest")
Settings.llm = Ollama(model="gemma4:e2b")
# 1-1. chunk_size, overlap 지정(글자수가 아니라 토큰 수)
Settings.chunk_size = 300
Settings.chunk_overlap = 30

# 2. chromadb 생성 및 collection 연동

# 3. 데이터 삽입
# 3-1. pdf 읽어오기 + pdf 에서 각각의 페이지에서 텍스트 추출 + text_splitter 설정 + 쪼개주기
print('PDF 읽는 중...')
documents = SimpleDirectoryReader("data", required_exts=[".pdf"]).load_data()
print(f"읽어온 chunk : {len(documents)}")
# 3-2. 저장하기 위한 인덱싱(임베딩)
index = VectorStoreIndex.from_documents(documents,show_progress=True)
nodes = list(index.docstore.docs.values())
print(f"총 생성된 청크 수 : {len(nodes)}")
for i,node in enumerate(nodes):
    # print(f"{i}:{node}")
    # print(node.metadata)
    page = node.metadata.get('page_label','?')
    text = node.text[:50]
    id = node.node_id
    print(f"[NODE {i+1}] {id}")
    print(f"{page} page")
    print(f"{text}...")

# 3-5. 저장(생략)
# 4. 질문에 대한 내용 찾아오기(retrieve 모드로 변환)(생략)
# 5. 해당 내용 찾아서 LLM 에 전달(생략)
