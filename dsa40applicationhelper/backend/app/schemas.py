from typing import Literal

from pydantic import BaseModel


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
