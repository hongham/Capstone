import os
import requests

NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def get_lowest_price(ko_ingredient: str):
    # --- [Mock 로직 추가] 키가 없을 때 가짜 가격 반환 ---
    if not NAVER_ID or not NAVER_SECRET:
        return "2500" # 테스트용 최저가
    # --------------------------------------------------

    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET
    }
    url = f"https://openapi.naver.com/v1/search/shop.json?query={ko_ingredient}&display=1&sort=asc"
    
    try:
        res = requests.get(url, headers=headers).json()
        return res['items'][0]['lprice'] if res.get('items') else "0"
    except:
        return "0"