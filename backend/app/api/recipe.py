from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.recipe import RecipeRequest, RecipeListResponse, RecipePriceResponse, IngredientHistory
from app import crud
from app import models
from app.services import spoonacular, naver_shop, ai_advisor, translator, recommendation

router = APIRouter(prefix="/recipes", tags=["Recipes"])

# 1. 레시피 검색 (지재헌님 스타일: 리스트부터 한글화 적용)
@router.get("/search", response_model=List[RecipeListResponse])
async def search_recipes(
    mode: str = Query("요리 초보", description="요리 초보, 설거지 최소화, 전자레인지 전용, 10분 완성"),
    budget: int = Query(10000, description="사용자 예산"),
    db: Session = Depends(get_db)
):
    try:
        # 친구가 만든 API 호출 (비동기)
        results = await spoonacular.search_recipes_from_api(
            cuisine="Korean", 
            ingredients="", 
            difficulty_tags=[mode]
        )
        
        if not results:
            return []

        # [지재헌님 로직 추가] 리스트 결과물들을 한글로 미리 가공하기
        processed_results = []
        for res in results:
            processed_results.append({
                "id": res["id"],
                "title": translator.translate_to_ko(res["title"]), # 제목 한글화!
                "image": res.get("image"),
                "readyInMinutes": res.get("readyInMinutes", 0),
                "pricePerServing": res.get("pricePerServing", 0) # API 가격은 참고용
            })
            
        return processed_results

    except Exception as e:
        print(f"❌ 검색 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="서버 내부 오류가 발생했습니다.")

# 2. 요리 상세 정보 및 쇼핑 목록 API (지재헌님 DB 로직 핵심)
@router.get("/{recipe_id}/details")
async def get_recipe_details(recipe_id: int, budget: int = 10000, db: Session = Depends(get_db)):
    detail = await spoonacular.get_recipe_detail_from_api(recipe_id)
    if not detail:
        raise HTTPException(status_code=404, detail="레시피 상세 정보를 찾을 수 없습니다.")

    title_ko = translator.translate_to_ko(detail["title"])
    
    # [지재헌님 로직] 부모 테이블(Recipe) 데이터 확인 및 생성
    db_recipe = db.query(models.Recipe).filter(models.Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        new_recipe = models.Recipe(recipe_id=recipe_id, title=title_ko)
        db.add(new_recipe)
        db.commit()

    # 조리법 정리 및 번역
    raw_inst = detail.get("instructions") or "조리 정보가 없습니다."
    clean_inst = raw_inst.replace("<ol>", "").replace("<li>", "- ").replace("</li>", "\n").replace("</ol>", "")
    instructions_ko = translator.translate_to_ko(clean_inst)
    
    # 재료 번역 및 요약
    ingredients_raw = detail.get("extendedIngredients", [])
    ko_ingredients = [translator.translate_to_ko(item["name"]) for item in ingredients_raw]
    summary_ingredients = ", ".join(ko_ingredients[:5])

    # 네이버 최저가 및 AI 조언 (재헌님의 하이라이트 로직)
    shopping_data = await naver_shop.get_total_shopping_list(ko_ingredients)
    total_price = shopping_data["total_price"]
    real_ai_advice = ai_advisor.get_ai_advice(summary_ingredients, str(total_price), budget)

    # [지재헌님 로직] DB에 최종 결과물 저장
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

# 3. 검색 기록 조회 (History 로직 유지)
@router.get("/history", response_model=List[IngredientHistory])
def get_search_history(db: Session = Depends(get_db)):
    return crud.get_search_history(db)