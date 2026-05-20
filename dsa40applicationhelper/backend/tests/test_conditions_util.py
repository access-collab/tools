from app.core.conditions_util import (
    parse_condition_clauses,
    platform_conditions_to_general_groups,
)
from app.core.models import Condition


def test_parse_tiktok_and_condition():
    clauses = parse_condition_clauses(
        "if T2 == Academic institution AND T3 == EEA (European Economic Area), UK, or Switzerland AND T7 == No"
    )
    assert len(clauses) == 3
    assert clauses[0] == ("T2", "Academic institution")
    assert clauses[1][0] == "T3"
    assert "EEA" in clauses[1][1]
    assert clauses[2] == ("T7", "No")


def test_platform_conditions_or_groups_for_country():
    mappings = {
        "T3": "org-addr-country",
        "T4": "org-addr-country",
        "T2": "commercial-purpose",
    }
    platform_conditions = {
        "T3": [
            Condition(question_id="T2", operator="eq", value="Academic institution"),
        ],
        "T4": [
            Condition(question_id="T2", operator="eq", value="Academic institution"),
            Condition(
                question_id="T3", operator="eq", value="US and its territories"
            ),
        ],
    }
    groups = platform_conditions_to_general_groups(mappings, platform_conditions)
    assert "org-addr-country" in groups
    assert len(groups["org-addr-country"]) == 2
    assert groups["org-addr-country"][1][1].question_id == "org-addr-country"
