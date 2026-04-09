from enum import Enum
from typing import Any

from pydantic import BaseModel
from pydantic_core import ErrorDetails

from app.models import InputType


class PlatformMappingComplex(BaseModel):
    src: str | list[str]
    operation: str


PlatformMapping = str | PlatformMappingComplex


class VlopseAnswer(BaseModel):
    id: str
    value: str


class Answer(BaseModel):
    question_id: str
    value: str


class MappedAnswer(BaseModel):
    question_id: str
    value: str


class MappingError(BaseModel):
    question_id: str
    errors: list[ErrorDetails]


class UnifiedQuestion(BaseModel):
    id: str
    text_en: str
    category: str
    type: InputType
    granularity: str
    options: list[str] | None = None  # FIXME: use InputTypeWithOptions
    help_text: str | None = None


class Operator(str, Enum):
    eq = "eq"
    neq = "neq"


class Condition(BaseModel):
    vlopse_question_id: str
    operator: Operator
    value: Any
