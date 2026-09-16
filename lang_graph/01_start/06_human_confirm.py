# 1. 저장소 생성
import uuid

from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
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

# 6. 컴파일(저장소,정지포인트)
# checkpointer = 어디에 저장할 것인가?
# inturrupt_before = 어떤 노드 전에 세울 것이냐?
memory = MemorySaver()
app = wf.compile(checkpointer=memory, interrupt_before=['send'])

# 7. 실행
# 현재 이것을 실행하는 thread id 를 지정(어떤 프로세스인지 식별하기 위해)
config = {'configurable':{'thread_id':uuid.uuid4()}}
result = app.invoke({"title":"전사 야유회 참여 공지 메일"},config)

# 메모리에 뭐가 저장되어있는지 확인차원(뭘했는지? 다음에 뭘 할건지?)
state_snapshot = app.get_state(config)
# print(state_snapshot)
print(state_snapshot.values) # 현재 데이터 상태
print(state_snapshot.next) # 대기중인 노드

yn = input('작성된 초안을 승인하고 발송 하시겠습니까?')
if yn.lower().strip() == 'y':
    print('승인 완료 발송 시작')
    print(f'memory : {memory}')
    app.invoke(None, config)
else:
    print('발송이 거부 되었습니다.')

# print(result)