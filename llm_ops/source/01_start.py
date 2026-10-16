# 기본적으로 lang-chain 을 이용하여 연결
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from opik.integrations.langchain import OpikTracer

from commons import LLM_MODEL, OLLAMA_URL, PROJECT_NAME

# 1. opik tracer 등록(tags = 기록 검색용 꼬리표)
tracer = OpikTracer(project_name=PROJECT_NAME,tags=['langchain','ollama'])

# 2. 모델 호출
llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_URL, temperature=0)

# 3. 프롬프트 입력
prompt = ChatPromptTemplate.from_messages([
    ("system","너는 대학교 학사 안내 전문가야. 모르는 내용은 모른다고 답해"),
    ("human","{question}")
])

chain = prompt|llm

questions = [
    "수강신청은 어디서 하나요?",
    "졸업하려면 몇 학점이 필요한가요?",
    "오늘 학생식당 메뉴는 뭐예요?"
]

for q in questions:
    # 질문과 결과를 tracer 에게 전달
    result = chain.invoke({'question':q},config={'callbacks':[tracer]})
    print(f"Q : {q} \nA : {result.content}\n")


# 4. 모든 기록 서버에 전송
tracer.flush()
print(f"전송 완료 Opik > Projects > {PROJECT_NAME} 에서 Traces 를 확인하세요")