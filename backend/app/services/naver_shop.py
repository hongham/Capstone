import os
import httpx
from fastapi import HTTPException

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

async def get_naver_shopping_item(query: str):
    # 1. 자취생에게 필요 없는 기본 품목 및 포장재 제외
    exclude_keywords = ["소금", "후추", "물", "설탕", "박스", "봉투", "용기", "스티커","업소"]
    if any(k in query for k in exclude_keywords):
        return None

    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    
    # [핵심] 검색어 뒤에 '식재료'를 붙여 식품 카테고리 유도
    params = {
        "query": f"{query} 식재료", 
        "display": 10,
        "sort": "sim"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()
        
        if data.get("items"):
            for item in data["items"]:
                title = item["title"].replace("<b>", "").replace("</b>", "")
                price = int(item["lprice"])
                
                # [필터] 요리와 상관없는 공산품 원천 차단
                bad_stuff = ["LP", "중고", "띠지", "퍼프", "화장", "에어캡", "포장재", "인쇄", "제작", "공병", "봉투"]
                if any(bs in title for bs in bad_stuff):
                    continue
                
                # 자취생 적정 가격 범위 (너무 싼 배송비 낚시나 너무 비싼 대용량 제외)
                if 500 < price < 50000:
                    return {
                        "title": title,
                        "lprice": price,
                        "link": item["link"]
                    }
    return None

async def get_total_shopping_list(ingredients: list):
    items = []
    total_price = 0
    for ing in ingredients:
        if len(ing) < 2: continue
        result = await get_naver_shopping_item(ing)
        if result:
            items.append(result)
            total_price += result["lprice"]
    return {"items": items, "total_price": total_price}