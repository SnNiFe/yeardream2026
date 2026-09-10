from pydantic import BaseModel, Field

class ReviewAnalysis(BaseModel):
    sentiment:str = Field(description="긍정,부정,중립 중 하나")
    score:int = Field(description="1점부터 5점 까지의 만족도 점수, 절대 1보다 작지 않고 5보다 크지 않은 정수여야함")
    summary:str = Field(description="리뷰 핵심 내용을 한줄 요약")