import opik


from commons import build_query_engine, use_llama_index


# 1. llama-index 와 opik callback manager 호출
use_llama_index()


#.2. RAG 를 읽어온 쿼리엔진 호출
query_engine = build_query_engine(2)


# 3. 질문 목록
questions = [
    "한 학기에 최대 몇 학점까지 들을 수 있나요?",
    "수강 정정기간은 언제까지 인가요?",
    "기숙사 신청은 어떻게 하나요?"
]


# 질문에 대한 답변
for q in questions:
    resp = query_engine.query(q)
    print(f"Q:{q}\nA:{resp}\n")


# 전송
opik.flush_tracker()
print("완료!!!!")