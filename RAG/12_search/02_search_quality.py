# k 값에 따라서 다양한 답변을 낼 수 있으며, k=1 이라 하더라도 점수가 낮을 수 있다.
# 여기에는 언어특성에 따른 경우가 많다.

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from common import get_hf_embeddings, sample_documents


questions = [
    "RAG와 파인튜닝의 차이는?",
    "한국어 문서엔 어떤 임베딩을 써야 하나?",
    "환각을 줄이려면 프롬프트를 어떻게 써야 하나?",
    "벡터 데이터베이스에는 어떤 종류가 있나?",
]

EMB_KO = "intfloat/multilingual-e5-small" # ~470MB, 다국어(한국어양호)
EMB_EN = "sentence-transformers/all-MiniLM-L6-v2" # ~90MB, 영어위주(한국어약함)

# index 함수 - 특정 임베딩 모델을 이용해 데이터를 청킹/저장
def index(model_name):
    # 1. 데이터 불러오기
    docs = sample_documents()
    # 2. 청킹
    chunks = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50).split_documents(docs)
    # 3. 저장후 반환
    return Chroma.from_documents(chunks,get_hf_embeddings(model_name),collection_name=model_name.split("/")[-1])

# show 함수 - model 과 k 값을 주면 해당 토픽과 점수를 반환
def show(model_name,k):
    store = index(model_name)
    print(f"임베딩 모델 : {model_name.split('/')[-1]} / top_k={k}")
    for q in questions:
        hits = store.similarity_search_with_score(q,k)
        for data,score in hits:
            print(f"* 답변 : {data.metadata['topic']}({score:.2f})")
    
    store.delete_collection()

# 동일 모델 다른 k 값:
show(EMB_KO,k=1)
show(EMB_KO,3)