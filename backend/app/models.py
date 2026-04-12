from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    # 기본키 이름을 recipe_id로 명확히 지정합니다.
    recipe_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    image = Column(String, nullable=True)
    readyInMinutes = Column(Integer, nullable=True)
    summary = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)

    # 관계 설정 (레시피 하나에 여러 재료가 연결됨)
    ingredients = relationship("Ingredient", back_populates="recipe")

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    # 외래키: recipes 테이블의 recipe_id 컬럼을 정확히 참조합니다.
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"))
    name = Column(String, index=True)
    current_price = Column(Float, nullable=True)
    purchase_url = Column(Text, nullable=True)
    unit = Column(String, nullable=True)
    ai_advice = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계 설정
    recipe = relationship("Recipe", back_populates="ingredients")