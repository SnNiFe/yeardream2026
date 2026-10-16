import random
import opik

from opik import opik_context
from opik.evaluation.metrics import AnswerRelevance, Hallucination
from commons import JUDGE_MODEL, PROJECT_NAME, build_query_engine, use_llama_index

use_llama_index()
query_engine = build_query_engine(2)

@opik.track(name='haksa_chatbot', project_name=PROJECT_NAME, tags=['online','local-judge'])
def answer_with_scoring(question:str):
    # 1. 질문에 대한 답변과 근거를 받음
    res = query_engine.query(question)
    answer = str(res)
    context = [n.get_content() for n in res.source_nodes]

    # 2. 채점
    # 예) 30% 확률로 채점하고 싶다면? < 0.3
    if random.random() < 1.0:
        print('채점중...')
        h = Hallucination(model=JUDGE_MODEL).score(input=question, output=answer, context=context)
        r = AnswerRelevance(model=JUDGE_MODEL).score(input=question, output=answer, context=context)

        # 채점 내용을 opik trace 에 붙임
        opik_context.update_current_trace(
            feedback_scores=[
                {"name":"hall_online","value":h.value,"reason":h.reason},
                {"name":"rel_online","value":r.value,"reason":r.reason}
            ]
        )
        print(f"[채점완료] 환각 = {h.value:.2f} / 연관성 = {r.value:.2f}")

    return {"answer":answer, "context":context}

if __name__ == '__main__':
    questions = [
        "수강 신청은 어디서 하나요?",
        "평점 4.2면 몇 학점까지 신청이 되나요?",
        "기숙사 신청기간 알려줘", # 문서에 없는 내용
        "오늘 점심메뉴 추천해줘", # 학사와 무관한 내용
    ]

    for q in questions:
        print(f"Q : {q}")
        result = answer_with_scoring(q)
        print(f"A : {result['answer']}\n")

    opik.flush_tracker()
    print(f"완료! Traces 목록에서 hal_online / rel_online 점수를 확인 하세요.")