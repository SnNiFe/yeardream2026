# uv pip install chromadb
import chromadb

# 1. 클라이언트 생성(데이터 저장소 생성)
client = chromadb.PersistentClient(path="./my_db")

# 2. 컬렉션 생성 - collection 은 SQL 의 테이블과 비슷한 개념
# get_or_create_collection : 있으면 가져오고, 없으면 만들어라
coll = client.get_or_create_collection(name="my_collection")

# 3. 데이터 추가(입력시 벡터화)
# 벡터화 모델은 기본 모델(all-MiniLM-L6_v2)을 사용하며 다른모델을 사용해도 된다.
# 허깅페이스에서 자동으로 다운로드 받아옴
coll.add(
    documents=[
        "RAG는 외부 데이터를 참조하여 답변을 생성하는 기술 입니다.",
        "벡터 DB는 의미적 유사도를 바탕으로 데이터를 검색 합니다.",
        "파이썬은 데이터과학과 AI 분야에서 널리 쓰이는 언어 입니다."
    ], # 입력 데이터
    ids=["id1","id2","id3"]  # 데이터에 대한 id
)

# 데이터 검색
results = coll.query(
    query_texts=["RAG 는 무엇 인가요?"],
    n_results=2
)

print(f'검색결과 : {results}')

for doc in results['documents'][0]:
    print(f'doc : {doc}')