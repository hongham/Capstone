from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db  # [유지] DB 연결 도구
from app.schemas import RecipePriceResponse  # [유지] 응답 규격
from app import crud  # [추가] DB 저장 로직 모음

router = APIRouter()

# 1. response_model 규격은 그대로 유지합니다.
@router.get("/recipe/{recipe_id}/price", response_model=RecipePriceResponse)
def get_recipe_price(recipe_id: int, db: Session = Depends(get_db)):
    
    # 2. [기존 가짜 데이터] 키가 오면 실제 서비스 호출로 바꿀 데이터들입니다.
    recipe_title = "테스트용 파스타 (구조 연결 및 DB 저장 성공!)"
    ingredient_name = "파스타면"
    price_str = "2,500"
    
    # 3. [핵심 추가] Ingredient 테이블에 실시간 가격 정보를 기록합니다.
    # 이 코드가 실행되면 DB의 ingredients 테이블에 데이터가 쌓입니다.
    crud.update_or_create_ingredient(db, name=ingredient_name, price=price_str)
    
    # 4. [기존 반환 구조] 규격에 맞춰 데이터를 내보냅니다.
    return {
        "recipe_title": recipe_title,
        "ingredient": ingredient_name,
        "lowest_price": price_str,
        "ai_advice": "검색 결과가 성공적으로 출력되고 DB에도 기록되었습니다!"
    }