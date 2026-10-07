# BM25(키워드) 와 벡터(의미) 를 동시에 돌려 결과를 합쳐 약점 상호 보완하는 방식
from common import build_vector_retriever, rag_tech_documents, topics

# 1. 데이터 불러오기
docs = rag_tech_documents()
print(f"{len(docs)} 개 문서 불러오기")
query = "두 검색 방식을 합쳐 약점을 보완하는 방법"
EMB_KO = "intfloat/multilingual-e5-small"

# vector 방식 불러오기
vec = build_vector_retriever(docs,EMB_KO,"vec")
results = vec.invoke(query)
print(f"1. 벡터의 결과값 : {topics(results)}")




SCENARIOS = [
    {
        "query": "키워드 검색의 한국어 처리",
        "target": "doc02",
        "expect": "BM25 우위 — 정답 doc02에 'BM25'가 직접 등장. Vector는 '한국어'에 끌려 다국어(doc05)로 샘"
     },
    {
        "query": "검색 결과를 좁은 후보에서 한 번 더 정렬하는 모델",
        "target": "doc04",
        "expect": "Vector 우위 — 정답 doc04의 단어가 질의와 거의 안 겹쳐 BM25는 놓침"
    },
]