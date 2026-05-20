"""Parse platform form conditions and expose them on general question ids."""

import re
from collections import defaultdict

from app.core.models import Condition, PlatformMapping

_CONDITION_CLAUSE = re.compile(
    r"([A-Z]\d+)\s*==\s*(.+?)(?=\s+(?:AND|&&)\s+[A-Z]\d+\s*==|$)",
    re.IGNORECASE,
)

# CSV condition typos → platform option text (TikTok and shared forms).
_VALUE_ALIASES: dict[str, str] = {
    "Academic Institute": "Academic institution",
    "Student": "Research student",
    "US": "US and its territories",
    "EEA": "EEA (European Economic Area), UK, or Switzerland",
}


def parse_condition_clauses(condition: str) -> list[tuple[str, str]]:
    """Return (platform_question_id, value) pairs from a platform Condition cell."""
    condition = condition.strip()
    if not condition:
        return []
    if condition.lower().startswith("if "):
        condition = condition[3:].strip()
    clauses: list[tuple[str, str]] = []
    for match in _CONDITION_CLAUSE.finditer(condition):
        platform_id, raw_value = match.group(1).upper(), match.group(2).strip()
        value = _VALUE_ALIASES.get(raw_value, raw_value)
        clauses.append((platform_id, value))
    return clauses


def mapping_target(mappings: dict[str, PlatformMapping], platform_id: str) -> str | None:
    """General question shorthand that a platform question maps to."""
    entry = mappings.get(platform_id)
    if entry is None:
        return None
    if isinstance(entry, str):
        return entry
    src = entry.src
    if isinstance(src, list):
        return src[0] if src else None
    return src


def remap_clause_to_general(
    mappings: dict[str, PlatformMapping],
    platform_id: str,
    value: str,
) -> Condition | None:
    general_id = mapping_target(mappings, platform_id)
    if general_id is None:
        return None
    return Condition(question_id=general_id, operator="eq", value=value)


def platform_conditions_to_general_groups(
    mappings: dict[str, PlatformMapping],
    platform_conditions: dict[str, list[Condition]],
) -> dict[str, list[list[Condition]]]:
    """Map platform-keyed AND-clauses to general ids; OR multiple clauses per general field."""
    by_general: dict[str, list[list[Condition]]] = defaultdict(list)

    for platform_qid, raw_clauses in platform_conditions.items():
        general_target = mapping_target(mappings, platform_qid)
        if general_target is None:
            continue
        group: list[Condition] = []
        for clause in raw_clauses:
            if isinstance(clause, Condition):
                remapped = remap_clause_to_general(
                    mappings, clause.question_id, clause.value
                )
            else:
                remapped = remap_clause_to_general(
                    mappings, clause["question_id"], clause["value"]
                )
            if remapped:
                group.append(remapped)
        if group:
            by_general[general_target].append(group)

    return dict(by_general)


def parse_row_condition(
    mappings: dict[str, PlatformMapping], condition: str
) -> list[Condition]:
    """Parse a CSV Condition cell into remapped general Condition objects."""
    group: list[Condition] = []
    for platform_id, value in parse_condition_clauses(condition):
        remapped = remap_clause_to_general(mappings, platform_id, value)
        if remapped:
            group.append(remapped)
    return group
