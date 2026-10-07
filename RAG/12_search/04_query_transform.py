# 질문이 짧거나 모호한 경우 문서를 제대로 못찾아 올 수 있다.
# 이에대한 대안으로 Multi-Query, HyDE 가 있다.
from common import *

# 1. 데이터 불러오기
docs = rag_tech_documents()
llm = get_llm()
EMB_KO = "intfloat/multilingual-e5-small"

# 질문, 정답
q = "한번 더 거르기"
target = "doc04"
vec = build_vector_retriever(docs,EMB_KO,k=10,name="qt_nb")
v_result = vec.invoke(q)
## print(v_result.metadata)
v_rank = rank_of(target,v_result)
# print(f"질문 : {q} / 정답 : {target} / 순위 : {v_rank}")

# Multi-Query
# LLM 을 사용해서 원본의 질문을 n개로 확장
# 확장된 질문으로 각각 검색후 RRF 로 검색결과를 합쳐서 순위 산정
variants = multi_query(llm,q,3)
## print(variants)
print('확장된 질문')
result_list = []
for v in variants:
    print(f"질문 : {v}")
    result_list.append(vec.invoke(v))

fused = rrf_fuse(result_list,top_n=5)
mq_rank = rank_of(target,fused)
print(f"VEC 순위:{v_rank} -> MQ 순위:{mq_rank} (topic : {topics(fused)})")

# HyDE(Hypothetical Document Embeddgings, 가상 답변 검색)
# 질문을 LLM 에 던져 답변을 받고 그 내용으로 RAG 검색을 수행한다.
answer = hyde(llm,q)
print(f"가상답변 : {answer}")
# answer 를 기반으로 vector 검색 수행
hyde_rank=rank_of(target,vec.invoke(answer))
print(f"VEC 순위:{v_rank} | MQ 순위:{mq_rank} | HyDE 순위:{hyde_rank}") 