from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    OK = "ok"
    ERROR = "error"


class HealthResponse(BaseModel):
    api: Status
    db: Status
    dsa_status: int | Status
    mapping_status: int | Status
