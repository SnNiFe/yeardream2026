# 2단계 검색 구조(retriever -> re rank)
# 1. 검색결과를 폭넓게 가져와 추려낸다.
# 2. 그 안에서 (질문,답변) 연관관계를 추론해 다시 정렬한다.
from common import build_vector_retriever, rag_tech_documents, rank_of, rerank

# 데이터 호출
docs = rag_tech_documents()
RERANK = "BAAI/bge-reranker-v2-m3"
EMB_KO = "intfloat/multilingual-e5-small"
# 질문 준비
SCENARIOS = [
    # 1차 벡터는 doc02(BM25)에 끌려 정답 doc03(하이브리드)을 2위로 → 리랭커가 1위로
    {"query": "BM25와 벡터를 합쳐 약점을 보완하는 검색", "target": "doc03"},
    # 1차 벡터는 doc04(리랭킹, '1차로 추린')에 끌려 정답 doc07(압축)을 2위로 → 리랭커가 1위로
    {"query": "1차로 추린 문서에서 핵심 문장만 추출", "target": "doc07"},
]

# 1차 검색(일반적인 vector 검색 또는 BM25 검색)
vec = build_vector_retriever(docs,EMB_KO,k=6,name='re_rank_coll')
print("준비완료 / 1차벡터 k=6")
for sc in SCENARIOS:
    q = sc['query']
    tgt = sc['target']
    print(f"{q} -> {tgt}")
    step1 = vec.invoke(q)
    step1_rank = rank_of(tgt,step1)
    # list1 = [f'{d.metadata["id"]}/{d.metadata["topic"]}' for d in step1] # f-string err 방지
    # print(f"1차 검색 순위:{step1_rank} {list1}")
    print(f"1차 검색 순위:{step1_rank} {[f'{d.metadata["id"]}/{d.metadata["topic"]}' for d in step1]}")

    step2 = rerank(q,step1,6,RERANK)
    step2_rank = rank_of(tgt,step2)
    # list2 = [f'{d.metadata["id"]}/{d.metadata["topic"]}' for d in step2] # f-string err 방지
    # print(f"2차 Re-Rank:{step2_rank} {list2}")
    print(f"2차 Re-Rank:{step2_rank} {[f'{d.metadata["id"]}/{d.metadata["topic"]}' for d in step2]}")
