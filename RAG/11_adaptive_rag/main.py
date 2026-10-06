"""
1. init 에서 RAG 답변을 받는다.
2. router 를 통해 노드 이동
2-1. 적당한 답변이면 그대로 대답노드에 전달
2-2. 모델 스스로 답변이면 데이터를 지우고 대답노드로 이동
2-3. 검색이 필요한 경우 인터넷 검색으로 가져온 데이터를 대답 노드에 전달
"""
from langgraph.graph import END

from node_funcs import *

wf = get_state()

# 노드 등록
wf.add_node('init_answer',init_answer)
wf.add_node('plain',plain)
wf.add_node('web',web)
wf.add_node('last_answer',last_answer)

# 흐름 배치(시작점, 라우터, 경로)
wf.set_entry_point('init_answer')
wf.add_conditional_edges(
    'init_answer',
    router,
    {
        'rag':'last_answer',
        'web':'web',
        'plain':'plain'
    }
)
wf.add_edge('web','last_answer')
wf.add_edge('plain','last_answer')
wf.add_edge('last_answer',END)

# compile 및 실행
app = wf.compile()
query = input('질문 내용을을 입력하세요!\n')
# result = app.invoke({'question':query})
# print(f"최종결과 : {result}")

for chunk in app.stream({'question':query}, stream_mode="messages"):
    print(chunk[0].content,end="",flush=True)