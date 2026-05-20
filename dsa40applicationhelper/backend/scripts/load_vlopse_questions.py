"""Load platform question CSVs into vlopse_question (per-platform replace).

Usage (from backend/):
    uv run python scripts/load_vlopse_questions.py [--fresh] [platform ...]

Platforms default to meta, tiktok, youtube, x. Each reads ../data/<platform>.csv,
deletes existing rows for that vlopse, then inserts fresh rows.

Use --fresh to delete ALL vlopse_question rows first (recommended when reloading
only these CSVs). Question ids are globally unique in the DB, so leftover rows
from other platforms (e.g. Mastodon also using X1) would otherwise cause conflicts.

No running server required.
"""

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal, init_db
from app.models import InputType, VLOPSEQuestion
from app.services.questions import QuestionService

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

DEFAULT_PLATFORMS: dict[str, str] = {
    "meta": "meta.csv",
    "tiktok": "tiktok.csv",
    "youtube": "youtube.csv",
    "x": "x.csv",
}

CSV_TYPE_TO_INPUT: dict[str, InputType] = {
    "free form": InputType.text,
    "selection": InputType.selection,
    "file upload": InputType.file_upload,
    "date-select": InputType.date_select,
    "multi-select": InputType.multi_select,
}


def parse_options(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw:
        return []
    if "; " in raw:
        return [part.strip() for part in raw.split("; ") if part.strip()]
    return [part.strip() for part in raw.split(", ") if part.strip()]


def build_config(csv_type: str, input_type: InputType, options: list[str]) -> dict[str, object] | None:
    if input_type == InputType.selection and options:
        return {"type": "selection", "options": options}
    if input_type == InputType.multi_select and options:
        return {"type": "selection", "options": options, "multiple": True}
    return None


def parse_required(raw: str) -> bool:
    return raw.strip().upper() == "TRUE"


def combine_details(row: dict[str, str]) -> str | None:
    parts = [(row.get("Details") or "").strip(), (row.get("Comments") or "").strip()]
    parts = [p for p in parts if p]
    return "\n".join(parts) if parts else None


def read_platform_rows(csv_path: Path) -> list[dict[str, str]]:
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    header_idx = next((i for i, line in enumerate(lines) if line.startswith("id,")), None)
    if header_idx is None:
        raise ValueError(f"No question table found in {csv_path}")
    return list(csv.DictReader(lines[header_idx:]))


def csv_row_to_payload(row: dict[str, str], vlopse: str) -> dict[str, object]:
    qid = row["id"].strip()
    csv_type = row["Type"].strip().lower()
    if csv_type not in CSV_TYPE_TO_INPUT:
        raise ValueError(f"{vlopse}/{qid}: unknown type {row['Type']!r}")

    input_type = CSV_TYPE_TO_INPUT[csv_type]
    options = parse_options(row.get("Options") or "")
    config = build_config(csv_type, input_type, options)

    return {
        "id": qid,
        "text": row["Question"].strip(),
        "vlopse": vlopse,
        "required": parse_required(row.get("Required") or "FALSE"),
        "input_type": input_type.value,
        "details": combine_details(row),
        "config": config,
    }


def load_platform(vlopse: str, csv_path: Path) -> int:
    rows = [
        row
        for row in read_platform_rows(csv_path)
        if (row.get("id") or "").strip() and re.match(r"^[A-Z]\d+$", row["id"].strip())
    ]

    with SessionLocal() as db:
        deleted = (
            db.query(VLOPSEQuestion).filter(VLOPSEQuestion.vlopse == vlopse).delete()
        )
        db.commit()
        print(f"[{vlopse}] Cleared {deleted} existing question(s)")

    service = QuestionService()
    for row in rows:
        payload = csv_row_to_payload(row, vlopse)
        service.add(
            id=str(payload["id"]),
            text=str(payload["text"]),
            vlopse=str(payload["vlopse"]),
            required=bool(payload["required"]),
            input_type=str(payload["input_type"]),
            details=payload["details"],  # type: ignore[arg-type]
            config=payload["config"],  # type: ignore[arg-type]
        )
        print(f"  + {payload['id']}")

    print(f"[{vlopse}] Loaded {len(rows)} question(s) from {csv_path.name}")
    return len(rows)


def clear_all_vlopse_questions() -> int:
    with SessionLocal() as db:
        deleted = db.query(VLOPSEQuestion).delete()
        db.commit()
    print(f"Cleared all {deleted} vlopse question(s) in database")
    return deleted


def main() -> None:
    init_db()
    args = sys.argv[1:]
    fresh = False
    if "--fresh" in args:
        fresh = True
        args = [a for a in args if a != "--fresh"]

    names = args if args else list(DEFAULT_PLATFORMS.keys())
    if fresh:
        clear_all_vlopse_questions()

    total = 0

    for name in names:
        if name not in DEFAULT_PLATFORMS:
            known = ", ".join(DEFAULT_PLATFORMS)
            print(f"Unknown platform {name!r}. Known: {known}", file=sys.stderr)
            sys.exit(1)
        csv_path = DATA_DIR / DEFAULT_PLATFORMS[name]
        if not csv_path.is_file():
            print(f"File not found: {csv_path}", file=sys.stderr)
            sys.exit(1)
        total += load_platform(name, csv_path)

    print(f"Done. Loaded {total} platform question(s) across {len(names)} platform(s).")


if __name__ == "__main__":
    main()
