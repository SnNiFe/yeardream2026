# main stream
import uuid

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END
from node_func import end_point_answer, excel_answer, excel_data, get_state, init_answer, plain_answer, router, vector_db


# Lang Graph
# State : 그래프 내에서 공유하는 상태객체
wf = get_state()

# node 등록
wf.add_node('init_answer',init_answer) # 첫 질문 노드
wf.add_node('router',router) # 질문 분배 노드
wf.add_node('plain_answer',plain_answer) # 일반답변
# 엑셀 데이터를 이용한 답변 노드
wf.add_node('excel_data',excel_data)
wf.add_node('excel_answer',excel_answer)
# vectorDB 검색을 이용한 답변 노드
wf.add_node('vector_db',vector_db)
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
        'excel':'excel_data',
        'vector':'vector_db'
    }
)

# edge 등록
wf.add_edge('plain_answer','end_point')
wf.add_edge('excel_data','excel_answer')
wf.add_edge('excel_answer','end_point')
wf.add_edge('vector_db','end_point')
wf.add_edge('end_point',END)

# MemorySaver 를 통해 compile 시 checkpoint 지정
memory = MemorySaver()
app = wf.compile(checkpointer=memory)
config = {'configurable':{'thread_id': uuid.uuid4()}}

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
# print(history.values['context'])
for ctx in history.values['context']:
    print(ctx)