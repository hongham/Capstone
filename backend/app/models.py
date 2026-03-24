from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    cooking_time = Column(Integer)  # 분 단위
    mode_tag = Column(String)       # 설거지최소화 등
    total_cost = Column(Integer)    # 예상 단가

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    current_price = Column(Float)   # 단위당 가격
    unit = Column(String)           # g, 개 등