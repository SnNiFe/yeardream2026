import dspy

# 1. model 연결
llm = dspy.LM(model="ollama/gemma4:e2b")
dspy.configure(lm=llm)

# 2. 시그니처 - 무엇을 할 것인가?
# 프롬프트를 question -> answer 형태로 정의
class QuestionAnswer(dspy.Signature):
    """주어진 질문에 대해 친절한 말투로 한국어로 대답합니다.""" # system prompt
    question = dspy.InputField(desc="사용자가 궁금해하는 질문") # 입력필드 설명
    answer = dspy.OutputField(desc="질문에 대한 간결한 답변") # 츨력필드 설명

# 모듈 - 어떻게 처리할 것인가?(어떤 종류의 추론?)
# 기본예측, 생각 사슬기법 등...
qa_system = dspy.ChainOfThought(QuestionAnswer)
resp = qa_system(question="로컬 LLM을 사용하면 보안상 어떤점이 좋아?")
print("생각중...")
print(resp.answer)
llm.inspect_history(n=1) # 전달된 프롬프트
# module                    역활 및 프롬프트 기법                                            활용예시/특징
# dspy.Predict              가장 기본이 되는 단발성 입력-출력 예측단순                           분류, 번역, 텍스트 추출
# dspy.ChainOfThought       답변 생성 전에 생각의 과정(Rationale)을 거침                        논리적 추론, 계산, 질문 답변
# dspy.ProgramOfThought     텍스트 대신 파이썬 코드를 생성하여 실행 후 결과를 바탕으로 답함          복잡한 수학 연산, 데이터 분석 및 계산
# dspy.ReAct                외부 도구(검색, 계산기 등)를 사용할 수 있는 에이전트(Agent) 구조        웹 검색 기반 Q&A, 데이터베이스 조회
# dspy.MultiChainComparison 여러 개의 추론 경로를 생성한 후 비교하여 최선의 답을 선택               복잡한 의사결정, 정확도가 중요한 문제
# dspy.Majority             동일한 질문에 대해 여러 번 생성(Self-Consistency) 후 다수결 투표답변   안정성이 중요한 추론

# 최적화 도구(생략)