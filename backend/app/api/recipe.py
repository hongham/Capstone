from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.recipe import RecipeRequest, RecipeListResponse, RecipePriceResponse, IngredientHistory
from app import crud, models
from app.services import recommendation, spoonacular, naver_shop, translator, ai_advisor

router = APIRouter(prefix="/recipes", tags=["Recipes"])

# 1. 요리 추천 API (화면 1-4 ~ 1-5 대응)
@router.post("/recommend", response_model=List[RecipeListResponse])
async def recommend_recipes(request: RecipeRequest, db: Session = Depends(get_db)):
    """
    사용자의 요리 종류, 예산, 난이도 등을 받아 최적의 레시피 4개를 추천합니다.
    """
    results = await recommendation.get_recipe_recommendations(request)
    return results

# 2. 요리 상세 정보 및 쇼핑 목록 API (화면 1-6 ~ 1-7 대응)
@router.get("/{recipe_id}/details")
async def get_recipe_details(recipe_id: int, budget: int = 10000, db: Session = Depends(get_db)):
    """
    상세 레시피(한글), 쇼핑 최저가 리스트, AI 구매 조언을 반환합니다.
    """
    # 외부 API에서 레시피 상세 정보 가져오기
    detail = await spoonacular.get_recipe_detail_from_api(recipe_id)
    if not detail:
        raise HTTPException(status_code=404, detail="레시피 상세 정보를 찾을 수 없습니다.")

    # [번역] 1. 제목 및 조리법 한글화
    title_ko = translator.translate_to_ko(detail["title"])
    
    # 조리법 HTML 태그 제거 및 방어 코드 (None 처리)
    raw_inst = detail.get("instructions")
    if raw_inst:
        clean_inst = raw_inst.replace("<ol>", "").replace("<li>", "- ").replace("</li>", "\n").replace("</ol>", "")
    else:
        clean_inst = "상세 조리 방법 정보가 없습니다."
    
    instructions_ko = translator.translate_to_ko(clean_inst)
    
    # [번역] 2. 재료 리스트 한글화
    ingredients_raw = detail.get("extendedIngredients", [])
    ko_ingredients = [translator.translate_to_ko(item["name"]) for item in ingredients_raw]
    summary = ", ".join(ko_ingredients[:5])

    # 3. 네이버 쇼핑 데이터 수집 (실시간 최저가)
    shopping_data = await naver_shop.get_total_shopping_list(ko_ingredients)
    total_price = shopping_data["total_price"]

    # 4. DB 저장 로직 (models.py의 'id' 컬럼 규격에 맞춤)
    # [수정 포인트] models.Recipe.recipe_id -> models.Recipe.id
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    
    if not db_recipe:
        # models.py 구조에 맞춰 신규 레시피 생성
        new_recipe = models.Recipe(
            id=recipe_id, 
            title=title_ko,
            cooking_time=detail.get("readyInMinutes", 0),
            total_cost=int(total_price),
            mode_tag="일반"
        )
        db.add(new_recipe)
        db.commit()

    # 5. AI 조언 생성 (ai_advisor 서비스 호출)
    main_ingredient = ko_ingredients[0] if ko_ingredients else "식재료"
    real_ai_advice = ai_advisor.get_ai_advice(main_ingredient, f"{total_price}원", budget)

    # 6. 검색 기록 저장 (수정된 crud.py 규격에 맞춤)
    crud.update_or_create_ingredient(
        db, 
        title=title_ko, 
        name=summary, 
        price=str(total_price), 
        advice=real_ai_advice
    )

    # 7. 최종 응답 구조 (프론트엔드 연결용)
    return {
        "recipe_info": {  # 화면 1-6: 레시피 상세
            "title": title_ko,
            "instructions": instructions_ko,
            "image": detail.get("image"),
            "ingredients": ko_ingredients
        },
        "shopping_info": { # 화면 1-7: 최저가 쇼핑 리스트
            "total_price": total_price,
            "shopping_list": shopping_data["items"],
            "ai_advice": real_ai_advice
        }
    }

# 3. 검색 기록 조회 (화면 2-1 대응)
@router.get("/history", response_model=List[IngredientHistory])
def get_search_history(db: Session = Depends(get_db)):
    # 수정된 crud.py의 함수명 반영
    return crud.get_ingredient_history(db)