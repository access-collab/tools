from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel


class InputType(str, Enum):
    text = "text"
    file_upload = "file_upload"
    date_select = "date_select"
    selection = "selection"
    multi_select = "multi_select"


class Operator(str, Enum):
    eq = "eq"
    neq = "neq"


class Condition(BaseModel):
    vlopse_question_id: str
    operator: Operator
    value: Any


class Granularity(str, Enum):
    general = "general"
    platform_specific = "platform_specific"


class UnifiedQuestion(BaseModel):
    id: str
    text_en: str
    category: str
    type: InputType
    options: list[str] | None = None  # TODO: Aren't these dymanic?
    help_text: str | None = None
    granularity: Granularity


class VLOPSEQuestion(BaseModel):
    id: str
    question_text: str
    classification: str
    main_question: str  # maps to above
    type: InputType
    required: bool
    condition: Condition


class Frage(BaseModel):
    id: str
    text_en: str
    sources: list[VLOPSEQuestion]
    help_text: str | None = None


class Selection(BaseModel):
    i_type: Literal["selection"]
    options: list[str]


class Boolean(BaseModel):
    i_type: Literal["boolean"]


class Text(BaseModel):
    i_type: Literal["text"]
    max_length: int | None = None


class DateRange(BaseModel):
    i_type: Literal["daterange"]
    begin: Literal["TODO"]


InputTypeWithOptions = Selection | Boolean | Text | DateRange
