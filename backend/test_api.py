import os
import requests
from dotenv import load_dotenv
from deep_translator import GoogleTranslator # 최신 파이썬용 번역 라이브러리

# 1. .env 파일에서 설정값 로드
load_dotenv()
SPOON_KEY = os.getenv("SPOON_API_KEY")
NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def run_integration_test(recipe_id):
    print(f"🚀 [1단계] Spoonacular에서 레시피 가져오기 (ID: {recipe_id})")
    
    # Spoonacular API 호출
    spoon_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={SPOON_KEY}"
    spoon_res = requests.get(spoon_url)
    
    if spoon_res.status_code != 200:
        print(f"❌ Spoonacular 에러: {spoon_res.status_code}. 키를 확인하세요.")
        return

    recipe_data = spoon_res.json()
    # 첫 번째 재료 추출 (예: "pasta")
    eng_ingredient = recipe_data['extendedIngredients'][0]['name']
    
    print(f"✅ 레시피명: {recipe_data['title']}")
    print(f"✅ 원본 재료(영문): {eng_ingredient}")
    print("-" * 30)

    # 2. 한글로 번역 (deep-translator 사용)
    print(f"🚀 [2단계] 영어를 한글로 번역 중...")
    try:
        ko_ingredient = GoogleTranslator(source='en', target='ko').translate(eng_ingredient)
        print(f"✅ 번역된 재료(한글): {ko_ingredient}")
    except Exception as e:
        print(f"❌ 번역 에러: {e}")
        ko_ingredient = eng_ingredient # 번역 실패 시 영어 그대로 사용

    print("-" * 30)

    # 3. 네이버 쇼핑 최저가 검색
    print(f"🚀 [3단계] 네이버 쇼핑에서 '{ko_ingredient}' 최저가 검색")
    
    naver_url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET
    }
    params = {
        "query": ko_ingredient,
        "display": 1,
        "sort": "asc" # 최저가순 정렬
    }
    
    naver_res = requests.get(naver_url, headers=headers, params=params)
    
    if naver_res.status_code != 200:
        print(f"❌ 네이버 API 에러: {naver_res.status_code}. 설정을 확인하세요.")
        print(f"에러 메시지: {naver_res.text}")
        return

    shop_data = naver_res.json()
    if shop_data.get('items'):
        item = shop_data['items'][0]
        # 상품명에서 <b> 태그 제거
        clean_title = item['title'].replace('<b>', '').replace('</b>', '')
        print(f"✅ 최저가 상품명: {clean_title}")
        print(f"✅ 가격: {item['lprice']}원")
        print(f"✅ 쇼핑몰: {item['mallName']}")
        print(f"✅ 구매 링크: {item['link']}")
    else:
        print("❓ 네이버 검색 결과가 없습니다.")

if __name__ == "__main__":
    # 테스트용 레시피 ID (716429는 파스타 레시피)
    run_integration_test(716429)