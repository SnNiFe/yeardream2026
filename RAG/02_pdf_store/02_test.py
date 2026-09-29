# collection : lecture
# 과목 : FAST API, PANDAS, SCIKIT-LEARN 중 택일(모두 해도 상관 없음)
# 시험용 LLM 제작



# 1. 임베딩 함수 지정(chromadb 의 기본 임베딩을 사용하지 않을 경우)
import os
import chromadb
import tiktoken
from PyPDF2 import PdfReader
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="nomic-embed-text:latest",
    timeout=300.0  # 타임아웃을 300초(5분)로 연장
)

# 2. chromadb 선언시 임베딩 함수를 지정
client = chromadb.PersistentClient(path="./store")
coll = client.get_or_create_collection(
    name="lecture",
    embedding_function=ollama_ef
)

# 3. 토크나이징(쪼개기 작업)
# 3-1. 토크나이저 등록
# cl100k_base 이라는 인코딩 규칙으로 토큰을 생성하는(쪼개는) 토크나이저 부름
tokenizer = tiktoken.get_encoding("cl100k_base")

def my_tokenizer(text:str) -> int:
    text = text.strip()
    if len(text) < 2: # 2글자 미만은 토크나이징 안함
        return 0
    # 사용될 토큰 크기 반환
    #print(f"text:{text}")
    token_len = len(tokenizer.encode(text))
    #print(f'token size : {token_len}')
    return token_len

# 4. 데이터 저장
def insert_data(path:str) -> None:
    # 4-1. 특정 PDF 를 불러와 읽는다.
    reader = PdfReader(path)
    # 1. 파일 이름 추출 (예: 'data/pandas.pdf' -> 'pandas')
    file_name = os.path.splitext(os.path.basename(path))[0]
    text = ''
    for page in reader.pages: # PDF 페이지들을 한장씩 꺼내서
        extracted = page.extract_text()
        if extracted: # None 이 아닌 경우만
            text += extracted # 텍스트를 추출 후 text 변수에 누적시킨다.

    # 9페이지짜리 문자를 통으로 넣을수 없기에 잘라줘야 한다.(chunking 작업)
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=800, # 최대 청크 크기
        chunk_overlap= 50, # 청크간 전후 문맥 파악을 위해 겹쳐지는 수
        length_function=my_tokenizer, # 토큰의 길이를 뭘로 정해?
    )
    # 데이터 끊어주기
    chunks = text_spliter.split_text(text)
    #print(f'chunks = {chunks}')
    # chromadb 에 입력
    ids = [f"{file_name}_{i}" for i in range(len(chunks))]

    # 3. 권장 추가: 검색 시 출처를 확인할 수 있도록 메타데이터 부여
    metadatas = [{"source": file_name, "chunk_index": i} for i in range(len(chunks))]

    # 한 번에 요청할 청크 개수
    batch_size = 10
    print(f"[{file_name}] 총 {len(chunks)}개 청크 저장 시작...")
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i : i + batch_size]
        batch_ids = ids[i : i + batch_size]
        batch_metas = metadatas[i : i + batch_size]
        # 0개씩 끊어서 Ollama에 전달
        coll.upsert(documents=chunks,ids=ids,metadatas=metadatas)
        print(f"진행 중: {min(i + batch_size, len(chunks))} / {len(chunks)} 완료")
    print(f'{file_name} 저장 완료, {len(chunks)}개 문맥 확보')

# insert_data('data/pandas.pdf')
# insert_data('data/FASTAPI.pdf')
# insert_data('data/scikit_learn.pdf')

def search_data(query:str) -> None:
    # print(f'질문내용 : {query}')
    results = coll.query(
        query_texts=[query],
        n_results=3, # 청크 개수 제한
    )
    # print(results) # chroma db 에서 가져온 내용
    # 가져온 리스트 안의 내용을 줄바꿈 두번으로 붙여서 하나의 텍스트로 만든다.
    context = "\n\n".join(results['documents'][0])

    # llm 에 전달할 프롬프트 작성
    prompt = f"""
    당신은 코딩, 분석 전문가 입니다. 제공된 [강의자료]를 바탕으로 사용자의 [질문]에 답하세요.
    없는 말을 지어내지말고, 자료와 다른 답변을 해선 안됩니다.
    최대한 간결하게 사용자의 질문과 관련 된 답변만 해주세요.
    예시는 너무 길지 않게 최대 1개만 적어주세요.
    
    [강의자료]
    {context}
    
    [질문]
    {query}    
    """
    print('llm model loading..')
    resp = ollama.generate(
        model='gemma4:e2b',
        prompt=prompt,
        stream=True,
        options={
            "num_predict":1024,   # 출력토큰 수(-1:무제한)
            "num_ctx":2048,      # 입력+출력 합친 컨텍스트 크기
            "temperature": 0.2     # 강의자료 기반이므로 창의성 낮추고 정확도 유지
        }
    )
    for chunk in resp:
        print(chunk['response'],end="", flush=True)

        if chunk.get('done'):
            print('\n')
            print(f"중지이유 : {chunk.get('done_reason')}")

question = input('(pandas, fastapi, scikit-learn 관련) 질문을 해주세요\n')
search_data(question)

