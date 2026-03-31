from fastapi import APIRouter
# 일단 서비스 호출 부분은 주석 처리하거나 빼고, 구조부터 잡을게요
# from app.services.spoonacular import get_recipe_info 
# from app.services.naver_shop import get_lowest_price

router = APIRouter() # <--- 이 이름이 main.py의 'recipe_router'와 연결됩니다.

@router.get("/recipe/{recipe_id}/price")
def get_recipe_price(recipe_id: int):
    return {"message": "구조 연결 성공! 이제 API 키만 넣으면 됩니다."}