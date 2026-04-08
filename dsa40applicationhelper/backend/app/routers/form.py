from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.services.vlopse import VlopseConfigService
router = APIRouter()
service = VlopseConfigService()


@router.get("/api/questions")
async def applicable_questions(
    vlopse: list[str] = Query(...), kek: int = 1
) -> list[UnifiedQuestion]:
    selected_vlopses = vlopse or []
    vlopses = service.get_all()
    print(f"Asking for {vlopse}")
    missing = [s for s in selected_vlopses if s not in vlopses]
    if len(missing):
        raise HTTPException(status_code=322, detail=f"Unknown vlopse(s): {missing}")
    mapper = QuestionMapper.from_vlopse_names(vlopse)
    qs = mapper.map()

    print(f"Returning {qs}")

    return qs


