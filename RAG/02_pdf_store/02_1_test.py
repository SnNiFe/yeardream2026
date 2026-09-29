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
    name="lecture",
    embedding_function=ollama_ef
)

# 3. 토크나이징 - 기본 길이로만 처리할 예정

# 4. 데이터 저장
def insert_data(path:str) -> None:
    lecture = path.split('/')[1].rsplit('.',1)[0].lower()
    # print(lecture)
    
    # 4-1. 특정 PDF 를 불러와 읽는다.
    reader = PdfReader(path)
    text = ''
    for i, page in enumerate(reader.pages): # PDF 페이지들을 한장씩 꺼내서
        text += page.extract_text() # 텍스트를 추출 후 text 변수에 누적시킨다.
        # print(f'{i} PAGE')
        # print(text)

    # 9페이지짜리 문자를 통으로 넣을 수 없기에 잘라줘야한다.(chunking 작업)
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=400, # 최대 청크 크기
        chunk_overlap=25, # 청크간 전후 문맥 파악을 위해 겹쳐지는 수
        length_function=len, # 토큰의 길이를 뭘로 정해?
    )
    # 데이터 끊어주기
    chunks = text_spliter.split_text(text)
    print(f'{lecture} chunks = {len(chunks)}')
    
    # chromadb 에 입력
    ids = [f"idx_{i}" for i in range(len(chunks))]
    metas = [{"subject":lecture} for i in range(len(chunks))]

    batch_size = 5 # 배치 사이즈 만큼 잘라서 저장
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i : i + batch_size]
        batch_ids = ids[i : i + batch_size]
        batch_metas = metas[i : i + batch_size]
        coll.upsert(documents=batch_chunks, ids=batch_ids, metadatas=batch_metas)
        print(f"진행 중: {min(i + batch_size, len(chunks))} / {len(chunks)} 완료")

    print(f'저장 완료 {len(chunks)}개 문맥 확보')
    print(coll.get(where={'subject':lecture}))

# insert_data('data/pandas.pdf')
# insert_data('data/scikit_learn.pdf')
# insert_data('data/FASTAPI.pdf')

def search_data(subject:str, query:str) -> None:
    print(f'과목 : {subject} / 질문내용 : {query}')
    results = coll.query(
        query_texts=[query],
        n_results=5,
        where={'subject':{'$eq':subject}}
    )
    # print(results) # chroma db 에서 가져온 내용
    # 가져온 리스트 안의 내용을 줄바꿈 두번으로 붙여서 하나의 텍스트로 만든다.
    context = "\n\n".join(results['documents'][0])

    # llm 에 전달할 프롬프트 작성
    prompt = f"""
    당신은 python 을 이용한 머신러닝 선생님 입니다. 제공된 [학습교재]를 바탕으로 사용자의 [질문]에 답하세요.
    [학습교제] 내용에 근거하여 질문한 기술의 개요, 특징 등에 대해서 알기쉽게 설명해 주세요.
    
    [학습교제]
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

subject = input('물어보고 싶은 과목(fastapi, scikit-learn, pands)\n')
q = input('질문내용\n')
search_data(subject,q)