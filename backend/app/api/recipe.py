from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import RecipePriceResponse
from app import crud
from app.services.spoonacular import get_recipe_info
from app.services.naver_shop import get_lowest_price

router = APIRouter()

@router.get("/recipe/{recipe_id}/price", response_model=RecipePriceResponse)
def get_recipe_price(recipe_id: int, db: Session = Depends(get_db)):
    
    # 1. 실제 API 호출 (이제 여기서 실시간으로 키를 읽어옵니다)
    title, ko_name = get_recipe_info(recipe_id)
    
    # 만약 제목이 "설정 오류"라면 더 이상 진행하지 않고 바로 반환 (디버깅용)
    if title in ["설정 오류", "API 오류", "시스템 에러"]:
        return {
            "recipe_title": title,
            "ingredient": ko_name,
            "lowest_price": "0",
            "ai_advice": "서버 설정 확인이 필요합니다."
        }

    # 2. 정상일 경우 네이버 검색 및 DB 저장
    price_str = get_lowest_price(ko_name)
    crud.update_or_create_ingredient(db, name=ko_name, price=price_str)
    
    return {
        "recipe_title": title,
        "ingredient": ko_name,
        "lowest_price": price_str,
        "ai_advice": f"'{ko_name}'의 실시간 물가 분석이 완료되었습니다."
    }