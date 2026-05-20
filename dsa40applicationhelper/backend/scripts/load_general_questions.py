"""Load general_questions.csv into dsa_question (full replace).

Usage (from backend/):
    uv run python scripts/load_general_questions.py [path/to/general_questions.csv]

Default path: ../data/general_questions.csv
"""

import csv
import sys
from pathlib import Path

# Allow `uv run python scripts/load_general_questions.py` from backend/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal, init_db
from app.models import DSAQuestion, InputType
from app.services.questions import QuestionService

DEFAULT_CSV = Path(__file__).resolve().parents[2] / "data" / "general_questions.csv"

CSV_TYPE_TO_INPUT: dict[str, InputType] = {
    "free form": InputType.text,
    "selection": InputType.selection,
    "file upload": InputType.file_upload,
    "date-select": InputType.date_select,
    "multi-select": InputType.multi_select,
}

COUNTRY_SHORTHANDS = frozenset({"researcher-addr-country", "org-addr-country"})


def parse_options(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw:
        return []
    if "; " in raw:
        return [part.strip() for part in raw.split("; ") if part.strip()]
    return [part.strip() for part in raw.split(", ") if part.strip()]


def build_config(
    shorthand: str, csv_type: str, input_type: InputType, options: list[str]
) -> dict[str, object] | None:
    if input_type == InputType.ISO_3166_1:
        return {"type": "iso-3166-1"}
    if input_type == InputType.selection and options:
        return {"type": "selection", "options": options}
    if input_type == InputType.multi_select and options:
        return {"type": "selection", "options": options, "multiple": True}
    if csv_type == "selection" and shorthand in COUNTRY_SHORTHANDS:
        return {"type": "iso-3166-1"}
    return None


def csv_row_to_payload(row: dict[str, str]) -> dict[str, object]:
    shorthand = row["shorthand"].strip()
    csv_type = row["type"].strip().lower()
    if csv_type not in CSV_TYPE_TO_INPUT:
        raise ValueError(f"{shorthand}: unknown type {row['type']!r}")

    input_type = CSV_TYPE_TO_INPUT[csv_type]
    options = parse_options(row.get("options") or "")

    if csv_type == "selection" and shorthand in COUNTRY_SHORTHANDS and not options:
        input_type = InputType.ISO_3166_1

    help_text = (row.get("help") or "").strip() or (row.get("comments") or "").strip()
    config = build_config(shorthand, csv_type, input_type, options)

    return {
        "id": shorthand,
        "text": row["question_en"].strip(),
        "input_type": input_type.value,
        "help_text": help_text or None,
        "config": config,
    }


def load_csv(path: Path) -> None:
    init_db()
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    if not rows:
        print(f"No rows in {path}")
        return

    with SessionLocal() as db:
        deleted = db.query(DSAQuestion).delete()
        db.commit()
        print(f"Cleared {deleted} existing DSA question(s)")

    service = QuestionService()
    for row in rows:
        payload = csv_row_to_payload(row)
        service.add_unified(
            id=str(payload["id"]),
            text=str(payload["text"]),
            input_type=str(payload["input_type"]),
            help_text=payload["help_text"],  # type: ignore[arg-type]
            config=payload["config"],  # type: ignore[arg-type]
        )
        print(f"  + {payload['id']}")

    print(f"Loaded {len(rows)} general question(s) from {path}")


def main() -> None:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    if not csv_path.is_file():
        print(f"File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    load_csv(csv_path)


if __name__ == "__main__":
    main()
