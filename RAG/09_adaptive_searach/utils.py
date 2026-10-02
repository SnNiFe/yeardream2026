from datetime import datetime
import contextlib
import io


def retrieve_to_text(docs):
    text = ''
    for doc in docs:
        text += doc.page_content+'\n'
    return text

### 대답에서 코드만 추출
def python_code_parser(text:str):
    # 대답중에서 ```python 으로 감싸진 부분만 받아오는 함수
    # ```python -> ``` -> [```,code내용,```]
    code_list = text.replace("```python","```").strip().split("```")

    # ``` 이 없어서 끊지 못한 경우 코드를 그대로 내보낸다.
    if len(code_list) == 1:
        return code_list[0]
    return code_list[1]

### 추출한 코드 실행 -> 거기서 출력된 내용을 output 에 담아 밖으로 내보냄
def run_code(df_name,df,input_code:str):
    # 코드를 실행했을때 print 된 내용을 보고싶다.
    output = io.StringIO() # 문자열이 오갈수 있는 객체
    try:
        # 무언가 출력이 나오면 output 으로 보내서 저장해라
        # 아래 코드가 실행되는 동안만(with 로 인해 다 끝나면 자동으로 자원은 닫힌다.)
        with contextlib.redirect_stdout(output):
            # exec(code, 필요한변수)
            exec(input_code,{df_name:df})
            # result = df_inkjet.loc[df_inkjet['Velocity'].idxmax()]
    except Exception as e:
        print(f'Error : {e}',file=output)
    
    return output.getvalue()


def save_chat_log(state, file_path: str = "chat_log.txt"):
    """대화 로그를 txt 파일에 누적 기록합니다."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"""
    ==================================================
    [일시: {timestamp}] [경로: {route}]
    - 질문: {question}
    - 답변:
    {answer}
    """
    # 'a' 모드는 파일이 없으면 새로 만들고, 있으면 끝에 이어 씁니다.
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(log_entry.strip() + "\n")