import pandas as pd

from langchain_ollama import ChatOllama

### 1. 모델 설정 및 지정
llm = ChatOllama(model="gemma4:e2b")

### 2. 데이터 불러오기
data_path = 'data/InkjetDB_preprocessing.csv'
df = pd.read_csv(data_path,index_col=0)
columns = ",".join(df.columns)
# print(columns)

### 3. 데이터 분석 프롬프트 작성
system_prompt = f"""
    당신은 주어진 데이터를 분석하는 데이터 분석가 입니다.
    주어진 DataFrame 으로 질문에 답할 수 있는 정보를 출력하는 파이썬 코드를 작성하세요.
    DataFrame 이름은 df_inkjet 이며, 다음과 같은 컬럼들이 있습니다.
    컬럼들 : {columns}
    데이터는 이미 로드되어 있으므로 데이터 로드 코드는 생략하세요.
"""
print(system_prompt)