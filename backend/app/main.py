from fastapi import FastAPI
from .database import engine, Base
from . import models

# 서버 시작 시 DB 테이블 자동 생성
models.Base.metadata.create_all(bind=engine)

# uvicorn이 찾는 핵심 객체 'app'
app = FastAPI(title="Capstone Recipe API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Capstone Backend Server!"}

@app.get("/test-db")
def test_db():
    return {"status": "DB Tables Created Successfully"}