from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import RecipePriceResponse, IngredientHistory, RecipeListResponse
from app import crud
from app import models
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
    results = spoonacular.search_recipes(query=query, budget=budget)
    
    # 예산 부족 예외 처리 (화면 1-4-1 대응)
    if not results:
        raise HTTPException(status_code=400, detail="금액에 맞는 요리를 찾을 수 없습니다.")
        
    return results

# 2. 상세 물가 및 AI 조언 (여기서 부모 데이터를 먼저 챙깁니다)
@router.get("/{recipe_id}/price", response_model=RecipePriceResponse)
def get_recipe_price(recipe_id: int, budget: int = 10000, db: Session = Depends(get_db)):
    # Spoonacular API에서 정보 수집
    title, ko_name = spoonacular.get_recipe_info(recipe_id)
    
    if title in ["설정 오류", "API 오류"]:
        return {"recipe_title": title, "ingredient": ko_name, "lowest_price": "0", "ai_advice": "점검 중"}

    # [핵심] 부모 데이터(Recipe)가 DB에 있는지 확인 후, 없으면 먼저 저장
    # 이 작업이 선행되어야 ForeignKeyViolation 에러가 나지 않습니다.
    db_recipe = db.query(models.Recipe).filter(models.Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        new_recipe = models.Recipe(recipe_id=recipe_id, title=title)
        db.add(new_recipe)
        db.commit() # 부모를 먼저 DB에 확정(Commit) 시킴

    # 최저가 및 AI 조언 생성
    price_str = naver_shop.get_lowest_price(ko_name)
    real_ai_advice = ai_advisor.get_ai_advice(ko_name, price_str, budget)
    
    # 자식 데이터(Ingredient) 저장 (이제 부모가 확실히 존재하므로 안전합니다)
    crud.update_or_create_ingredient(
        db, 
        recipe_id=recipe_id, 
        title=title, 
        name=ko_name, 
        price=price_str, 
        advice=real_ai_advice
    )
    
    return {
        "recipe_title": title, "ingredient": ko_name, 
        "lowest_price": price_str, "ai_advice": real_ai_advice
    }

# 3. 검색 기록
@router.get("/history", response_model=List[IngredientHistory])
def get_search_history(db: Session = Depends(get_db)):
    return crud.get_search_history(db)