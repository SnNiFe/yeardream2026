from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# 모델 호출
model =ChatOllama(model="exaone3.5:2.4b")

# 프롬프트 작성
prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 답변 전문 AI 모델 입니다. 주어진 질문에 대해서 핵심만 간단히 대답하세요"),
    ("user","{query}")
])

# 파이프라인 조립
chain = prompt|model

# 실행 및 출력
while True:
    query = input('\n당신> ')

    if query == '/exit' or query == '/bye':
        print('대화를 종료 합니다.')
        break

    for chunk in chain.stream({'query':query}):
        print(chunk.content,end='',flush=True)