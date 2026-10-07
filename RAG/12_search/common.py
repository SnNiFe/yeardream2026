from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings

from sample_data import SAMPLE_DOCS, RAG_TECH_DOCS


def sample_documents():
    documents = []
    for doc in SAMPLE_DOCS:
        documents.append(Document(
            page_content=doc['text'],
            metadata={"id":doc['id'], "topic":doc['topic']}
        ))
    return documents


def rag_tech_documents():
    """
    RAG_TECH_DOCS 를 LangChain Document 리스트로 변환(검색 비교 실습용).
    문서가 짧아 1청크=1문서이므로 별도 청킹 없이 검색기에 바로 넣는다.
    """
    documents = []
    for doc in RAG_TECH_DOCS:
        documents.append(Document(
            page_content=doc["text"],
            metadata={"id": doc["id"], "topic": doc["topic"]}
        ))
    return documents


def get_embeddings() -> OllamaEmbeddings:
    # nomic-embed-text:latest
    return OllamaEmbeddings(model="nomic-embed-text:latest")


model_dict = {}
def get_hf_embeddings(model_name:str):
    model_dict[model_name] = HuggingFaceEmbeddings(model_name=model_name)
    return model_dict[model_name]


def get_llm(temperature:float=0.2) -> ChatOllama:
    return ChatOllama(model="gemma4:e2b", temperature=temperature)


def rank_of(target_id: str, docs):
    """
    검색결과 docs 안에 정답 target_id 가 몇번째로 있는가?
    이 순서가 곧 순위 이다.
    만약 없다면 X 로 표기
    """
    for i, d in enumerate(docs, 1): # docs 를 1번 부터
        if d.metadata.get("id") == target_id: # 정답과 맞는 결과물이
            return i # 몇번째 있는가?(이걸 순위로 지정)
    return "X" # 아예 정답이 검색 결과에 없다면 X


def topics(ds):
    list = []
    for d in ds:
        list.append(d.metadata.get('topic','?'))
    return list


# ── 인덱싱 ────────────────────────────────────────────────
def build_vector_retriever(chunks, model:str, name:str, k:int = 5):
    store = Chroma.from_documents(
        chunks,
        get_hf_embeddings(model),
        collection_name=name
    )
    return store.as_retriever(search_kwargs={"k": k})


def build_bm25(chunks, k: int = 5):
    retriever = BM25Retriever.from_documents(chunks)   # 공백 토큰화(한국어는 형태소 분석 권장)
    retriever.k = k
    return retriever


# ── 융합(RRF) ─────────────────────────────────────────────
# k : RRF 에서 순위간 점수격차가 커지는 것을 막는 상수값(기본 60)
def rrf_fuse(result_list, k: int = 60, top_n: int = 5):
    # 각 문서별 최종 RRF 점수를 저장할 딕셔너리 {문서 내용: RRF 점수}
    scores = {}
    # 문서 내용을 Key로, 실제 문서(Document 객체)를 Value로 저장하는 맵
    docmap = {}

    for docs in result_list:
        for i, doc in enumerate(docs):
            key = doc.page_content
            docmap[key] = doc
            # [핵심] RRF 점수 계산 공식: 1 / (k + rank)
            # 기존 점수에 현재 순위 기반 점수를 누적합(+=) -> A 에도 있고, B 에도 있으면 더 중요
            # A 에서 5점, B 에서 4점 -> 9점
            # A 에서 4점, B 에서 0점 -> 4점
            scores[key] = scores.get(key, 0) + 1 / (k + i + 1)

    # 내림차순 정렬하여 점수가 가장 '높은' 문서가 상위에 오게 함
    # ("doc01", 0.032) -> key=lambda x: x[1] -> key = 0.032
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # 상위 top_n개 문서의 Key를 이용해 원본 Document 객체 리스트로 복원하여 반환
    doc_list = []
    for key,_ in ranked[:top_n]:
        doc_list.append(docmap[key])

    return doc_list


# ── 쿼리 변환 ─────────────────────────────────────────────
def multi_query(llm, q: str, n: int = 3):
    """LLM 으로 질문을 서로 다른 표현의 검색 질의 n개로 늘린다(원 질문 포함)."""
    text = llm.invoke(
        f"다음 질문을 검색이 잘 되도록 서로 다른 표현의 검색 질의 {n}개로 바꿔줘. "
        f"각 줄에 하나씩, 번호·기호 없이.\n질문: {q}"
    ).content

    qs = []
    for ln in text.splitlines(): # 줄바꿈 기준(\n) 으로 분리
        if ln.strip():  # 빈 줄이 아니라면
            cleaned_line = ln.strip("-•* \t")  # 불릿 기호 및 공백 제거
            qs.append(cleaned_line)

    return [q] + qs[:n] # [q, qs[0], qs[1]]


def hyde(llm, q: str):
    """HyDE — 질문에 대한 '가상의 답변'을 만들어 그걸로 검색"""
    return llm.invoke(
        f"다음 질문에 대한 가상의 짧은 답변을 1~2문장으로 써줘(사실 여부 무관, 검색용).\n질문: {q}"
    ).content


# ── 재순위화(Cross-Encoder) ───────────────────────────────
# 모델별로 캐시(여러 리랭커를 한 노트북에서 비교할 수 있게).
# 기본 ms-marco 는 영어 위주(데모용). 한국어는 다국어 BAAI/bge-reranker-v2-m3 가 정석.
def rerank(query: str, docs, top_n: int = 3,
           model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
    from sentence_transformers import CrossEncoder
    """1차 후보를 Cross-Encoder 로 (질문,문서) 쌍 점수화해 재정렬."""
    # 1. 모델 로드
    # 질문(Query)과 문서(Document)를 한꺼번에 묶어서 한 번에 분석하는 AI 검색/연관도 측정 모델
    ce = CrossEncoder(model, max_length=512)

    contents = []
    for doc in docs:
        contents.append((query,doc.page_content)) # (질문, 문서) 형태로 문서 추가

    # 2. (질문, 문서) 쌍으로 점수 계산
    scores = ce.predict(contents)

    # 3. 점수가 높은 순으로 정렬 후 상위 top_n개 반환
    ranked_docs = []
    for _,d in sorted(zip(scores, docs), key=lambda x: x[0], reverse=True):
        ranked_docs.append(d)

    return ranked_docs[:top_n]