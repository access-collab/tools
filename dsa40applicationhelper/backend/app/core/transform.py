from pydantic import ValidationError

from .config import (
    get_vlopse_configuration_for
)
from .models import (
    PlatformMapping
)
from app.core.operator import hydrate_operator
from app.core.util import find_inputs_for_multiple


class AnswerTransformer:
    _mapping: dict[str, PlatformMapping]

    @classmethod
    def from_vlopse_name(cls, vlopse: str):
        mapping = get_vlopse_configuration_for(vlopse).mappings
        return cls(mapping)

    def __init__(self, mapping: dict[str, PlatformMapping]) -> None:
        self._mapping = mapping

    def _get_mapping_operator(self, id: str):
        operator = self._mapping.get(id)
        return operator

    def apply_operator(self, operator: Operator[A, B], inputs: A) -> B:
        print(f"{operator}({inputs})")
        return operator.apply(inputs)
        return None

    def map(self, answers: list[Answer]):
        answer_map = {a.question_id: a.value for a in answers}
        result: list[MappedAnswer | MappingError] = []
        for src, operator in self._mapping.items():  # FIXME: src name is confusing??
            print(f"FIGURE OUT INPUT FOR {operator} TO GET {src}")
            op = hydrate_operator(operator)
            if isinstance(operator, str):
                inputs = answer_map.get(src)
            elif isinstance(operator.src, list):
                inputs = find_inputs_for_multiple(answer_map, operator.src)
            elif isinstance(operator.src, str):
                inputs = answer_map.get(operator.src)

            else:
                print(f"Unknown operation {operator}")
                raise TypeError()
            print(f"SOLUTION CANDIDATE {inputs}")
            output = self.apply_operator(op, inputs)
            try:
                answer = MappedAnswer(question_id=src, value=output)
            except ValidationError as e:
                answer = MappingError(question_id=src, errors=e.errors())
            result.append(answer)
        print(f"MAPPED RESULT: {result}")

        return result
