import os
import requests
from deep_translator import GoogleTranslator

SPOON_KEY = os.getenv("SPOON_API_KEY")

def get_recipe_info(recipe_id: int):
    # --- [Mock 로직 추가] 키가 없을 때 가짜 데이터 반환 ---
    if not SPOON_KEY:
        print("⚠️ 경고: API 키가 없습니다. 가상 데이터를 반환합니다.")
        return "테스트용 맛있는 파스타", "파스타면"
    # --------------------------------------------------

    # 1. Spoonacular API 호출
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={SPOON_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return "API 에러", "데이터를 가져오지 못했습니다."
            
        recipe_data = response.json()
        
        # 2. 첫 번째 재료 추출
        if recipe_data.get('extendedIngredients'):
            eng_name = recipe_data['extendedIngredients'][0]['name']
        else:
            eng_name = "ingredient not found"

        # 3. 한글로 번역
        ko_name = GoogleTranslator(source='en', target='ko').translate(eng_name)
        return recipe_data['title'], ko_name

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return "시스템 에러", "데이터 처리 중 오류 발생"