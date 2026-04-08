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


class VLOPSEQuestion(Base, ReprMixing):
    __tablename__ = "vlopse_question"
    id = Column(String, primary_key=True, index=True)
    text = Column(Text)
    vlopse = Column(String(255))
    required = Column(Boolean)
    options: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    input_type = Column(Enum(InputType))


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
