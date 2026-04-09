
from pydantic import BaseModel

from app.schemas import InputTypeWithOptions


class DSAQuestion(BaseModel):
    id: str
    text: str
    type: InputTypeWithOptions
    help_text: str | None = None
