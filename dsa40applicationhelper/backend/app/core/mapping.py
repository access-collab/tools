from app.core.config import get_vlopse_configuration_for
from app.core.models import PlatformMapping, UnifiedQuestion
from app.core.operator import hydrate_operator


class QuestionMapper:
    _mapping: dict[str, dict[str, PlatformMapping]]
    questions: list[UnifiedQuestion]

    @classmethod
    def from_vlopse_names(cls, vlopses: list[str], questions: list[UnifiedQuestion]):
        mapping = {
            vlopse: get_vlopse_configuration_for(vlopse).mappings for vlopse in vlopses
        }
        return cls(mapping, questions)

    def __init__(
        self,
        mapping: dict[str, dict[str, PlatformMapping]],
        questions: list[UnifiedQuestion],
    ) -> None:
        self._mapping = mapping
        self.questions = questions

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
        print(f"Mapping to {unified_question_ids}")
        # FIXME: this should ask the db
        result: list[UnifiedQuestion] = []
        for q in self.questions:
            if q.id not in unified_question_ids:
                print(f"WARNING {q.id} not MAPPED TO ANYTHING")
            else:
                result.append(q)

        return result
        result = []
        # op = self._hydrate_operator(operator)
