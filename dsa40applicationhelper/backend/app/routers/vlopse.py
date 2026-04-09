from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.models import InputTypeWithOptions
from app.services.questions import QuestionService
from app.services.vlopse import (
    VlopseConfigService,
    VlopseDoesNotExistException,
    VlopseExistsException,
)

router = APIRouter()
vlopse_service = VlopseConfigService()
question_service = QuestionService(None)


@router.get("/api/vlopse", response_model=list[str])
async def get_vlopse() -> JSONResponse:
    vlopses = vlopse_service.get_all()
    return JSONResponse(vlopses)


class PostVlopseRequest(BaseModel):
    name: str


@router.post("/api/vlopse")
async def add_vlopse(new_vlopse: PostVlopseRequest) -> JSONResponse:
    try:
        vlopse_service.add(new_vlopse.name)
    except VlopseExistsException:
        raise HTTPException(status_code=409, detail="vlopse already exists")

    return JSONResponse({"success": True})


class PutVlopseRequest(BaseModel):
    new_name: str


@router.put("/api/vlopse/{name}")
async def put_vlopse(name: str, req: PutVlopseRequest) -> JSONResponse:
    try:
        vlopse_service.rename(name, req.new_name)
    except VlopseDoesNotExistException:
        raise HTTPException(status_code=404, detail="vlopse does not exist")
    except VlopseExistsException:
        raise HTTPException(status_code=409, detail="vlopse already exists")
    return JSONResponse({"success": True})


@router.delete("/api/vlopse/{name}")
async def delete_vlopse(name: str) -> JSONResponse:
    try:
        vlopse_service.delete(name)
    except VlopseDoesNotExistException:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse({"success": True})


class IType:
    pass


def to_pydantic(question: VLOPSEQuestion):
    i_type = {"i_type": question.input_type}
    i_type.update(question.options)
    return VlopseQuestion(
        id=question.id,
        text=question.text,
        required=question.required,
        vlopse=question.vlopse,
        input_type=i_type,
    )


class PostVlopseQuestionRequest(BaseModel):
    id: str | None
    text: str
    required: bool
    input_type: InputTypeWithOptions = Field(discriminator="i_type")


###### QUESTIONS
@router.get("/api/vlopse/{name}/question")
async def get_questions(name: str) -> JSONResponse:
    try:
        questions = question_service.get_all_for_vlopse(vlopse=name)
        result = []
        for q in questions:
            result.append(to_pydantic(q))

        return result
    except VlopseExistsException:
        raise HTTPException(status_code=409, detail="vlopse already exists")


class VlopseQuestion(BaseModel):
    id: str
    text: str
    required: bool
    vlopse: str
    input_type: InputTypeWithOptions = Field(discriminator="i_type")


@router.get("/api/vlopse/{vlopse_name}/question/{question_id}")
async def get_question(vlopse_name: str, question_id: str) -> JSONResponse:
    try:
        question = question_service.get(question_id)
        if question is None:
            raise HTTPException(status_code=404, detail="question not found")

        return to_pydantic(question)

        res = PostVlopseQuestionRequest.model_validate(question)

        return JSONResponse(res)
    except VlopseExistsException:
        raise HTTPException(status_code=409, detail="vlopse already exists")


@router.post("/api/vlopse/{name}/question")
async def add_question(name: str, question: PostVlopseQuestionRequest) -> JSONResponse:
    try:
        question_service.add(
            vlopse=name,
            **question.model_dump(exclude={"input_type"}),
            input_type_with_options=question.input_type,
        )
    except VlopseExistsException:
        raise HTTPException(status_code=409, detail="vlopse already exists")

    return JSONResponse({"success": True})
