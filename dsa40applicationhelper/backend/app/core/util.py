from pathlib import Path
from typing import Any

from pydantic import TypeAdapter

from .models import UnifiedQuestion

_DATA_DIR = Path(__file__).parent.parent / "data"
someadapter = TypeAdapter(list[UnifiedQuestion])


def find_inputs_for_multiple(candidates: dict[str, Any], keys: list[str]):
    print(f"Finding multiple {keys} in {candidates}")
    return {k: v for k, v in candidates.items() if k in keys}


def dEBUGLOAD():
    path = _DATA_DIR / "questions.json"
    data = path.read_text()
    result = someadapter.validate_json(data)
    return result
