from enum import Enum
from typing import Any

from pydantic import BaseModel
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    String,
    Text,
)
from sqlalchemy import (
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Operator(str, Enum):
    eq = "eq"
    neq = "neq"


class Condition(BaseModel):
    vlopse_question_id: str
    operator: Operator
    value: Any

class InputType(str, Enum):
    text = "text"
    file_upload = "file_upload"
    date_select = "date_select"
    selection = "selection"
    multi_select = "multi_select"


class UnifiedQuestion(BaseModel):
    id: str
    ...


class Base(DeclarativeBase):
    pass


class ReprMixing:
    def __repr__(self) -> str:
        return self._repr(id=self.id)

    def _repr(self, **fields: dict[str, Any]) -> str:
        """
        Helper for __repr__
        """
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f"{key}={field!r}")
            except sa.orm.exc.DetachedInstanceError:
                field_strings.append(f"{key}=DetachedInstanceError")
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"


class VLOPSEQuestion(Base, ReprMixing):
    __tablename__ = "vlopse_question"
    id = Column(String, primary_key=True, index=True)
    text = Column(Text)
    vlopse = Column(String(255))
    required = Column(Boolean)
    options: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    input_type = Column(SQLAlchemyEnum(InputType))

    def __repr__(self):
        # easy to override, and it'll honor __repr__ in foreign relationships
        return self._repr(
            id=self.id,
            text=self.text,
            vlopse=self.vlopse,
            required=self.required,
            options=self.options,
            input_type=self.input_type,
        )


class DSAQuestion(Base, ReprMixing):
    __tablename__ = "dsa_question"
    id = Column(String, primary_key=True, index=True)
    text = Column(Text)
    category = Column(String(255))
    help_text = Column(Text, nullable=True)

    def __repr__(self):
        # easy to override, and it'll honor __repr__ in foreign relationships
        return self._repr(
            id=self.id, text=self.text, category=self.category, help_text=self.help_text
        )
