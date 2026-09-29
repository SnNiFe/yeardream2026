import chromadb

client = chromadb.PersistentClient("./my_db")
coll = client.get_or_create_collection(name="study")
# 이렇게 한번에 한 데이터만 삽입도 가능
"""
coll.upsert(
    documents=["파이썬 완벽 가이드"],
    metadatas=[{"lang":"python","year":2024,"official":True}],
    ids=["id1"]
)

coll.upsert(
    documents=["자바 성능 최적화"],
    metadatas=[{"lang":"java","year":2022,"official":False}],
    ids=["id2"]
)

coll.upsert(
    documents=["리액트 기초 실습"],
    metadatas=[{"lang":"javascript","year":2023,"official":True}],
    ids=["id3"]
)
"""
print(coll.get())

# 단일 조건 - 공부할 자료를 찾을 건데 2023년 이후 데이터였으면 좋겠어
res = coll.query(
    query_texts=['공부할 자료'],
    n_results=2,
    where={"year":{"$gte":2023}}
)
print(f"doc : {res['documents']}")
print(f"distance:{res['distances']}")

# AND
print('AND 조건'+'='*36)
res = coll.query(
    query_texts=['참고문서'],
    n_results=2,
    where={"$and":[
        {"official":{"$eq":True}},
        {"lang":{"$eq":"python"}}
    ]}
)
print(f"doc : {res['documents']}")
print(f"distance:{res['distances']}")

# OR
print('OR 조건'+'='*36)
res = coll.query(
    query_texts=['참고문서'],
    n_results=2,
    where={"$or":[
        {"official":{"$eq":False}},
        {"level":{"$eq":"beginner"}}
    ]}
)
print(f"doc : {res['documents']}")
print(f"distance:{res['distances']}")