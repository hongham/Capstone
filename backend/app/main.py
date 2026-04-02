import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .database import engine
from . import models

# 환경 변수 로드
base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

print(f"🚀 [시스템 체크] 환경 변수 로드 성공 여부: {bool(os.getenv('SPOON_API_KEY'))}")

from .database import engine
from . import models  # models.py의 내용을 가져옴
from app.api.recipe import router as recipe_router

# DB 테이블 생성 (models.py에 정의된 구조대로 생성)
models.Base.metadata.create_all(bind=engine)


models.Base.metadata.drop_all(bind=engine) # 기존 테이블 삭제
models.Base.metadata.create_all(bind=engine) # 새 설계도로 생성
app = FastAPI(title="Hallym Recipe API")

# 라우터 등록
app.include_router(recipe_router)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Recipe API Server is Running!"}