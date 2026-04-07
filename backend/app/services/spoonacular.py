import os
import httpx
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()

def search_recipes(query: str, budget: int = 10000):
    """모드별 키워드로 레시피 리스트 검색"""
    api_key = os.getenv("SPOON_API_KEY")
    url = "https://api.spoonacular.com/recipes/complexSearch"
    
    params = {
        "apiKey": api_key,
        "query": query,
        "number": 5,
        "addRecipeInformation": True,
        "fillIngredients": True
    }

    try:
        with httpx.Client() as client:
            response = client.get(url, params=params, timeout=10.0)
            data = response.json()
            results = []
            for item in data.get("results", []):
                results.append({
                    "id": item["id"],
                    "title": item["title"],
                    "image": item["image"],
                    "readyInMinutes": item.get("readyInMinutes", 0)
                })
            return results
    except Exception as e:
        print(f"🚀 Spoonacular 검색 에러: {e}")
        return []

def get_recipe_info(recipe_id: int):
    """특정 레시피 상세 정보 및 재료 번역"""
    api_key = os.getenv("SPOON_API_KEY")
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    
    try:
        with httpx.Client() as client:
            response = client.get(url, params={"apiKey": api_key}, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                title = data.get('title', 'Unknown Recipe')
                if data.get('extendedIngredients'):
                    eng_name = data['extendedIngredients'][0]['name']
                    ko_name = GoogleTranslator(source='en', target='ko').translate(eng_name)
                    return title, ko_name
                return title, "재료 정보 없음"
            return "API 오류", f"에러코드: {response.status_code}"
    except Exception as e:
        return "시스템 에러", str(e)