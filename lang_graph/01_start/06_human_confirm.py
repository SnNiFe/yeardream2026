# 1. 저장소 생성
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph
from pydantic import BaseModel


class EmailState(BaseModel):
    title:str=""
    email_detail:str=""

# 2. 모델 호출
llm = ChatOllama(model="gemma4:e2b", temperature=2) # gemma4:e4b

# 3. 노드/라우터함수 선언
def write_mail_node(state:EmailState) -> EmailState:
    """주어진 제목으로 이메일을 작성하는 노드"""
    prompt = f"""
    당신은 사내메일 작성 담당자 입니다.
    제목 - {state.title}
    에 대한 이메일을 정중하고 격식있는 어조로 한글로만 작성해 주세요.
    불필요한 설명이나 참고, 팁 등은 필요없이 오직 메일 내용만 출력하세요.
    """
    print('메일 작성 중...')
    resp = llm.invoke(prompt)
    print(f'[메일 작성 완료]')
    content = resp.content.strip().replace("*","")
    # print(content)
    state.email_detail = content
    return state

def send_mail_node(state:EmailState) -> None:
    """메일을 발송해 주는 노드"""
    print("메일이 발송 되었습니다.")
    print("[발송된 내용]")
    print(state.email_detail)

# 4. 저장소,노드 등록
wf = StateGraph(EmailState)
wf.add_node("writer",write_mail_node)
wf.add_node("send",send_mail_node)

# 5. 엣지 등록(조립)
wf.set_entry_point("writer")
wf.add_edge("writer","send")
wf.add_edge("send",END)

# 6. 컴파일
app = wf.compile()

# 7. 실행
result = app.invoke({"title":"전사 야유회 참여 공지 메일"})
print(result)