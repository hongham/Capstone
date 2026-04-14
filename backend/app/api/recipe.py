from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.recipe import RecipeRequest, RecipeListResponse, RecipePriceResponse, IngredientHistory
from app import crud
from app import models
from app.services import spoonacular, naver_shop, ai_advisor, translator, recommendation

router = APIRouter(prefix="/recipes", tags=["Recipes"])

# 1. 레시피 검색 (모드 & 예산 반영) - 지재헌님 로직 유지
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
    
    if not results:
        raise HTTPException(status_code=400, detail="금액에 맞는 요리를 찾을 수 없습니다.")
        
    return results

# 2. 요리 상세 정보 및 쇼핑 목록 API (지재헌님 DB 로직 + 친구 번역 로직 통합)
@router.get("/{recipe_id}/details")
async def get_recipe_details(recipe_id: int, budget: int = 10000, db: Session = Depends(get_db)):
    # Spoonacular API에서 정보 수집
    detail = await spoonacular.get_recipe_detail_from_api(recipe_id)
    if not detail:
        raise HTTPException(status_code=404, detail="레시피 상세 정보를 찾을 수 없습니다.")

    # [번역] 친구가 만든 번역 기능 활용
    title_ko = translator.translate_to_ko(detail["title"])
    
    # [핵심] 지재헌님의 DB 무결성 로직 (부모 레시피 먼저 저장)
    db_recipe = db.query(models.Recipe).filter(models.Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        new_recipe = models.Recipe(recipe_id=recipe_id, title=title_ko)
        db.add(new_recipe)
        db.commit()

    # 조리법 정리 및 번역
    raw_inst = detail.get("instructions", "조리 방법 정보가 없습니다.")
    clean_inst = raw_inst.replace("<ol>", "").replace("<li>", "- ").replace("</li>", "\n").replace("</ol>", "")
    instructions_ko = translator.translate_to_ko(clean_inst)
    
    # 재료 리스트 번역
    ingredients_raw = detail.get("extendedIngredients", [])
    ko_ingredients = [translator.translate_to_ko(item["name"]) for item in ingredients_raw]
    summary_ingredients = ", ".join(ko_ingredients[:5])

    # 네이버 쇼핑 및 AI 조언 (두 사람의 로직 결합)
    shopping_data = await naver_shop.get_total_shopping_list(ko_ingredients)
    total_price = shopping_data["total_price"]
    real_ai_advice = ai_advisor.get_ai_advice(summary_ingredients, str(total_price), budget)

    # [DB 저장] 지재헌님의 최신화 로직
    crud.update_or_create_ingredient(
        db, 
        recipe_id=recipe_id, 
        title=title_ko, 
        name=summary_ingredients, 
        price=str(total_price), 
        advice=real_ai_advice
    )

    return {
        "recipe_info": {
            "title": title_ko,
            "instructions": instructions_ko,
            "image": detail.get("image"),
            "ingredients": ko_ingredients
        },
        "shopping_info": {
            "total_price": total_price,
            "shopping_list": shopping_data["items"],
            "ai_advice": real_ai_advice
        }
    }

# 3. 검색 기록 조회
@router.get("/history", response_model=List[IngredientHistory])
def get_search_history(db: Session = Depends(get_db)):
    return crud.get_search_history(db)