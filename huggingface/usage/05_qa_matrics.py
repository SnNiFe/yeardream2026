import evaluate

qa_matrics = evaluate.load('squad')

# 예측값
predictions = [
    {"id":"1","prediction_text":"Albert Einstein"},
    {"id":"2","prediction_text":"Tokyo"}
]

# 정답
references = [
    {"id":"1","answer":{
        "text":["Albert Einstein"],
        "answer_start":[0] # 정답의 시작점
    }},
    {"id":"2","answer":{
        "text":["Tokyo Japan","Tokyo city"],
        "answer_start":[0,0] # 정답의 시작점
    }}
]

result = qa_matrics.compute(predictions=predictions, references=references)
print(result)