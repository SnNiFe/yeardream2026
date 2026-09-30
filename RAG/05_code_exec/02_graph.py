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
print('=== 데이터 불러오기 ===')

### 3. 데이터 분석 프롬프트 작성
system_prompt = f"""
    당신은 주어진 데이터를 분석하는 데이터 분석가 입니다.
    주어진 DataFrame 으로 질문에 답할 수 있는 정보를 출력하는 파이썬 코드를 작성하세요.
    DataFrame 이름은 df_inkjet 이며, 다음과 같은 컬럼들이 있습니다.
    컬럼들 : {columns}
    데이터는 이미 로드되어 있으므로 데이터 로드 코드는 생략하세요.
    그래프를 그릴때는 반드시 out01.png 같은 파일로 저장하도록 코드를 작성해주세요.
    그래프가 여러개일 경우 out01.png, out02.png, .. 와 같이 다른 이름으로 저장하세요.
    반드시 하나의 파일을 저장 후 도화지를 초기화 하여 오류가 나지 않도록 해주세요.
"""

# system_pompt = f"""
#     당신은 주어진 데이터를 분석하는 데이터 분석가 입니다.
#     주워진 DataFrame 으로 요청에 맞는 그래프를 그리는 파이썬 코드를 작성하세요.
#     DataFrame 이름은 df_inkjet 이며, 다음과 같은 컬럼들이 있습니다.
#     컬럼들 : {columns}
#     그리고 아래 내용을 참고해서 작성해 주세요.
#     1. 데이터는 이미 로드되어 있으므로 데이터 로드 코드는 생략
#     2. 레이블과 타이틀은 모두 영문으로만 표기
#     3. matplotlib 라이브러리 사용할 것
# """

### 4. 프롬프트 조립 후 실행
msg_list = [ ("system",system_prompt), ("human","{question}") ]
prompt = ChatPromptTemplate.from_messages(msg_list)
code_gen_chain = {"question":RunnablePassthrough()}|prompt|llm|StrOutputParser()

### 5. 대답에서 코드만 추출
def python_code_parser(text:str):
    code_list = text.replace("```python","```").strip().split("```")
    if len(code_list) == 1:
        return code_list[0]
    return code_list[1]

### 6. chain 으로 코드 추출 조합
code_extract_chain = code_gen_chain|python_code_parser

### 7. 추출한 코드 실행 -> 거기서 출력된 내용을 output 에 담아 밖으로 내보냄
def run_code(input_code:str):
    print('=== CODE ===')
    print(input_code)
    output = io.StringIO() # 문자열이 오갈수 있는 객체
    try:
        with contextlib.redirect_stdout(output):
            # exec(code, 필요한변수)
            exec(input_code,{'df_inkjet':df_inkjet})
            # result = df_inkjet.loc[df_inkjet['Velocity'].idxmax()]
    except Exception as e:
        print(f'Error : {e}',file=output)
    
    return output.getvalue()

# 코드 실행 결과 보기
code_exec_chain = code_extract_chain|run_code
# print(code_exec_chain.invoke("주어진 데이터로 그래프를 그려보고싶어"))
print('코드 생성 중...')
print(code_exec_chain.invoke(
    "데이터를 파악 할 수 있는 분포표를 그려줘, 그리고 plot.png 파일로 저장해줘"))

"""
# seaborn 수동으로 설치함 #
# 1 차 #
데이터 분석이 완료되었으며, 상관관계 히트맵이 'output01.png' 파일로 저장되었습니다.
# 2 차 #
데이터 분석 및 그래프 생성이 완료되었습니다. 결과 파일이 저장되었습니다: out01.png, out02.png, out03.png, out04.png
"""