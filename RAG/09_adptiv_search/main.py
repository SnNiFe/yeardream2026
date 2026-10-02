"""
1. init_answer 에서 질문을 통해 RAG 에게 데이터를 받아온다.
2. router 에서 이 데이터가 질문에 적합한지 판단
3. 적합하면 RAG 답변을 통해서 종결
4. 부적합 하면 plain 이나 web 으로 데이터 검색
5. 해당 데이터로 답변 생성후 종결
"""
from langgraph.graph import END

from node_list import *

wf = get_state()

# 노드 등록
wf.add_node('init_answer',init_answer)
wf.add_node('plain',plain)
wf.add_node('web',web_search)
wf.add_node('last_answer',last_answer)

# 순서 등록
wf.set_entry_point('init_answer')

wf.add_conditional_edges(
    'init_answer',
    router,
    {
        'rag':'last_answer', # router 반환값: 가야할노드명
        'plain':'plain',
        'web':'web'
    }
)

wf.add_edge('web','last_answer')
wf.add_edge('plain','last_answer')
wf.add_edge('last_answer',END)

# 실행
app = wf.compile()
query = input('질문 내용을 입력 하세요\n')
# result = app.invoke({'question':query})
# print(result)

for chunk in app.stream({'question':query}, stream_mode='messages'):
    print(chunk[0].content, end='', flush=True)