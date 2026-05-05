from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.core.models import Answer, ErrorDetails, MappedAnswer, MappingError
from app.models import InputType
from app.services.form_engine import FormService
from app.services.questions import QuestionService
from app.services.vlopse import VlopseConfigService

from .schemas.form import DSAQuestion

router = APIRouter()

service = VlopseConfigService()
form_service = FormService()
question_service = QuestionService()


class PostDSAQuestionRequest(BaseModel):
    id: str
    text: str
    input_type: InputType
    help_text: str | None = None
    config: dict[str, str] | None = None


@router.post("/api/question")
async def add_dsa_question(question: PostDSAQuestionRequest):
    question_service.add_unified(**question.model_dump())
    return {"success": True}


@router.get("/api/question/{id}")
async def get_dsa_question(id: str):
    return question_service.get_unified(id)


@router.get("/api/question")
async def get_all_dsa_questions():
    return question_service.get_all_unified()


@router.get("/api/questions")
async def applicable_questions(vlopse: list[str] = Query(...)) -> list[DSAQuestion]:
    selected_vlopses = vlopse or []
    vlopses = service.get_all()
    print(f"Asking for {vlopse}")
    missing = [s for s in selected_vlopses if s not in vlopses]
    if len(missing):
        raise HTTPException(status_code=322, detail=f"Unknown vlopse(s): {missing}")
    qs = form_service.get_required_questions_for(vlopse)

    response: list[DSAQuestion] = []
    for q in qs:
        res = DSAQuestion.model_validate(q)
        res.options = form_service.compute_options(q, vlopse)
        response.append(res)

    print(f"Returning {len(response)} DSA questions..")

    return response


class MappedAnswerWithText(MappedAnswer):
    text: str


class MappingErrorWithText(MappingError):
    text: str


MappingResultWithText = Annotated[
    MappedAnswerWithText | MappingErrorWithText, Field(discriminator="type")
]


class AnswerRequest(BaseModel):
    answers: list[Answer]


class TransformResponseForVlopse(BaseModel):
    name: str
    answers: list[MappingResultWithText]


class TransformResponse(BaseModel):
    by_vlopse: list[TransformResponseForVlopse]


class ValidationResponse(BaseModel):
    errors: dict[str, list[ErrorDetails] | str]
    ok: bool
    kind: Literal["validation", "transformation"]


@router.post("/api/validate")
async def validate_answers(
    answers: AnswerRequest, vlopse: list[str] = Query(...)
) -> ValidationResponse:
    answers_inner = answers.answers
    print("Checking answers..")
    result = form_service.validate_unified_question(answers_inner)
    print(result)
    kind = "validation"
    ok = len(result) == 0
    print(f"Ok: {ok}")
    if ok:
        ok, result = form_service.map_unified_to_vlopse_and_validate(
            answers_inner, vlopse
        )
        kind = "transformation"
    return ValidationResponse(errors=result, ok=ok, kind=kind)


@router.post("/api/transform")
async def transform_answers(answers: AnswerRequest, vlopse: list[str] = Query(...)):
    answers_inner = answers.answers
    result = form_service.transform_answers_to_vlopse_answers(vlopse, answers_inner)
    res = [TransformResponseForVlopse(name=name, answers=res) for name, res in result]

    print(f"TRANSFORM RESULT {result}")

    response = TransformResponse(by_vlopse=res)

    return response
