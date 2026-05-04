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
        with SessionLocal() as db:
            db.add(question)
            db.commit()

    def get_all_for_vlopse(self, vlopse: str):
        with SessionLocal() as db:
            result = (
                db.query(VLOPSEQuestion).where(VLOPSEQuestion.vlopse == vlopse).all()
            )

            return result

    def get(self, question_id: str):
        with SessionLocal() as db:
            question = (
                db.query(VLOPSEQuestion).where(VLOPSEQuestion.id == question_id).first()
            )

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
        with SessionLocal() as db:
            db.add(question)
            db.commit()

    def get_unified(self, question_id: str):
        with SessionLocal() as db:
            question = (
                db.query(DSAQuestion).where(DSAQuestion.id == question_id).first()
            )

            return question

    def get_all_unified_for(self, question_ids: list[str]):
        with SessionLocal() as db:
            result = db.query(DSAQuestion).where(DSAQuestion.id.in_(question_ids)).all()

            return result

    def get_all_unified(self):
        with SessionLocal() as db:
            question = db.query(DSAQuestion).all()

            return question
