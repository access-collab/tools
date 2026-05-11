from collections import defaultdict

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

    def get_merged_conditions(self, for_vlopses: list[str]):
        merged: dict[str, list[Condition]] = defaultdict(list)
        for conditions in self.get_conditions(for_vlopses).values():
            for target_id, conds in conditions.items():
                merged[target_id].extend(conds)
        return merged
