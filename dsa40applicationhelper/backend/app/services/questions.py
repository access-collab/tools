from app.database import SessionLocal
from app.models import VLOPSEQuestion
from app.schemas import InputTypeWithOptions


class QuestionService:
    def __init__(self, db):
        pass

    def add(
        self,
        id: str | None,
        text: str,
        vlopse: str,
        required: bool,
        input_type_with_options: InputTypeWithOptions,
    ):
        i_type = input_type_with_options.i_type
        options = input_type_with_options.model_dump(exclude=["i_type"])
        question = VLOPSEQuestion(
            id=id,
            text=text,
            vlopse=vlopse,
            required=required,
            input_type=i_type,
            options=options,
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
