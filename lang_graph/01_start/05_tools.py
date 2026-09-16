from typing import Annotated, Dict, TypedDict
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph, add_messages

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
# 호출을 하기위한 등록
tools_dict={} # {name:funtion} 저장하여 name 을 부르면 해당 funciton이 나오도록
for tool in tools:
    tools_dict[tool.name] = tool

# 5. 노드 및 라우트함수 선언
def agent_node(state:AgentState) -> Dict:
    """사용자의 질문을 받아 응답하는 노드"""
    print('사용자 메시지를 받아서 분석중...')
    resp = model.invoke(state['messages'])
    # print(f"[AGENT NODE]     {resp}")
    return {'messages':[resp]}

def tool_node(state:AgentState) -> Dict:
    """LLM 의 요청에 따라서 필요한 툴을 실행하는 노드"""
    # 메시지들 중에서 직전의(마지막) 메시지인 AIMessage 를 가져온다.
    last_msg = state['messages'][-1]

    msg_list = []
    for call in last_msg.tool_calls:
        name = call['name']
        args = call['args']
        call_id = call['id']
        # print(f'id : {call_id} 실행!!')
        # print(f'[TOOL NODE]     {name}({args})')
        func = tools_dict[name] # 함수를 꺼내온 다음
        result = func.invoke(args)   # 실행
        print(f'실행 결과 값 : {result}')
        msg_list.append(ToolMessage(content=str(result),tool_call_id=call_id))

    return {'messages':msg_list}

def should_continue(state:AgentState) -> str:
    """LLM 최근 메시지 에서 tool_calls 가 있으면 call_tool 로, 아니면 go_end 로 반환한다."""
    last_msg = state['messages'][-1]
    if len(last_msg.tool_calls):
        return "call_tool"
    else:
        return "go_end"

# 6. 저장소 및 노드 등록
wf = StateGraph(AgentState)
wf.add_node("agent",agent_node)
wf.add_node("tool",tool_node)

# 7. 엣지 조립
wf.set_entry_point("agent")
# wf.add_edge("agent","tool")
# wf.add_edge("tool",END)
wf.add_conditional_edges(
    "agent",
    should_continue,
    {
        "call_tool":"tool",
        "go_end":END
    })
wf.add_edge("tool","agent")
# 8. 컴파일
app = wf.compile()
# 9. 실행
for node in app.stream({'messages':[HumanMessage(content="256 곱하기 4가 무엇인지 계산해 주세요")]},stream_mode="updates"):
    for key,val in node.items():
        print(f'[{key}]     {val}')
"""
HumanMessage    : 사용자가 보내는 메시지(content)
AIMessage       : LLM 모델이 생성한 메시지(content,tool_calls)
ToolMessage     : Tool 이 수행후 반환하는 메시지(content,tool_call_id)
"""