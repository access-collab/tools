from enum import Enum
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text
from app.database import SessionLocal

router = APIRouter()


class Status(str, Enum):
    OK = "ok"
    ERROR = "error"


class HealthResponse(BaseModel):
    api: Status
    db: Status


@router.get("/health")
def health_check() -> HealthResponse:
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        db_status = Status.OK
    except Exception:
        db_status = Status.ERROR
    finally:
        db.close()
    return HealthResponse(api=Status.OK, db=db_status)
