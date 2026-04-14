import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 환경 변수 로드
base_dir = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=base_dir / ".env")

from app.database import engine
from app import models
from app.api.recipe import router as recipe_router

# DB 초기화
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hallym Recipe API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipe_router, prefix="/api")

@app.get("/", tags=["Root"])
def root():
    return {"message": "자취생 요리 경제 비서 API 서버 정상 작동 중!"}