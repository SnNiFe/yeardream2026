
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

# 최적화 도구(생략)