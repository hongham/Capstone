from sqlalchemy.orm import Session
from . import models

# [최종 수정] recipe_id 인자를 추가하여 recipe.py와의 호출 규격을 맞췄습니다.
def update_or_create_ingredient(db: Session, recipe_id: int, title: str, name: str, price: str, advice: str):
    # 가격 문자열 "2,500원"에서 특수문자 제거 후 숫자로 변환
    try:
        clean_price = str(price).replace(",", "").replace("원", "").strip()
        numeric_price = float(clean_price)
    except:
        numeric_price = 0.0
    
    # 1. 이미 저장된 동일한 이름의 재료가 있는지 확인
    db_item = db.query(models.Ingredient).filter(models.Ingredient.name == name).first()
    
    if db_item:
        # 2. 있다면 정보 업데이트
        # models.py 구조에 맞춰 recipe_id를 기록합니다.
        db_item.recipe_id = recipe_id 
        db_item.current_price = numeric_price
        db_item.ai_advice = advice
    else:
        # 3. 없다면 새로 생성
        db_item = models.Ingredient(
            recipe_id=recipe_id,
            name=name,
            current_price=numeric_price,
            ai_advice=advice,
            unit="개/g"
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_item)
    return db_item

# 화면 2-1 레시피함(최근 기록) 조회를 위한 함수
def get_search_history(db: Session, limit: int = 10):
    return db.query(models.Ingredient).order_by(models.Ingredient.id.desc()).limit(limit).all()