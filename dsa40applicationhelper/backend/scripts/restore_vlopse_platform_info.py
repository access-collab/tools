"""Restore platform info blocks in vlopse JSON configs.

Usage (from backend/):
    uv run python scripts/restore_vlopse_platform_info.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import PlatformInformation, VLOPSEConfiguration, write_vlopse_configuration_for

VLOPSES_DIR = Path(__file__).resolve().parents[1] / "app" / "data" / "vlopses"
DEFAULTS_PATH = Path(__file__).resolve().parents[1] / "app" / "data" / "platform_info.json"


def load_defaults() -> dict[str, dict[str, object]]:
    return json.loads(DEFAULTS_PATH.read_text(encoding="utf-8"))


def restore_all() -> None:
    defaults = load_defaults()
    for vlopse, info in defaults.items():
        path = VLOPSES_DIR / f"{vlopse}.json"
        if not path.is_file():
            print(f"[skip] missing {path}")
            continue

        raw = json.loads(path.read_text(encoding="utf-8"))
        merged_info = {**info, **(raw.get("info") or {})}
        if not merged_info.get("application_link"):
            merged_info["application_link"] = info["application_link"]

        config = VLOPSEConfiguration(
            info=PlatformInformation.model_validate(merged_info),
            mappings=raw.get("mappings") or {},
            conditions=raw.get("conditions") or {},
        )
        write_vlopse_configuration_for(vlopse, config)
        print(f"[{vlopse}] restored info: {merged_info.get('application_link')}")


if __name__ == "__main__":
    restore_all()
