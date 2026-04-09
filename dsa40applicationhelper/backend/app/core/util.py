from pathlib import Path

from pydantic import TypeAdapter

from app.models import UnifiedQuestion

_DATA_DIR = Path(__file__).parent.parent / "data"
someadapter = TypeAdapter(list[UnifiedQuestion])


def dEBUGLOAD():
    path = _DATA_DIR / "questions.json"
    data = path.read_text()
    result = someadapter.validate_json(data)
    return result
