from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 사용자가 입력한 검색 조건을 담는 스키마 (화면 1-1 ~ 1-5 대응)
class RecipeRequest(BaseModel):
    cuisine: str              # 화면 1-1: 요리 종류 (한식, 양식, 중식 등)
    budget: int               # 화면 1-2: 예산 입력
    difficulty: List[str]     # 화면 1-3: 난이도/태그 (설거지 최소화, 10분 완성 등)
    include_ingredients: str  # 화면 1-4: 넣고 싶은 재료 추가 (쉼표로 구분된 문자열)

class RecipeListResponse(BaseModel):
    id: int
    title: str
    image: str
    readyInMinutes: int
    pricePerServing: Optional[float] = None # 예산 필터링을 위해 추가

    class Config:
        from_attributes = True

# 기존 코드 유지
class RecipePriceResponse(BaseModel):
    recipe_title: str
    ingredient: str
    lowest_price: str
    ai_advice: str

class IngredientHistory(BaseModel):
    recipe_title: Optional[str] = None
    name: str
    current_price: float
    ai_advice: Optional[str] = None
    updated_at: datetime

    class Config:
        from_attributes = True