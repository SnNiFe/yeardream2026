import uuid

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END
from node_func import end_point_answer, get_state, init_answer, plain_answer, router, search, vector_db, web_answer

# Lang Graph
# State : 그래프 내에서 공유하는 상태객체
wf = get_state()

# node 등록
wf.add_node('init_answer',init_answer) # 첫 질문 노드 (rag, plain, web)
wf.add_node('router',router) # 질문 분배 노드
# 일반 답변 노드
wf.add_node('plain_answer',plain_answer)
# (RAG)vectorDB 검색을 이용한 답변 노드
wf.add_node('vector_db',vector_db)
# web 검색을 이용한 답변 노드
wf.add_node('search',search)
wf.add_node('web_answer',web_answer)
# 최종 답변 노드(context 저장을 위해)
wf.add_node('end_point',end_point_answer)

# 시작점(set_entry_point) 등록
wf.set_entry_point('init_answer')
# 조건부 edge 등록
wf.add_conditional_edges(
    'init_answer',
    router,
    {
        'plain':'plain_answer',
        'rag':'vector_db',
        'web':'search'
    }
)

# edge 등록
wf.add_edge('plain_answer','end_point')
wf.add_edge('vector_db','end_point')
wf.add_edge('search','web_answer')
wf.add_edge('web_answer','end_point')
wf.add_edge('end_point',END)

# MemorySaver 를 통해 compile 시 checkpoint 지정
memory = MemorySaver()
app = wf.compile(checkpointer=memory)
config = {'configurable':{'thread_id': str(uuid.uuid4())}}

while True:
    query = input('질문을 입력하세요.(종료는 exit)\n')
    if query == 'exit':
        break
    else:
        result = app.invoke({'question':query},config)
        print(result['generation'])

# 저장상황 확인
print('대화 종료, 저장상황 확인')
history = app.get_state(config)
for ctx in history.values['context']:
    print(ctx)
