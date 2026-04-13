import os
import httpx
from dotenv import load_dotenv
from app.services.translator import translate_cuisine, translate_to_english

load_dotenv()

SPOON_API_KEY = os.getenv("SPOON_API_KEY")
BASE_URL = "https://api.spoonacular.com/recipes"

async def search_recipes_from_api(cuisine: str, ingredients: str, difficulty_tags: list):
    """
    Spoonacular API의 complexSearch를 호출하여 원본 레시피 데이터를 가져옵니다.
    """
    url = f"{BASE_URL}/complexSearch"
    
    # 1. 번역 적용
    eng_cuisine = translate_cuisine(cuisine)
    eng_ingredients = translate_to_english(ingredients)
    
    # 2. 파라미터 조립
    params = {
        "apiKey": SPOON_API_KEY,
        "cuisine": eng_cuisine,
        "includeIngredients": eng_ingredients,
        "number": 4,                # 화면 1-5 설계서에 맞춰 4개만!
        "addRecipeInformation": True, # 가격(pricePerServing), 조리시간 정보를 위해 필수
        "fillIngredients": True      # 상세 재료 정보를 위해 필수
    }

    # 3. 난이도(시간) 조건 추가 (화면 1-3 대응)
    # '10분완성'이 태그에 있다면 maxReadyTime 파라미터 추가
    if "10분완성" in difficulty_tags:
        params["maxReadyTime"] = 10

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except Exception as e:
            print(f"🚀 Spoonacular API 호출 에러: {e}")
            return []

async def get_recipe_detail_from_api(recipe_id: int):
    """
    특정 레시피의 상세 정보(재료 리스트 등)를 가져옵니다. (화면 1-6용)
    """
    url = f"{BASE_URL}/{recipe_id}/information"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params={"apiKey": SPOON_API_KEY}, timeout=10.0)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"🚀 상세 정보 가져오기 에러: {e}")
            return None