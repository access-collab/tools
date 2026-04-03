import json
from pathlib import Path
from typing import Any, TypedDict

from app.models import Condition, PlatformMapping

_DATA_DIR = Path(__file__).parent.parent / "data"


class CustomStuffs(TypedDict):
    mappings: dict[str, PlatformMapping]
    conditions: list[Condition]


def _load_json(filename: str) -> Any:
    path = _DATA_DIR / filename
    with open(path) as f:
        return json.load(f)


def _write_json(filename: str, value: CustomStuffs):
    path = _DATA_DIR / filename
    serialized = json.dumps(value)
    with open(path, "w") as f:
        f.write(serialized)


def get_custom_stuffs_for(platform_name: str) -> CustomStuffs:
    return _load_json(f"{platform_name}.json")


def write_custom_stuffs_for(platform_name: str, stuff: CustomStuffs):
    return _write_json(f"{platform_name}.json", stuff)
