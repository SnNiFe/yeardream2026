from typing import Annotated, TypedDict
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from langgraph.graph import add_messages

# 1. 상태 저장소 생성 : class 를 Dictionary 처럼 여기게 해줌
class AgentState(TypedDict):
    # Lang Graph 에서는 상태를 덮어쓰는것을 원칙으로하고 있다.
    # Annotated[데이터타입,규칙] 을 통해서 규칙을 변경하고자 함
    # 어노테이션(@) - 컴파일러에게 미리 힌트를 주는 개념
    messages:Annotated[list[BaseMessage],add_messages]

# 2. 모델 생성
llm = ChatOllama(model="gemma4:e2b", temperature=0) # gemma4:e4b

# 3. 툴 생성
@tool
def multiply(a:int, b:int) -> int:
    """
    두 정수를 곱하는 계산기 도구 입니다. 곱셈이 필요할 때만 이 도구를 사용 하세요.

    Args:
        a:첫번째 정수
        b:두번쨰 정수
    """
    print(f'{a}*{b} 를 구하는 도구 실행')
    return a * b

# 4. 툴 등록
tools = [multiply]
model = llm.bind_tools(tools)

# 5. 노드 및 라우트함수 선언

# 6. 노드 등록

# 7. 엣지 조립

# 8. 컴파일

# 9. 실행