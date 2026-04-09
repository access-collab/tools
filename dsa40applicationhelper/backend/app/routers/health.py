from fastapi import APIRouter
from sqlalchemy import text

from app.database import SessionLocal

from .schemas.health import HealthResponse, Status

router = APIRouter()


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
