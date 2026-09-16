# 1. 상태 객체
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph
from pydantic import BaseModel


class TaskState(BaseModel):
    title:str = ""        # 메일 제목
    detail:str = ""       # 상세 내용
    approval:bool = True  # 수락 여부

# 2. 모델 호출
llm = ChatOllama(model="gemma4:e2b", temperature=1.5)

# 3. 노드/라우터 함수 정의
def write_mail_node(state:TaskState) -> TaskState:
    """주어진 제목으로 메일 작성하는 노드"""
    prompt = f"""
    당신은 메일 작성 담당자 입니다.
    제목 - {state.title}
    에 대한 이메일의 내용과 분위기를 파악하여 어울리는 어조로 한글로만 작성해 주세요.
    불필요한 설명이나 참고, 팁 등은 필요없이 오직 메일 내용만 출력하세요.
    """
    resp = llm.invoke(prompt)
    content = resp.content.strip().replace("*","")
    state.detail = content
    return state

def send_mail_node(state:TaskState) -> None:
    """메일 전송하는 노드"""
    print('[메일 전송 시작]')
    print(state.detail)

def router(state:TaskState) -> str:
    """state.approval 여부에 따라 문자열 반환"""
    if state.approval:
        return "go_send"
    else:
        return "go_write"
    
# 4. 저장소/노드 등록
wf = StateGraph(TaskState)
wf.add_node("writer",write_mail_node)
wf.add_node("send",send_mail_node)

# 5. 엣지 조립
wf.set_entry_point("writer")
wf.add_edge("writer","send")
wf.add_edge("send",END)

# 6. 컴파일
app = wf.compile()

# 7. 실행
title = input('작성하고 싶은 메일의 제목을 정하세요\n')
app.invoke({'title':title})