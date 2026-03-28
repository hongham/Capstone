from fastapi import FastAPI
from .database import engine, Base
from . import models
import requests
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# DB 설정 (친구 코드 유지)
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Capstone Recipe API")

# 환경 변수 로드
load_dotenv()
SPOON_KEY = os.getenv("SPOON_API_KEY")
NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")

@app.get("/")
def read_root():
    return {"message": "Welcome to Capstone Backend Server!"}

# --- 재헌님이 만든 최저가 로직 추가 ---
@app.get("/recipe/{recipe_id}/price")
def get_recipe_price(recipe_id: int):
    # 1. 스푸나큘러에서 재료 가져오기
    spoon_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={SPOON_KEY}"
    recipe_data = requests.get(spoon_url).json()
    
    # 첫 번째 재료 추출 및 번역
    eng_name = recipe_data['extendedIngredients'][0]['name']
    ko_name = GoogleTranslator(source='en', target='ko').translate(eng_name)
    
    # 2. 네이버 최저가 검색
    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET
    }
    naver_url = f"https://openapi.naver.com/v1/search/shop.json?query={ko_name}&display=1&sort=asc"
    naver_res = requests.get(naver_url, headers=headers).json()
    
    price = naver_res['items'][0]['lprice'] if naver_res.get('items') else "0"

    return {
        "recipe_title": recipe_data['title'],
        "ingredient": ko_name,
        "lowest_price": price
    }