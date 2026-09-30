
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama

# 모델 생성
model = ChatOllama(base_url='http://localhost:11434', model="gemma4:e2b", temperature=0.2)

# 프롬프트 생성
prompt = ChatPromptTemplate.from_template("""
    당신은 어려운 내용을 알기쉽게 가르쳐주는 강사 입니다.
    [질문]의 내용을 아래 [참고문서]의 내용만으로 알기 쉽게 설명해주세요.
    [참고문서]에 없는 내용은 "참고문서에 없는 내용은 답변이 어렵습니다." 라고 대답하세요.

    [참고문서]
    {context}

    [질문]
    {query}
""")

# 받아온 쿼리문, 검색기, 프롬프트를 조합해서 실행
def get_answer(query:str, search):
    chain = {'query':RunnablePassthrough(),'context':search}|prompt|model|StrOutputParser()

    for chunk in chain.stream(query):
        yield chunk
    return None