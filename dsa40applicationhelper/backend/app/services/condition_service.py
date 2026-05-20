from collections import defaultdict

from app.core.conditions_util import platform_conditions_to_general_groups
from app.core.config import get_vlopse_configuration_for
from app.core.models import Condition
from app.services.questions import QuestionService


class ConditionService:
    question_service: QuestionService

    def __init__(self) -> None:
        self.question_service = QuestionService()

    def get_conditions(self, for_vlopses: list[str]):
        return {
            vlopse: get_vlopse_configuration_for(vlopse).conditions
            for vlopse in for_vlopses
        }

    def get_merged_conditions(
        self, for_vlopses: list[str]
    ) -> dict[str, list[list[Condition]]]:
        """General question id → OR of AND-groups for unified-form visibility."""
        merged: dict[str, list[list[Condition]]] = defaultdict(list)
        for vlopse in for_vlopses:
            config = get_vlopse_configuration_for(vlopse)
            groups = platform_conditions_to_general_groups(
                config.mappings, config.conditions
            )
            for general_id, or_groups in groups.items():
                merged[general_id].extend(or_groups)
        return dict(merged)
