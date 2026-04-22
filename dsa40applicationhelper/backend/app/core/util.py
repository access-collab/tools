from pathlib import Path
from typing import Any

_DATA_DIR = Path(__file__).parent.parent / "data"


def find_inputs_for_multiple(candidates: dict[str, Any], keys: list[str]):
    print(f"Finding multiple {keys} in {candidates}")
    return {k: v for k, v in candidates.items() if k in keys}
