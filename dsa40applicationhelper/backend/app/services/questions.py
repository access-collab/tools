from app.database import (
    VLOPSEQuestion,
    add_vlopse_question,
    get_question,
    get_questions_for,
)
from app.models import InputTypeWithOptions


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
        print(f"Adding {question}")
        add_vlopse_question(question)

    def get_all_for_vlopse(self, vlopse: str):
        questions = get_questions_for([vlopse])
        return questions

    def get(self, id: str):
        question = get_question(id)
        print(f"Gotted{question}")
        return question
