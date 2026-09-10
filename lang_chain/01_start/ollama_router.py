from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

model = ChatOllama(model="exaone3.5:2.4b")

prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 어려운 기술을 알기쉽게 설명해주는 전문가 입니다."),
    ("user","{topic} 에 대해서 설명해 주세요")
])

q = input("질문 내용을 입력 하세요:\n")

chain = prompt|model|StrOutputParser()

for chunk in chain.stream({"topic":q}):
    print(chunk,end='',flush=True)