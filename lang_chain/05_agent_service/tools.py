from datetime import datetime

from langchain_core.tools import tool

@tool
def check_weather(location:str) -> str:
    """특정 지역의 현재(오늘) 날씨를 확인하는 도구입니다."""
    print(f"{location} 지역 날씨 데이터 크롤링")
    return f"요청하신 {location} 지역은 현재 맑습니다."

@tool
def now_date() -> str:
    """현재(오늘) 날짜와 시간을 확인해주는 도구 입니다."""
    curr_datetime = datetime.now()
    fmt_datetime = curr_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(f'현재 날짜와 시간 : {fmt_datetime}')
    return fmt_datetime

@tool
def check_stock() -> str:
    """현재(오늘) 주식시장의 현황을 알려주는 도구 입니다."""
    print("주요 뉴스사이트에서 주식 정보 크롤링")
    return "오늘의 주식시장은 나쁘지 않습니다."