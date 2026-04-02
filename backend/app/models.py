from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    cooking_time = Column(Integer)
    mode_tag = Column(String)
    total_cost = Column(Integer)

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    recipe_title = Column(String)
    name = Column(String, unique=True, index=True)
    current_price = Column(Float)
    unit = Column(String, default="개/g")
    ai_advice = Column(String)
    # SQLAlchemy 표준에 맞춰 onupdate로 수정
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())