from enum import Enum
from pathlib import Path
from typing import Any, Generator

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Enum,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.models import InputType

DB_PATH = Path(__file__).parent / "data" / "app.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
    input_type = Column(Enum(InputType))

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


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_questions_for(vlopses: list[str]):
    db = SessionLocal()
    result = db.query(VLOPSEQuestion).where(VLOPSEQuestion.vlopse.in_(vlopses)).all()
    return result


def get_question(question_id: str):
    db = SessionLocal()
    result = db.query(VLOPSEQuestion).where(VLOPSEQuestion.id == question_id).first()
    return result


def add_vlopse_question(question: VLOPSEQuestion):
    db = SessionLocal()
    db.add(question)
    db.commit()
