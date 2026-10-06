import chromadb
from llama_index.core import ChatPromptTemplate, PromptTemplate, Settings, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

# 1. 모델등록
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest")
Settings.llm = Ollama(model="gemma4:e2b", request_timeout=300)

# 2. cheomadb 와 llama-index 연동
client = chromadb.PersistentClient(path="store")
coll = client.get_collection("my_collection")
store = ChromaVectorStore(chroma_collection=coll)

# 3. chromadb 의 collection 불러오기
index = VectorStoreIndex.from_vector_store(store)

def query_engine(question:str):
    qa_template = ChatPromptTemplate.from_messages([
        ("system","당신은 소설 분석 전문가 입니다. 제공된 [소설 본문 발췌]를 근거로 사용자의 [질문]에 대답해 주세요."),
        ("user","[소설 본문 발췌]\n{context_str}\n\n[질문]\n{query_str}")
    ])

    engine = index.as_query_engine(similarity_top_k=5,text_qa_template=qa_template,streaming=True)
    resp = engine.query(question)
    for chunk in resp.response_gen:
        print(chunk,end="",flush=True)

# question = input("운수 좋은날에 대한 질문을 해주세요.\n")
# query_engine(question)

engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    similarity_top_k=5,
    system_prompt="당신은 소설 분석 전문가 입니다. 제공된 [소설 본문 발췌]를 근거로 사용자의 [질문]에 대답해 주세요.",
    context_prompt=PromptTemplate("[소설 본문 발췌]\n{context_str}\n\n[질문]\n{query_str}")
)

def chat_engine(question):
    # resp = engine.chat(question) # 실시간 X
    resp = engine.stream_chat(question)
    for chunk in resp.response_gen:
        print(chunk,end="",flush=True)

while True:
    question = input("운수 좋은날에 대한 질문을 해주세요.(exit는 종료)\n")
    if question == 'exit':
        break
    else:
        chat_engine(question)
        print("")