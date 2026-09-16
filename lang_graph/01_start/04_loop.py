# 1. 저장소 생성
from langchain_ollama import ChatOllama
from pydantic import BaseModel


class WriteState(BaseModel):
    topic:str=''    # 글의 주제
    draft:str=''    # 작성된 초안
    feedback:str='' # 피드백 내용
    state:str=''    # 통과(PASS), 재시도(RETRY)
    count:int=0     # 시도 횟수(일정 횟수를 넘으면 중지하려고)

# 2. 모델 생성
llm = ChatOllama(model="gemma4:e2b") # gemma4:e4b

# 3. 노드 및 라우터함수 선언
def write_node(state:WriteState) -> WriteState:
    """카피를 최초 또는 피드백에 의거 재작성 하는 노드"""
    return state

def critic_node(state:WriteState) -> WriteState:
    """카피를 검증하고 승인려부와 피드백을 반환하는 노드"""
    return state

def route_by_review(state:WriteState) -> str:
    """PASS / RETRY 에 따라서 다른 노드로 갈수있는 문자열을 반환"""
    return "go_retry"

# 4. 저장소 등록

# 5. 노드 등록

# 6. 엣지 등록(조립)

# 7. 컴파일

# 8. 실행
