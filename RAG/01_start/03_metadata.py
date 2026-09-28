import chromadb

client = chromadb.PersistentClient('./my_db')
coll = client.get_or_create_collection('study')

# 데이터 추가
"""
coll.add(
    documents=["파이썬 기초 문법 가이드","자바 고급 성능 최적화"],
    metadatas=[
        {"lang":"python","level":"beginner","version":3.19},
        {"lang":"java","level":"advance","version":25}
    ],
    ids=["doc1","doc2"]
)
"""

# 공부할 내용 추천해줘
# metadata 의 내용으로 필터링 하고, 그 안에서 n 개의 데이터를 추출
results = coll.query(
    query_texts=["자바 공부할 내용 추천해줘"],
    n_results=1,
    where={
        "$and":[
            {"lang":{"$eq":"java"}},
            {"level":{"$eq":"advance"}}
        ]
    }
)
print(results)