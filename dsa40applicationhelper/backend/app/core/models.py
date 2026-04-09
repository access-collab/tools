from pydantic import BaseModel

class PlatformMappingComplex(BaseModel):
    src: str | list[str]
    operation: str


PlatformMapping = str | PlatformMappingComplex

