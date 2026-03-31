import os
import requests

# main.py가 로드한 값을 사용
NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def get_lowest_price(ko_ingredient: str):
    if not NAVER_ID or not NAVER_SECRET:
        return "0"

    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET
    }
    url = f"https://openapi.naver.com/v1/search/shop.json?query={ko_ingredient}&display=1&sort=asc"
    
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            items = res.json().get('items')
            return items[0]['lprice'] if items else "0"
        return "0"
    except:
        return "0"