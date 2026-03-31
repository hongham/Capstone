from pydantic import BaseModel
from typing import Optional

# 1. 요청(Request) 규격: 사용자가 보낼 데이터
class RecipeRequest(BaseModel):
    recipe_id: int

# 2. 응답(Response) 규격: 서버가 돌려줄 데이터 (중요!)
class RecipePriceResponse(BaseModel):
    recipe_title: str       # 요리 제목
    ingredient: str         # 번역된 재료명
    lowest_price: str       # 최저가 (문자열로 통일)
    ai_advice: Optional[str] = "AI 조언을 준비 중입니다." # 나중에 제미나이가 채울 자리

    class Config:
        from_attributes = True # DB 객체를 자동으로 변환해주기 위한 설정