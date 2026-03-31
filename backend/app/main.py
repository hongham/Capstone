import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv  # 추가
from .database import engine
from . import models
from app.api.recipe import router as recipe_router

# [가장 중요] 최상단에서 환경 변수를 로드합니다.
load_dotenv()

# 터미널에서 키가 잘 읽혔는지 확인하는 디버깅 코드 (성공하면 나중에 지우세요)
print(f"🚀 [시스템 체크] SPOON_API_KEY 로드 상태: {'성공' if os.getenv('SPOON_API_KEY') else '실패'}")

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Capstone Recipe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipe_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Capstone Backend Server!"}