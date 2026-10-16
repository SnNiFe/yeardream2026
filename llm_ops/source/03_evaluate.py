from opik import Opik, evaluate
from opik.evaluation.metrics import Hallucination, AnswerRelevance
from opik.evaluation.models import LiteLLMChatModel

from commons import JUDGE_MODEL, LLM_MODEL, OLLAMA_URL, build_query_engine, use_llama_index

client = Opik()
dataset = client.get_or_create_dataset(name="haksa-qa")
dataset.insert([
    {"input": "수강 신청은 어디서 하나요?", "expected_output": "학사서비스 > 수강신청 메뉴"},
    {"input": "수강 정정 기간은 언제인가요?", "expected_output": "개강 후 첫째 주 월~금"},
    {"input": "최대 신청 학점은?", "expected_output": "18학점, 평점 4.0 이상이면 21학점"},
    {"input": "기숙사 신청은 어떻게 하나요?", "expected_output": "문서에 없는 내용"},
])

# task - 특정 내용을 받아서 질문, 답, 참고문서를 반환
use_llama_index()
query_engine = build_query_engine(2)

def task(item):
    print(f"item={item}")
    res = query_engine.query(item['input'])
    print(f"response={res}")
    answer = str(res)
    context = [node.get_content() for node in res.source_nodes]
    # for node in res.source_nodes:
    #     context.append(node.get_content())

    return {"input":item['input'], "output":answer, "context":context}

# 평가 - JUDGE LLM 을 활용한 평가
# 원래 평가모델은 7B 이상을 권장
if __name__ == '__main__': # 메인스레드만..
    # 심판 LLM 정의
    judge = LiteLLMChatModel(
        model_name=JUDGE_MODEL,
        api_base=OLLAMA_URL,
        timeout=600,
        num_ctx=8192
    )
    # 평가실행
    evaluate(
        dataset=dataset,    # 사전테스트 시험지와 답
        task=task,          # 질문, 답, 출처 반환 처리
        scoring_metrics=[   # 평가지표
            Hallucination(model=judge),    # 환각(0~1) 낮을수록 좋음
            AnswerRelevance(model=judge)   # 대답의 연관성(0~1) 높을수록 좋음
        ],
        experiment_name='rag_v1',
        experiment_config={'llm':LLM_MODEL,'judge':JUDGE_MODEL},
        task_threads=1
    )
    print('평가 완료 Opik -> Datasets -> haksa-qa -> Experiments 에서 확인하세요')

