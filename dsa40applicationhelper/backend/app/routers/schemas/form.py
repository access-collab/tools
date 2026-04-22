from pydantic import BaseModel, ConfigDict

from app.models import InputType
from app.schemas import ConstraintConfig


class DSAQuestion(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    text: str
    input_type: InputType
    help_text: str | None = None
    config: ConstraintConfig | None = None
    options: list[str] | None = None
