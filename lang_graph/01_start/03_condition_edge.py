from langchain_ollama import ChatOllama
from pydantic import BaseModel

# 1. 저장소 준비
class SupportState(BaseModel):
    query:str = ""
    dept:str = ""
    response:str = ""

# 2. 모델 준비
llm = ChatOllama(model="gemma4:e2b", temperature=0)

# 3. 노드에 등록할 함수 준비
def analyzer_node(state:SupportState) -> SupportState:
    """고객의 문의를 받아서 어느 부서 문의인지 분류해주는 노드"""
    print('[analyzer_node] 고객문의 분석중...')
    prompt = f"""
    당신은 고객문의 분류 전문가 입니다.
    [고객문의] 를 분석하여 'billing' 또는 'technical' 중 하나로만 대답하세요.
    반드시 다른 설명이나 문장없이 딱 한 단어 'billing' 또는 'technical' 중 하나로만 답할것
    [분류 기준]
    - billng : 결제, 환불, 요금제, 구독, 영수증, 가격 관련 문의
    - technical : 앱 오류, 로그인 실패, 화면 멈춤, 네트워크 문제 등의 시스템 장애 관련 문의
    [고객문의]
    {state.query}
    """
    resp = llm.invoke(prompt)
    dept = resp.content.strip().lower()

    if 'billing' in dept:
        state.dept = 'billing'
    else:
        state.dept = 'technical'

    print(f'고객문의 분류 완료 {dept} -> {state.dept}')

    return state

def billing_node(state:SupportState) -> SupportState:
    """결제 관련 문의를 답변해 주는 노드"""
    state.response = "결제 및 환불 관련 안내 : 마이페이지 > 결제내역에서 신청하세요"
    return state

def technical_node(state:SupportState) -> SupportState:
    """앱 또는 기술관련 문의를 답변해 주는 노드"""
    state.response = "기술지원 안내 : 이용에 불편을 드려서 죄송합니다. 곧 복구하도록 하겠습니다."
    return state

def route_by_dept(state:SupportState) -> str:
    """조건에 따라서 각기 다른 노드로 보내주는 함수"""
    node_name = "go_to_bill"
    if state.dept == "technical":
        node_name = "go_to_tech"
    return node_name

# 4. 저장소/노드 등록

# 5. 엣지등록

# 6. 컴파일

# 7. 실행