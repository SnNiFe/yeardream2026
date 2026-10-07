from common import build_bm25, build_vector_retriever, get_llm, multi_query, rag_tech_documents, rerank, rrf_fuse, topics
from langchain_core.messages import SystemMessage, HumanMessage

# 데이터 호출 / 모델 준비
docs = rag_tech_documents()
RERANK = "BAAI/bge-reranker-v2-m3"
EMB_KO = "intfloat/multilingual-e5-small"
vec = build_vector_retriever(docs,EMB_KO,name="pipeline",k=10)
bm25 = build_bm25(docs,k=10)
llm = get_llm()

# 질문 준비
QUERY = "검색 품질을 종합적으로 끌어올리는 방법은?"
print(f"질문 : {QUERY}")
# 벡터 검색 테스트
print(f"벡터검색 : {topics(vec.invoke(QUERY)[:3])}")

# Multi-Query + Hybrid Search + Rerank = pipeline
def pipeline(query:str) -> dict:
    # 1. MultiQuery
    variants = multi_query(llm,query,3)
    list_result = [vec.invoke(v) for v in variants] + [bm25.invoke(query)]
    # print(list_result)
    # 2. Hybrid search - RRF
    candidates = rrf_fuse(list_result,top_n=6)
    # 3. Re Rank
    rank_result = rerank(query,candidates,top_n=3)
    # print(rank_result)
    context = ""
    for data in rank_result:
        context += f"({data.metadata['topic']}) {data.page_content}"
    # 4. LLM 활용
    answer = llm.invoke([
        SystemMessage(content="제공된 [문맥]에 근거해 한국어로 [질문]에 대한 답변을 간결하게 해줘."),
        HumanMessage(content=f"[문맥]\n{context}\n\n[질문]\n{query}")
    ]).content
    print(answer)

    return {"question":query,"context":context,"generation":answer}

print(pipeline(QUERY))