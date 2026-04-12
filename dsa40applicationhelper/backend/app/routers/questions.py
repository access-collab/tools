from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from app.models import InputType
from app.schemas import ConstraintConfig
from app.services.questions import QuestionService
from app.services.vlopse import VlopseConfigService

router = APIRouter()
vlopse_service = VlopseConfigService()
question_service = QuestionService()


class VlopseQuestion(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    text: str
    required: bool
    input_type: InputType
    config: ConstraintConfig | None = None
    details: str | None = None
    vlopse: str


class PostVlopseQuestionRequest(VlopseQuestion):
    vlopse: str | None = None


@router.get("/api/vlopse/{name}/question")
async def get_questions(name: str) -> JSONResponse:
    questions = question_service.get_all_for_vlopse(vlopse=name)
    result = []
    for q in questions:
        qq = VlopseQuestion.model_validate(q)
        result.append(qq)

    return result


@router.get("/api/vlopse/{vlopse_name}/question/{question_id}")
async def get_question(vlopse_name: str, question_id: str) -> VlopseQuestion:
    question = question_service.get(question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="question not found")

    return VlopseQuestion.model_validate(question)


@router.post("/api/vlopse/{name}/question")
async def add_question(name: str, question: PostVlopseQuestionRequest) -> JSONResponse:
    question.vlopse = name
    question_service.add(
        **question.model_dump(),
    )

    return JSONResponse({"success": True})
