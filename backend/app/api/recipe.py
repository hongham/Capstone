from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import RecipePriceResponse, IngredientHistory, RecipeListResponse
from app import crud
from app.services import spoonacular, naver_shop, ai_advisor

router = APIRouter()

# 1. 레시피 검색 (모드 & 예산 반영)
@router.get("/search", response_model=List[RecipeListResponse])
def search_recipes(
    mode: str = Query("요리 초보", description="요리 초보, 설거지 최소화, 전자레인지 전용, 10분 완성"),
    budget: int = Query(10000, description="사용자 예산"),
    db: Session = Depends(get_db)
):
    mode_queries = {
        "요리 초보": "easy",
        "설거지 최소화": "one pot",
        "전자레인지 전용": "microwave",
        "10분 완성": "quick"
    }
    query = mode_queries.get(mode, "healthy")
    return spoonacular.search_recipes(query=query, budget=budget)

# 2. 상세 물가 및 AI 조언
@router.get("/{recipe_id}/price", response_model=RecipePriceResponse)
def get_recipe_price(recipe_id: int, budget: int = 10000, db: Session = Depends(get_db)):
    title, ko_name = spoonacular.get_recipe_info(recipe_id)
    if title in ["설정 오류", "API 오류"]:
        return {"recipe_title": title, "ingredient": ko_name, "lowest_price": "0", "ai_advice": "점검중"}

    price_str = naver_shop.get_lowest_price(ko_name)
    real_ai_advice = ai_advisor.get_ai_advice(ko_name, price_str, budget)
    
    crud.update_or_create_ingredient(db, title=title, name=ko_name, price=price_str, advice=real_ai_advice)
    
    return {
        "recipe_title": title, "ingredient": ko_name, 
        "lowest_price": price_str, "ai_advice": real_ai_advice
    }

# 3. 검색 기록
@router.get("/history", response_model=List[IngredientHistory])
def get_search_history(db: Session = Depends(get_db)):
    return crud.get_search_history(db)