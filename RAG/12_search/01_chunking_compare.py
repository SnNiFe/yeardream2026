# 같은 문서라도 청킹 사이즈를 얼마로 설정하느냐에 따라 검색 결과가 달라진다.
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from common import get_embeddings, sample_documents

# 1. 데이터 불러오기
docs = sample_documents()
print(f"문서 {len(docs)}개 불러오기 완료")

# 2. 청크 사이즈별 비교
# 청크 크기가 큰 경우   : 한 청크에 여러 문맥 정보가 뒤섞여 있을 수 있다.
# 청크 크기카 작은 경우 : 청크에 담긴 문맥 정보가 부족해 문맥 파악이 어려울 수 있다.
test_size = [(120,0),(300,50),(800,100)] # chunk_size, chunk_overlap 
embedding = get_embeddings()
q = "임베딩 모델이 한국어 검색 품질에 주는 영향은?"
for size,overlap in test_size:
    print(f"size={size}, overlap={overlap}")
    # 텍스트 분리
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    chunks = text_splitter.split_documents(docs)
    # 청킹 된 내용 확인 : (120,0)의 경우는 너무 짧은가? 의심 가능
    # for chunk in chunks:
    #     print(f"chunk length : {len(chunk.page_content)}")

    # RAG 저장(로컬에 저장하지않음)
    store = Chroma.from_documents(chunks,embedding,collection_name=f"chunk_{size}")
    # 검색기모드로 전환
    ret = store.as_retriever(search_kwargs={"k":2})
    # 검색
    for result in ret.invoke(q):
        print(f"{result.metadata['topic']}\n{result.page_content[:50]}...")
    # 컬렉션 삭제
    store.delete_collection()
    print()