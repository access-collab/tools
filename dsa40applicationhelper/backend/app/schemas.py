from typing import Annotated, Literal, Union

from pycountry import countries
from pydantic import BaseModel, Field, TypeAdapter


class ISO_3166_1(BaseModel):
    type: Literal["iso-3166-1"]

    def validate_answer(self, value) -> str | None:
        # TODO: 11.04 this is None, ensure its never
        if not isinstance(value, str):
            return f"Invalid input {value} with type {type(value)}"
        country = countries.get(name=value)
        if country is None:
            return f"Invalid selection: {value}"


class Selection(BaseModel):
    # TODO: rename property name
    type: Literal["selection"]
    options: list[str]
    multiple: bool = False

    def validate_answer(self, value) -> str | None:
        if isinstance(value, list) and not self.multiple:
            return "Only one selection allowed"
        values = value if isinstance(value, list) else [value]
        invalid = [v for v in values if v not in self.options]
        if invalid:
            return f"Invalid option(s): {', '.join(invalid)}. Possible: {', '.join(self.options)}"
        return None


class Boolean(BaseModel):
    type: Literal["boolean"]


class Text(BaseModel):
    type: Literal["text"]
    max_length: int | None = None

    def validate_answer(self, value: str) -> str | None:
        if self.max_length and len(value) > self.max_length:
            return f"Must not exceed {self.max_length} characters"
        return None


class DateRange(BaseModel):
    type: Literal["daterange"]
    begin: Literal["TODO"]


class DateSelect(BaseModel):
    type: Literal["date_select"]


ConstraintConfig = Annotated[
    Union[Selection | Text | ISO_3166_1], Field(discriminator="type")
]

config_adapter = TypeAdapter(ConstraintConfig)
