from app.database import SessionLocal
from app.models import DSAQuestion, VLOPSEQuestion


class QuestionService:
    def __init__(self):
        # TODO: self, app=.. then app.async session lala
        pass

    def add(
        self,
        id: str | None,
        text: str,
        vlopse: str,
        required: bool,
        input_type: str,
        details: str | None,
        config: dict[str, str] | None = None,
    ):
        question = VLOPSEQuestion(
            id=id,
            text=text,
            vlopse=vlopse,
            required=required,
            input_type=input_type,
            details=details,
            config=config,
        )
        db = SessionLocal()
        db.add(question)
        db.commit()

    def get_all_for_vlopse(self, vlopse: str):
        db = SessionLocal()
        result = db.query(VLOPSEQuestion).where(VLOPSEQuestion.vlopse == vlopse).all()

        return result

    def get(self, question_id: str):
        db = SessionLocal()
        question = (
            db.query(VLOPSEQuestion).where(VLOPSEQuestion.id == question_id).first()
        )

        print(f"Gotted{question}")
        return question

    def add_unified(
        self,
        id: str | None,
        text: str,
        input_type: str,
        help_text: str | None,
        config: dict[str, str] | None = None,
    ):
        question = DSAQuestion(
            id=id, text=text, input_type=input_type, help_text=help_text, config=config
        )
        # id = Column(String, primary_key=True, index=True)
        # text = Column(Text)
        # help_text = Column(Text, nullable=True)
        # input_type = Column(SQLAlchemyEnum(InputType))
        # config: Mapped[dict | None] = mapped_column(JSON, nullable=True)
        db = SessionLocal()
        db.add(question)
        db.commit()

    def get_unified(self, question_id: str):
        db = SessionLocal()
        question = db.query(DSAQuestion).where(DSAQuestion.id == question_id).first()

        print(f"Gotted{question}")
        return question

    def get_all_unified_for(self, question_ids: list[str]):
        db = SessionLocal()
        result = db.query(DSAQuestion).where(DSAQuestion.id.in_(question_ids)).all()

        return result

    def get_all_unified(self):
        db = SessionLocal()
        print("Selecting all DSA..")
        question = db.query(DSAQuestion).all()

        print(f"Gotted{question}")
        return question
