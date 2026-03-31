import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # [추가] CORS 도구
from dotenv import load_dotenv 
from .database import engine
from . import models
from app.api.recipe import router as recipe_router 

# 1. 환경 변수 로드 (최상단)
load_dotenv()

# 2. DB 테이블 생성 (기존 유지)
models.Base.metadata.create_all(bind=engine)

# 3. 앱 객체 생성
app = FastAPI(title="Capstone Recipe API")

# 4. [핵심 추가] 프론트엔드(Flutter)와 통신을 위한 CORS 설정
# 이 코드가 있어야 나중에 친구들이 만든 앱에서 접속이 가능합니다!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 모든 접속 허용
    allow_credentials=True,
    allow_methods=["*"],      # 모든 방식(GET, POST 등) 허용
    allow_headers=["*"],      # 모든 데이터 헤더 허용
)

# 5. 라우터 등록 (기존 유지)
app.include_router(recipe_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Capstone Backend Server!"}