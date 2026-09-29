# 1. 임베딩 함수 지정(chromadb 의 기본 임베딩을 사용하지 않을 경우)
import chromadb
import ollama
import tiktoken
from PyPDF2 import PdfReader
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="nomic-embed-text:latest"
)

# 2. chromadb 선언시 임베딩 함수를 지정
client = chromadb.PersistentClient(path="./store")
coll = client.get_or_create_collection(
    name="novel",
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
    # print(f"text:{text}")
    token_len = len(tokenizer.encode(text))
    # print(f'token_size : {token_len}')
    return token_len

# 4. 데이터 저장
def insert_data(path:str) -> None:
    # 4-1. 특정 PDF 를 불러와 읽는다.
    reader = PdfReader(path)
    text = ''
    for i, page in enumerate(reader.pages): # PDF 페이지들을 한장씩 꺼내서
        text += page.extract_text() # 텍스트를 추출 후 text 변수에 누적시킨다.
        # print(f'{i} PAGE')
        # print(text)

    # 9페이지짜리 문자를 통으로 넣을 수 없기에 잘라줘야한다.(chunking 작업)
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=800, # 최대 청크 크기
        chunk_overlap=50, # 청크간 전후 문맥 파악을 위해 겹쳐지는 수
        length_function=my_tokenizer, # 토큰의 길이를 뭘로 정해?
    )
    # 데이터 끊어주기
    chunks = text_spliter.split_text(text)
    # print(f'chinks = {chunks}')
    # chromadb 에 입력
    """
    ids = []
    for i in range(len(chunks)):
        ids.append(f"idx_{i}")
    """
    ids = [f"idx_{i}" for i in range(len(chunks))]
    coll.upsert(documents=chunks,ids=ids)
    print(f'저장 완료 {len(chunks)}개 문맥 확보')
    print(coll.get())

# insert_data('data/운수좋은날.pdf')

def search_data(query:str) -> None:
    print(f'질문내용 : {query}')
    results = coll.query(
        query_texts=[query],
        n_results=5,
    )
    # print(results) # chroma db 에서 가져온 내용
    # 가져온 리스트 안의 내용을 줄바꿈 두번으로 붙여서 하나의 텍스트로 만든다.
    context = "\n\n".join(results['documents'][0])

    # llm 에 전달할 프롬프트 작성
    prompt = f"""
    당신은 소설 분석 전문가 입니다. 제공된 [소설 본문 발췌]를 바탕으로 사용자의 [질문]에 답하세요.
    본문에 근거하여 인물의 심리, 사건의 배경, 복선 등을 상세히 분석해 주세요.
    
    [소설 본문 발췌]
    {context}

    [질문]
    {query}
    """

    resp = ollama.generate(
        model="gemma4:e2b", 
        prompt=prompt, 
        stream=True, 
        options={
            "num_predict":-1,   # 출력토큰 수(무제한)
            "num_ctx":8192      # 입력+출력 합친 컨텍스트 크기
        }
    )
    for chunk in resp:
        print(chunk['response'],end="",flush=True)

        if chunk.get('done'):
            print("\n")
            print(f"중지이유 : {chunk.get('done_reason')}")

question = input('소설 운수 좋은 날에 대한 질문을 해주세요\n')
# 이 소설의 주인공은 누구야?
# 이 소설의 줄거리에 대해서 요약해줘
search_data(question)