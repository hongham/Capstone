from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import RecipePriceResponse, IngredientHistory, RecipeListResponse
from app import crud
from app.services import spoonacular, naver_shop, ai_advisor

router = APIRouter()

# 1. 레시피 검색 (기존 유지)
@router.get("/search", response_model=List[RecipeListResponse])
def search_recipes(
    mode: str = Query("요리 초보", description="요리 초보, 설거지 최소화, 전자레인지 전용, 10분 완성"),
    budget: int = Query(10000, description="사용자 예산"),
    db: Session = Depends(get_db)
):
    mode_queries = {"요리 초보": "easy", "설거지 최소화": "one pot", "전자레인지 전용": "microwave", "10분 완성": "quick"}
    query = mode_queries.get(mode, "healthy")
    return spoonacular.search_recipes(query=query, budget=budget)

# 2. [수정] 상세 물가 및 AI 조언 (다중 재료 대응)
@router.get("/{recipe_id}/price", response_model=RecipePriceResponse)
def get_recipe_price(recipe_id: int, budget: int = 10000, db: Session = Depends(get_db)):
    # 1. 스푼애큘러에서 재료 '리스트' 가져오기
    title, ko_ingredients = spoonacular.get_recipe_info(recipe_id)
    
    if title in ["API 오류", "시스템 에러"]:
        return {"recipe_title": title, "ingredient": "정보 없음", "lowest_price": "0", "ai_advice": "점검중"}

    # 2. [핵심] 네이버 쇼핑에서 여러 재료의 총 합산 가격 가져오기
    # (naver_shop.py에 get_total_ingredients_price 함수를 이미 만드셨다고 가정!)
    total_price, summary = naver_shop.get_total_ingredients_price(ko_ingredients)
    
    # 3. AI 조언 생성 (요약된 재료 문자열과 총 가격 전달)
    real_ai_advice = ai_advisor.get_ai_advice(summary, str(total_price), budget)
    
    # 4. DB 저장
    crud.update_or_create_ingredient(db, title=title, name=summary, price=str(total_price), advice=real_ai_advice)
    
    return {
        "recipe_title": title, 
        "ingredient": summary, # 예: "마늘, 양파, 돼지고기..."
        "lowest_price": str(total_price), 
        "ai_advice": real_ai_advice
    }

# 3. 검색 기록 (기존 유지)
@router.get("/history", response_model=List[IngredientHistory])
def get_search_history(db: Session = Depends(get_db)):
    return crud.get_search_history(db)