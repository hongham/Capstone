from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RecipePriceResponse(BaseModel):
    recipe_title: str
    ingredient: str
    lowest_price: str
    ai_advice: str

class IngredientHistory(BaseModel):
    recipe_title: Optional[str] = None
    name: str
    current_price: float
    ai_advice: Optional[str] = None
    updated_at: datetime

    class Config:
        from_attributes = True