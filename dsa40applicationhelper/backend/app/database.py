from pathlib import Path
from typing import Generator

from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base

DB_PATH = Path(__file__).parent / "data" / "app.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

def get_questions_for(vlopses: list[str]):
    db = SessionLocal()
    result = db.query(VLOPSEQuestion).where(VLOPSEQuestion.vlopse.in_(vlopses)).all()
    return result


def get_question(question_id: str):
    db = SessionLocal()
    result = db.query(VLOPSEQuestion).where(VLOPSEQuestion.id == question_id).first()
    return result


def add_vlopse_question(question: VLOPSEQuestion):
    db = SessionLocal()
    db.add(question)
    db.commit()
