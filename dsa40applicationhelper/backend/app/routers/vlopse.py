from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.questions import QuestionService
from app.services.vlopse import (
    VlopseConfigService,
    VlopseDoesNotExistException,
    VlopseExistsException,
)

router = APIRouter()
vlopse_service = VlopseConfigService()
question_service = QuestionService()


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
