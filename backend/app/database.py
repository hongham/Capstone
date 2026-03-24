from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. DB 접속 주소
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/capstone_db"

# 2. SQLAlchemy 엔진 생성 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. DB 세션 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 모델 생성을 위한 기본 클래스
Base = declarative_base()

# DB 세션 연결 및 종료를 관리하는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()