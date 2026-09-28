import chromadb

client = chromadb.PersistentClient('./my_db')
coll = client.get_or_create_collection('user_guide')

def add_data():
    coll.add(
        documents=[
            "로그인 하려면 우측 상단 버튼을 누르세요",
            "비밀번호를 잊으셨나요? 이메일 인증을 진행 하세요.",
            "환경설정에서 다크모드를 지원합니다."
        ],
        ids=["doc1","doc2","doc3"],
        metadatas=[
            {"category": "auth", "importance": 1},
            {"category": "auth", "importance": 2},
            {"category": "settings", "importance": 1}
        ]
    )

# add_data() # 데이터 추가 (1회 이후 주석처리)

# 1. 특정 ids 를 이용해 가져오는 방법
results = coll.get(ids=["doc1"])
print(f'ids 를 활용해 데이터 가져오기 : {results}')

# 2. 쿼리를 이용한 데이터 조회
results = coll.query(query_texts=["비밀번호 찾기"], n_results=1)
print(f"{results['documents']} / {results['distances']}")

# 3. 데이터 수정 upsert: add or update
coll.update(
    documents=["로그인 방법 : 우측 상단 '로그인' 버튼 클릭 후 아이디 입력"],
    metadatas=[{"category":"auth","importance":3}],
    ids=["doc1"])

# doc1 에 대해서 변경되었는지 확인
results = coll.get(ids=["doc1"])
print(f'ids 를 활용해 데이터 가져오기 : {results}')

# 4. 데이터 삭제
coll.delete(ids=["doc3"])
data_list = coll.get()
print(data_list)