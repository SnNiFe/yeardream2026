# main stream
from langgraph.graph import END

from node_func import excel_data, get_state, init_answer, plain_answer, router, vector_db


# Lang Graph
# State : 그래프 내에서 공유하는 상태객체
wf = get_state()

# node 등록
wf.add_node('init_answer',init_answer) # 첫 질문 노드
wf.add_node('router',router) # 질문 분배 노드
wf.add_node('plain_answer',plain_answer) # 일반답변
# 엑셀 데이터를 이용한 답변 노드
wf.add_node('excel_data',excel_data)
# vectorDB 검색을 이용한 답변 노드
wf.add_node('vector_db',vector_db)

# 시작점(set_entry_point) 등록
wf.set_entry_point('init_answer')
# 조건부 edge 등록
wf.add_conditional_edges(
    'init_answer',
    router,
    {
        'plain':'plain_answer',
        'excel':'excel_data',
        'vecotr':'vector_db'
    }
)

# edge 등록
wf.add_edge('plain_answer',END)
wf.add_edge('excel_data',END)
wf.add_edge('vector_db',END)

# compile 및 실행
app = wf.compile()
query = input('readme.md 질문 내용중 하나를 입력하세요.')
result = app.invoke({'question':query})
print(result)