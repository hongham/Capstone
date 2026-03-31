from sqlalchemy.orm import Session
from . import models

def update_or_create_ingredient(db: Session, name: str, price: str):
    # 가격 문자열에서 콤마(,) 제거하고 숫자로 변환 (예: "2,500" -> 2500.0)
    numeric_price = float(price.replace(",", ""))
    
    # 1. 이미 있는 재료인지 이름으로 확인
    db_ingredient = db.query(models.Ingredient).filter(models.Ingredient.name == name).first()
    
    if db_ingredient:
        # 2. 이미 있으면 가격만 최신으로 업데이트
        db_ingredient.current_price = numeric_price
    else:
        # 3. 없으면 새로운 재료로 추가
        db_ingredient = models.Ingredient(
            name=name,
            current_price=numeric_price,
            unit="개/g"  # 기본 단위 설정
        )
        db.add(db_ingredient)
    
    db.commit()      # DB에 반영
    db.refresh(db_ingredient) # 최신 상태로 갱신
    return db_ingredient