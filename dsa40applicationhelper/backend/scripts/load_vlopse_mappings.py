"""Sync platform CSV mappings into backend/app/data/vlopses/*.json.

Reads MAIN_Question, Operation, and Condition from data/<platform>.csv and
replaces mappings + conditions for each platform (keeps info block unchanged).

Conditions are stored keyed by platform question id (e.g. T4), with clause
question_ids referring to other platform questions (e.g. T2, T3). The API
remaps these to general question ids for the unified form.

Usage (from backend/):
    uv run python scripts/load_vlopse_mappings.py [platform ...]

Default platforms: meta, tiktok, youtube, x
"""

import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.conditions_util import parse_condition_clauses
from app.core.config import (
    PlatformInformation,
    VLOPSEConfiguration,
    write_vlopse_configuration_for,
)
from pydantic import ValidationError

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
VLOPSES_DIR = Path(__file__).resolve().parents[1] / "app" / "data" / "vlopses"

DEFAULT_PLATFORMS: dict[str, str] = {
    "meta": "meta.csv",
    "tiktok": "tiktok.csv",
    "youtube": "youtube.csv",
    "x": "x.csv",
}

DEFAULT_MULTI_OPERATOR = "join-paragraph"
PLATFORM_INFO_DEFAULTS_PATH = (
    Path(__file__).resolve().parents[1] / "app" / "data" / "platform_info.json"
)


def load_platform_info_defaults() -> dict[str, dict[str, object]]:
    return json.loads(PLATFORM_INFO_DEFAULTS_PATH.read_text(encoding="utf-8"))


def ensure_platform_info(vlopse: str, config: VLOPSEConfiguration) -> VLOPSEConfiguration:
    """Fill missing info fields from platform_info.json (never drop mappings)."""
    defaults = load_platform_info_defaults().get(vlopse)
    if not defaults:
        return config

    current = config.info.model_dump()
    merged = {**defaults, **current}
    if not merged.get("application_link"):
        merged["application_link"] = defaults["application_link"]
    config.info = PlatformInformation.model_validate(merged)
    return config


def load_vlopse_config(vlopse: str) -> VLOPSEConfiguration:
    config_path = VLOPSES_DIR / f"{vlopse}.json"
    defaults = load_platform_info_defaults().get(vlopse, {})
    try:
        config = VLOPSEConfiguration.model_validate_json(
            config_path.read_text(encoding="utf-8")
        )
    except ValidationError:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        info = {**defaults, **(raw.get("info") or {})}
        if not info.get("application_link"):
            info["application_link"] = defaults.get("application_link", "")
        config = VLOPSEConfiguration(
            info=PlatformInformation.model_validate(info),
            mappings=raw.get("mappings") or {},
            conditions=raw.get("conditions") or {},
        )
    return ensure_platform_info(vlopse, config)


def split_main_question(main: str) -> list[str] | str:
    main = main.strip()
    if not main:
        return ""
    if ", " in main:
        return [p.strip() for p in main.split(", ") if p.strip()]
    if "," in main:
        return [p.strip() for p in main.split(",") if p.strip()]
    return main


def read_platform_rows(csv_path: Path) -> list[dict[str, str]]:
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    header_idx = next((i for i, line in enumerate(lines) if line.startswith("id,")), None)
    if header_idx is None:
        raise ValueError(f"No question table in {csv_path}")
    return list(csv.DictReader(lines[header_idx:]))


def build_mapping_entry(
    src: list[str] | str, operation: str
) -> str | dict[str, object]:
    if isinstance(src, list):
        if len(src) == 1:
            return src[0]
        op = operation or DEFAULT_MULTI_OPERATOR
        if not operation:
            print(f"  [info] Multi-source mapping uses default {DEFAULT_MULTI_OPERATOR!r}")
        return {"src": src, "operation": op}
    if operation:
        return {"src": src, "operation": operation}
    return src


def sync_platform(vlopse: str, csv_path: Path) -> tuple[int, int]:
    config_path = VLOPSES_DIR / f"{vlopse}.json"
    if not config_path.exists():
        raise FileNotFoundError(
            f"Missing {config_path}. Create a vlopse config with an info block first."
        )
    config = load_vlopse_config(vlopse)

    mappings: dict[str, str | dict[str, object]] = {}
    conditions: dict[str, list[dict[str, str]]] = {}

    for row in read_platform_rows(csv_path):
        qid = (row.get("id") or "").strip()
        if not qid or not re.match(r"^[A-Z]\d+$", qid):
            continue

        main = (row.get("MAIN_Question") or "").strip()
        if not main:
            print(f"  [skip] {qid}: no MAIN_Question")
            continue

        operation = (row.get("Operation") or "").strip()
        condition = (row.get("Condition") or "").strip()
        src = split_main_question(main)

        mappings[qid] = build_mapping_entry(src, operation)

        if condition:
            clauses = parse_condition_clauses(condition)
            if clauses:
                conditions[qid] = [
                    {"question_id": platform_id, "operator": "eq", "value": value}
                    for platform_id, value in clauses
                ]
            else:
                print(f"  [warn] {qid}: could not parse condition {condition!r}")

    config.mappings = mappings  # type: ignore[assignment]
    config.conditions = conditions  # type: ignore[assignment]
    config = ensure_platform_info(vlopse, config)
    write_vlopse_configuration_for(vlopse, config)

    print(f"[{vlopse}] Wrote {len(mappings)} mapping(s), {len(conditions)} conditional row(s)")
    return len(mappings), len(conditions)


def main() -> None:
    names = sys.argv[1:] if len(sys.argv) > 1 else list(DEFAULT_PLATFORMS.keys())
    total_m, total_c = 0, 0

    for name in names:
        if name not in DEFAULT_PLATFORMS:
            print(f"Unknown platform {name!r}. Known: {', '.join(DEFAULT_PLATFORMS)}")
            sys.exit(1)
        csv_path = DATA_DIR / DEFAULT_PLATFORMS[name]
        if not csv_path.is_file():
            print(f"File not found: {csv_path}")
            sys.exit(1)
        m, c = sync_platform(name, csv_path)
        total_m += m
        total_c += c

    print(f"Done. {total_m} mappings and {total_c} conditional rows across {len(names)} platform(s).")


if __name__ == "__main__":
    main()
