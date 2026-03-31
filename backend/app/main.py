import os
from fastapi import FastAPI
from dotenv import load_dotenv  # <-- 이 줄이 반드시 있어야 합니다!
from .database import engine
from . import models
# api.recipe에서 router를 가져올 때 이름 충돌을 피하기 위해 alias를 씁니다.
from app.api.recipe import router as recipe_router 

# 1. 환경 변수 로드 (최상단에서 실행)
load_dotenv()

# 2. DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

# 3. 앱 객체 생성
app = FastAPI(title="Capstone Recipe API")

# 4. 라우터 등록
app.include_router(recipe_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Capstone Backend Server!"}