# 1. 상태 객체
import uuid

from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
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
    print('메일 작성 중...')
    resp = llm.invoke(prompt)
    content = resp.content.strip().replace("*","")
    # state.approval = True
    state.detail = content
    return state

def send_mail_node(state:TaskState) -> None:
    """메일 전송하는 노드"""
    print('[메일 전송 시작]')
    print(state.detail)

def router(state:TaskState) -> str:
    """state.approval 여부에 따라 문자열 반환"""
    print(f'state.approval : {state.approval}')
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
# wf.add_edge("writer","send")
wf.add_conditional_edges(
    "writer",
    router,
    {
        "go_send":"send",
        "go_write":"writer"
    })
wf.add_edge("send",END)

# 6. 컴파일(저장소,멈춤 위치)
app = wf.compile(checkpointer=MemorySaver(), interrupt_after=['writer'])

# 7. 실행
config = {'configurable':{'thread_id':uuid.uuid4()}}
title = input('작성하고 싶은 메일의 제목을 정하세요\n')
app.invoke({'title':title},config)

while True:
    snap_shot = app.get_state(config)
    print(snap_shot.values)
    print(snap_shot.next)

    yn = input('작성된 초안을 승인하고 발송 하시겠습니까?\n')
    if yn.strip().upper() == 'Y':
        print('승인 완료!')
        # writer node 에서 approval 을 True/False 로 변경할 거다.
        app.update_state(config,{"approval":True}, as_node="writer")
        app.invoke(None, config)
        break
    else:
        print('발송 거부, 이메일 재작성')
        # writer node 에서 approval 을 True/False 로 변경할 거다.
        app.update_state(config,{"approval":False}, as_node="writer")
        app.invoke(None, config)