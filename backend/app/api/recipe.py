from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.recipe import RecipeRequest, RecipeListResponse, RecipePriceResponse, IngredientHistory
from app import crud
from app.services import recommendation, spoonacular, naver_shop, translator

router = APIRouter(prefix="/recipes", tags=["Recipes"])

# 1. 요리 추천 API
@router.post("/recommend", response_model=List[RecipeListResponse])
async def recommend_recipes(request: RecipeRequest, db: Session = Depends(get_db)):
    results = await recommendation.get_recipe_recommendations(request)
    return results

# 2. 요리 상세 정보 및 쇼핑 목록 API (화면 1-6 ~ 1-7 대응)
@router.get("/{recipe_id}/details")
async def get_recipe_details(recipe_id: int, db: Session = Depends(get_db)):
    detail = await spoonacular.get_recipe_detail_from_api(recipe_id)
    if not detail:
        raise HTTPException(status_code=404, detail="레시피 상세 정보를 찾을 수 없습니다.")

    # [번역] 1. 제목 및 조리법 한글화
    title_ko = translator.translate_to_ko(detail["title"])
    
    # HTML 태그 제거 후 번역 (자취생이 보기 편하게 정리)
    raw_inst = detail.get("instructions", "조리 방법 정보가 없습니다.")
    clean_inst = raw_inst.replace("<ol>", "").replace("<li>", "- ").replace("</li>", "\n").replace("</ol>", "")
    instructions_ko = translator.translate_to_ko(clean_inst)
    
    # [번역] 2. 재료 리스트 한글화
    ingredients_raw = detail.get("extendedIngredients", [])
    ko_ingredients = [translator.translate_to_ko(item["name"]) for item in ingredients_raw]
    summary = ", ".join(ko_ingredients[:5])

    # 3. 네이버 쇼핑 데이터 (번역된 재료로 검색)
    shopping_data = await naver_shop.get_total_shopping_list(ko_ingredients)
    total_price = shopping_data["total_price"]

    # 4. 검색 기록 저장 (DB)
    crud.update_or_create_ingredient(
        db, 
        title=title_ko, 
        name=summary, 
        price=str(total_price), 
        advice="최저가 구성이 완료되었습니다!"
    )

    # 5. 최종 응답 구조 (화면 설계서 1-6, 1-7 분리 대응)
    return {
        "recipe_info": {  # 화면 1-6: 레시피 상세용
            "title": title_ko,
            "instructions": instructions_ko,
            "image": detail.get("image"),
            "ingredients": ko_ingredients
        },
        "shopping_info": { # 화면 1-7: 최저가 쇼핑용
            "total_price": total_price,
            "shopping_list": shopping_data["items"]
        }
    }

# 3. 검색 기록 조회
@router.get("/history", response_model=List[IngredientHistory])
def get_search_history(db: Session = Depends(get_db)):
    return crud.get_search_history(db)