import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# [핵심] 현재 파일(main.py)의 위치를 기준으로 한 칸 위(backend)에 있는 .env를 정확히 지목합니다.
base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"
load_dotenv(dotenv_path=env_path)

# 터미널에서 확인용 (키가 있으면 True가 뜹니다)
print(f"🚀 [시스템 체크] 환경 변수 로드 성공 여부: {bool(os.getenv('SPOON_API_KEY'))}")

from .database import engine
from . import models
from app.api.recipe import router as recipe_router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# ... CORS 및 라우터 설정 동일 ...