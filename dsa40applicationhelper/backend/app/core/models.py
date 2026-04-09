


from pydantic_core import ErrorDetails
from pydantic import BaseModel

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
