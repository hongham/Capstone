import os
import requests
from dotenv import load_dotenv

load_dotenv()

# 환경 변수 로드
NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def get_lowest_price(ko_ingredient: str):
    """단일 재료의 최저가를 검색합니다."""
    if not NAVER_ID or not NAVER_SECRET:
        return "0"

    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET
    }
    # [수정] query 인코딩 문제를 방지하기 위해 params 방식을 권장합니다.
    url = "https://openapi.naver.com/v1/search/shop.json"
    params = {"query": ko_ingredient, "display": 1, "sort": "asc"}
    
    try:
        res = requests.get(url, headers=headers, params=params, timeout=5)
        if res.status_code == 200:
            items = res.json().get('items')
            # 가격 데이터에 콤마나 문자가 섞여 있을 수 있으니 숫자만 추출
            return items[0]['lprice'] if items else "0"
        return "0"
    except:
        return "0"

def get_total_ingredients_price(ko_ingredients_list: list):
    """
    여러 개의 한글 재료 리스트를 받아 총 합산 가격을 계산합니다.
    (API 과부하를 방지하기 위해 상위 3~5개 정도만 계산하는 것이 좋습니다.)
    """
    total_price = 0
    detailed_prices = []

    # 너무 많은 재료를 다 검색하면 서버가 느려지므로 최대 4개까지만!
    for ingredient in ko_ingredients_list[:4]:
        price_str = get_lowest_price(ingredient)
        price_int = int(price_str) if price_str.isdigit() else 0
        
        if price_int > 0:
            total_price += price_int
            detailed_prices.append(f"{ingredient}({price_int}원)")

    # 상세 내역 문자열 생성 (예: "마늘(500원), 양파(1200원)...")
    summary = ", ".join(detailed_prices)
    return total_price, summary