from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

# 1. 모델등록(임베딩,LLM)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest")
Settings.llm = Ollama(model="gemma4:e2b", request_timeout=300)
# 2. 청킹 사이즈 지정
Settings.chunk_size=300
Settings.chunk_overlap=30

# 3. PDF 읽어오기
pages = SimpleDirectoryReader("data",required_exts=[".pdf"]).load_data()

# 4. 인덱싱하기(조각내기+벡터로 바꾸기)
index = VectorStoreIndex.from_documents(pages, show_progress=True)

# 5-1. 검색기로 변환하여 검색 내용 확인
"""
ret = index.as_retriever(similarity_top_k=3)
nodes = ret.retrieve("문서에서 말하는 핵심 내용이 뭐야?")

for i,node_with_score in enumerate(nodes):
    print(f"=== 검색결과 {i+1} (유사도점수 : {node_with_score.score:.4f})")
    print(f"내용 : {node_with_score.node.get_content()}")
    print(f"메타데이터 : {node_with_score.node.metadata}")
"""
# 5-2. LLM 을 활용
query_engine = index.as_query_engine(similarity_top_k=5)
resp = query_engine.query("이 소설의 주제는?")
print(resp)

# AI 가 어떤 부분을 보고 답했는지 확인
for i,node in enumerate(resp.source_nodes,1):
    page = node.metadata.get("page_label","?")
    preview = node.text[:80].replace("\n","")
    print(f"[{i}] {page}쪽 유사도 : {node.score:.4f}")
    print(f"{preview}...")
    print("-"*120)