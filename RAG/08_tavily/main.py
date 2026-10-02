"""
LLM 활용하는 정보
1. 자체 모델 - 모델이 학습한 내용들(ollama - gemma4)
2. RAG - 저장소에서 담고있는 고유의 지식(chromadb)
3. 인터넷 검색 - 최신정보, 실시간 정보(tavily)
tavily search API - AI 에이젼트 및 LLM 을 위해 최적화된 AI 전용 검색엔진 서비스 API
"""
import os

from dotenv import load_dotenv
from langchain_tavily import TavilyExtract, TavilySearch

load_dotenv() # .env 불러오기

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

def basic_search(query:str):
    ## search_depth
    # basic     : 빠르고 저렴한 검색(1credit +a), 결과마다 간단한 content 제공
    # advance   : basic * 2 배 검색, 문맥적 의미까지 분석해 깊게 탐색(예: 광고 문구 제거)
    ### topic
    # general(기본) : 일반 웹 검색. 뉴스, 일반지식, 블로그, 위키피디아 등 웹 전반의 통합검색 
    # news      : 최신 뉴스/기사 전용 검색
    # finance   : 금융/경제/주식 전용 검색
    search = TavilySearch(max_results=3, search_depth='basic', topic='general')
    result = search.invoke({'query':query})
    # print(result['result'])
    for r in result['results']:
        print(f"TITLE : {r['title']}")
        print(f"URL : {r['url']}")
        print(f"SUMMARY : {r['content'][:450]}...")

# basic_search('2026년 langchain 최신버전 주요 변경사항')


def detail_content(query:str):
    search = TavilySearch(max_results=1, search_depth='basic', topic='general')
    result = search.invoke({'query':query})
    ### extract_depth
    # basic     : 표준적인 본문 텍스트 추출
    # advance   : 표,구조,동적요소 등 정밀한 추출
    extract = TavilyExtract(extract_depth='basic')
    i = 0 # 혹시 몰라서 임의로 정함
    for r in result['results']:
        print(f"TITLE : {r['title']}")
        url = r['url']
        print(f"URL : {url}")
        content = extract.invoke({'urls':[url]})
        print(content['results'][i].keys())
        print(content['results'][i]['raw_content'])
        i += 1 # 혹시 몰라서 임의로 정함
# detail_content('tavily 활용법')


def advance_search(query:str):
    # include_answer = "advanced"       : Tavily 에서 검색결과로 만든 요약답변 포함
    # include_raw_content = "markdown"  : 페이지 본문 전체 포함(markdown)
    # time_range = "year"               : 기간(day,month,year)
    # exclude_domains = ["youtube.com"] : 특정 도메인 제회(include_domains=[]를 이용해 필수포함)
    search = TavilySearch(
        max_results=3,
        topic="general",
        search_depth="advanced",
        include_answer="advanced",
        include_raw_content="markdown",
        time_range="year",
        exclude_domains=["youtube.com"]
    )
    result = search.invoke({'query':query})
    for r in result['results']:
        print(f"keys : {r.keys()}")
        print(f"TITLE : {r['title']}")
        print(f"CONTENT : {r['content']}")
        print('==='*120)
        print(f"RAW : {r['raw_content']}")
        break

advance_search('RAG 시스템에서 검색 품질을 높이는 최신 기법')