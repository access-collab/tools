import json
from pathlib import Path

from pydantic import BaseModel

from app.models import Condition

_DATA_DIR = Path(__file__).parent.parent / "data"


class PlatformMappingComplex(BaseModel):
    src: str | list[str]
    operation: str


PlatformMapping = str | PlatformMappingComplex


class CustomStuffs(BaseModel):
    mappings: dict[str, PlatformMapping]
    conditions: dict[str, Condition]


def _load_json(filename: str) -> CustomStuffs:
    path = _DATA_DIR / filename
    data = path.read_text()
    return CustomStuffs.model_validate_json(data)


def _write_json(filename: str, value: CustomStuffs):
    path = _DATA_DIR / filename
    serialized = json.dumps(value)
    with open(path, "w") as f:
        f.write(serialized)


def get_custom_stuffs_for(platform_name: str) -> CustomStuffs:
    return _load_json(f"{platform_name}.json")


def write_custom_stuffs_for(platform_name: str, stuff: CustomStuffs):
    return _write_json(f"{platform_name}.json", stuff)
