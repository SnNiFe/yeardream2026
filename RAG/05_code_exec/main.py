import contextlib
import io

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import pandas as pd

from langchain_ollama import ChatOllama

### 1. 모델 설정 및 지정
llm = ChatOllama(model="gemma4:e2b")

### 2. 데이터 불러오기
data_path = 'data/InkjetDB_preprocessing.csv'
df_inkjet = pd.read_csv(data_path,index_col=0)
columns = ",".join(df_inkjet.columns)
# print(columns)

### 3. 데이터 분석 프롬프트 작성
system_prompt = f"""
    당신은 주어진 데이터를 분석하는 데이터 분석가 입니다.
    주어진 DataFrame 으로 질문에 답할 수 있는 정보를 출력하는 파이썬 코드를 작성하세요.
    DataFrame 이름은 df_inkjet 이며, 다음과 같은 컬럼들이 있습니다.
    컬럼들 : {columns}
    데이터는 이미 로드되어 있으므로 데이터 로드 코드는 생략하세요.
"""
# print(system_prompt)

### 4. 프롬프트 조립 후 실행
# 'human', 'user', 'ai', 'assistant', 'system'
msg_list = [ # 메시지리스트 안의 개별메시지는 Tuple 형태여야 한다.
    ("system",system_prompt), # AIMessage(content=system_prompt)
    ("human","{question}")    # HumanMessage(content="{question}")
]
prompt = ChatPromptTemplate.from_messages(msg_list)
code_gen_chain = {"question":RunnablePassthrough()}|prompt|llm|StrOutputParser()
# result = code_gen_chain.invoke("Velocity가 가장 큰 데이터를 찾고 싶어")
# print(result)

""" # 출력 결과 #
# Velocity가 가장 큰 데이터를 찾기 위해 'Velocity' 컬럼을 기준으로 최대값을 찾습니다.
# 1. 'Velocity' 컬럼의 최댓값을 가진 행의 인덱스를 찾습니다.
max_velocity_index = df_inkjet['Velocity'].idxmax()
# 2. 해당 인덱스를 사용하여 전체 데이터프레임에서 해당 행을 선택합니다.
max_velocity_data = df_inkjet.loc[max_velocity_index]
# 결과 출력
print(max_velocity_data)
"""

### 5. 대답에서 코드만 추출
def python_code_parser(text:str):
    # 대답중에서 ```python 으로 감싸진 부분만 받아오는 함수
    # ```python -> ``` -> [```,code내용,```]
    code_list = text.replace("```python","```").strip().split("```")

    # ``` 이 없어서 끊지 못한 경우 코드를 그대로 내보낸다.
    if len(code_list) == 1:
        return code_list[0]
    return code_list[1]

# print('###'*30)
# print(python_code_parser(result))

""" # 출력 결과 #
# Velocity가 가장 큰 데이터를 찾기 위해 'Velocity' 컬럼을 기준으로 최대값을 찾습니다.
max_velocity_data = df_inkjet.loc[df_inkjet['Velocity'].idxmax()]
print(max_velocity_data)
"""

### 6. chain 으로 코드 추출 조합
code_extract_chain = code_gen_chain|python_code_parser
# print(code_extract_chain.invoke("Velocity가 가장 큰 데이터를 찾고 싶어"))

""" # 출력 결과 #
# Velocity가 가장 큰 데이터를 찾기 위해 DataFrame에서 Velocity 컬럼을 기준으로 정렬하고 첫 번째 행을 선택합니다.
# 방법 1: sort_values를 사용하여 내림차순 정렬 후 첫 번째 행 선택 (가장 직관적)
max_velocity_data = df_inkjet.sort_values(by='Velocity', ascending=False).iloc[0]
print(max_velocity_data)
# 또는 방법 2: idxmax를 사용하여 최대값을 가진 행의 인덱스를 찾은 후 해당 행을 선택 (더 효율적)
# max_index = df_inkjet['Velocity'].idxmax()
# max_velocity_data_idxmax = df_inkjet.loc[max_index]
# print(max_velocity_data_idxmax)
"""

### 7. 추출한 코드 실행 -> 거기서 출력된 내용을 output 에 담아 밖으로 내보냄
def run_code(input_code:str):
    # 코드를 실행했을때 print 된 내용을 보고싶다.
    output = io.StringIO() # 문자열이 오갈수 있는 객체
    try:
        # 무언가 출력이 나오면 output 으로 보내서 저장해라
        # 아래 코드가 실행되는 동안만(with 로 인해 다 끝나면 자동으로 자원은 닫힌다.)
        with contextlib.redirect_stdout(output):
            # exec(code, 필요한변수)
            exec(input_code,{'df_inkjet':df_inkjet})
            # result = df_inkjet.loc[df_inkjet['Velocity'].idxmax()]
    except Exception as e:
        print(f'Error : {e}',file=output)
    
    return output.getvalue()

# 코드 실행 결과 보기
code_exec_chain = code_extract_chain|run_code
print(code_exec_chain.invoke("Velocity가 가장 큰 데이터를 찾고 싶어"))

""" # 출력 결과 #
Viscosity          8
Velocity           9
PrintingSpeed    250
PatternSize       14
Name: 125, dtype: int64
"""