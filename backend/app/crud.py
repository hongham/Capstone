from sqlalchemy.orm import Session
from . import models

# [수정] title, name, price, advice 순서와 이름을 recipe.py와 완벽히 맞췄습니다.
def update_or_create_ingredient(db: Session, title: str, name: str, price: str, advice: str):
    # 가격 문자열 "2,500"에서 콤마 제거 후 숫자로 변환
    try:
        clean_price = str(price).replace(",", "").replace("원", "").strip()
        numeric_price = float(clean_price)
    except:
        numeric_price = 0.0
    
    # 1. 이미 저장된 재료가 있는지 확인
    db_item = db.query(models.Ingredient).filter(models.Ingredient.name == name).first()
    
    if db_item:
        # 2. 있다면 정보 업데이트 (title과 advice 포함)
        db_item.recipe_title = title
        db_item.current_price = numeric_price
        db_item.ai_advice = advice
    else:
        # 3. 없다면 새로 생성
        db_item = models.Ingredient(
            recipe_title=title,
            name=name,
            current_price=numeric_price,
            ai_advice=advice,
            unit="개/g"
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def get_ingredient_history(db: Session, limit: int = 10):
    return db.query(models.Ingredient).order_by(models.Ingredient.updated_at.desc()).limit(limit).all()