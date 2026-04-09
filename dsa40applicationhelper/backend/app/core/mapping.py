from typing import Any

from app.core.config import get_vlopse_configuration_for
from app.core.models import PlatformMapping
from app.core.operator import hydrate_operator
from app.core.util import dEBUGLOAD


class QuestionMapper:
    _mapping: dict[str, dict[str, PlatformMapping]]
    questions: Any

    @classmethod
    def from_vlopse_names(cls, vlopses: list[str]):
        mapping = {
            vlopse: get_vlopse_configuration_for(vlopse).mappings for vlopse in vlopses
        }
        return cls(mapping)

    def __init__(self, mapping: dict[str, dict[str, PlatformMapping]]) -> None:
        self._mapping = mapping
        self.questions = dEBUGLOAD()

    def _map(self):
        result = set()
        for vlopse, mapping in self._mapping.items():
            for src, operator in mapping.items():  # FIXME: src name is confusing??
                op = hydrate_operator(operator)
                print(f"FIGURE OUT INPUT FOR {operator} TO GET {src}")
                print(f"=> {op.arguments}")
                for a in op.arguments:
                    result.add(a)

        print(result)
        return result

    def map(self):
        unified_question_ids = self._map()
        # FIXME: this should ask the db

        return [q for q in self.questions if q.id in unified_question_ids]
        result = []
        # op = self._hydrate_operator(operator)
