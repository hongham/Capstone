from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import RecipePriceResponse
from app import crud
from app.services.spoonacular import get_recipe_info
from app.services.naver_shop import get_lowest_price
from app.services.ai_advisor import get_ai_advice

router = APIRouter()

@router.get("/recipe/{recipe_id}/price", response_model=RecipePriceResponse)
def get_recipe_price(recipe_id: int, db: Session = Depends(get_db)):
    
    # 1. 레시피 및 재료 정보 가져오기
    title, ko_name = get_recipe_info(recipe_id)
    
    # 오류 발생 시 즉시 반환
    if title in ["설정 오류", "API 오류", "시스템 에러"]:
        return {
            "recipe_title": title,
            "ingredient": ko_name,
            "lowest_price": "0",
            "ai_advice": "서버 설정을 확인해주세요."
        }

    # 2. 네이버 최저가 검색
    price_str = get_lowest_price(ko_name)
    
    # 3. HAI-GPT 실시간 조언 생성 (Claude 3.5)
    real_ai_advice = get_ai_advice(ko_name, price_str)
    
    # 4. DB에 결과 저장 (최신 물가 업데이트)
    crud.update_or_create_ingredient(db, name=ko_name, price=price_str)
    
    # 5. 최종 데이터 반환 
    return {
        "recipe_title": title,
        "ingredient": ko_name,
        "lowest_price": price_str,
        "ai_advice": real_ai_advice
    }