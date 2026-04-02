from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import RecipePriceResponse, IngredientHistory
from app import crud
from app.services.spoonacular import get_recipe_info
from app.services.naver_shop import get_lowest_price
from app.services.ai_advisor import get_ai_advice

router = APIRouter()

@router.get("/recipe/{recipe_id}/price", response_model=RecipePriceResponse)
def get_recipe_price(recipe_id: int, db: Session = Depends(get_db)):
    # 1. 정보 수집 (Spoonacular)
    title, ko_name = get_recipe_info(recipe_id)
    
    if title in ["설정 오류", "API 오류"]:
        return {"recipe_title": title, "ingredient": ko_name, "lowest_price": "0", "ai_advice": "점검중"}

    # 2. 가격 조회 (Naver)
    price_str = get_lowest_price(ko_name)
    
    # 3. AI 조언 생성 (HAI-GPT)
    real_ai_advice = get_ai_advice(ko_name, price_str)
    
    # 4. [핵심] DB에 모든 정보 기록 (정합성 맞춤)
    crud.update_or_create_ingredient(
        db, 
        title=title, 
        name=ko_name, 
        price=price_str, 
        advice=real_ai_advice
    )
    
    return {
        "recipe_title": title,
        "ingredient": ko_name,
        "lowest_price": price_str,
        "ai_advice": real_ai_advice
    }

@router.get("/history", response_model=List[IngredientHistory])
def get_search_history(db: Session = Depends(get_db)):
    return crud.get_ingredient_history(db)