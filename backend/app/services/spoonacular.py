import os
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

def get_recipe_info(recipe_id: int):
    # [핵심] 함수가 실행되는 순간에 한 번 더 로드해서 키를 확실히 챙깁니다.
    load_dotenv()
    spoon_key = os.getenv("SPOON_API_KEY")

    if not spoon_key:
        return "설정 오류", "환경 변수에서 API 키를 여전히 찾을 수 없습니다."

    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={spoon_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            title = data.get('title', 'Unknown Recipe')
            
            if data.get('extendedIngredients'):
                eng_name = data['extendedIngredients'][0]['name']
                # 번역기 작동
                ko_name = GoogleTranslator(source='en', target='ko').translate(eng_name)
                return title, ko_name
            return title, "재료 정보 없음"
            
        return "API 오류", f"Spoonacular 응답 에러: {response.status_code}"
    except Exception as e:
        return "시스템 에러", str(e)