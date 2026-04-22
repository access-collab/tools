from pydantic import ValidationError

from app.core.mapping import Mapping, hydrate_mapping
from app.core.operator import (
    AbstractOperator,
    hydrate_operator,
)

from .config import get_vlopse_configuration_for
from .models import Answer, MappedAnswer, MappingError, MappingResult, PlatformMapping


class Transformation:
    mapping: Mapping
    operator: AbstractOperator

    def __init__(self, mapping: Mapping, operator: AbstractOperator) -> None:
        self.mapping = mapping
        self.operator = operator
    def validate_args(self, args: list[Answer]):
        missing = [
            dsa_question
            for dsa_question in self.mapping.dsa_ids
            if dsa_question not in [a.question_id for a in args]
        ]

    def transform(self, args: list[Answer]):
            if len(args) == 1:
                result = self.operator.apply(args[0].value)
            else:
                result = self.operator.apply([a.value for a in args])
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

    def transform(
        self, answers: list[Answer], mapper: Mapping, op: AbstractOperator
    ) -> MappingResult:
        transformation = Transformation(mapper, op)

        transformation.validate_args(answers)
        output = transformation.transform(answers)
        answer = MappedAnswer(question_id=mapper.vlopse_id, value=output)

        return answer

    def map(self, answers: list[Answer]):
        answer_map = {a.question_id: a for a in answers}
        result: list[MappingResult] = []
        for vlopse_question, operator in self._mapping.items():
            mapper = hydrate_mapping(vlopse_question, operator)
            op = hydrate_operator(operator)
            if isinstance(operator, str):
                inputs = [answer_map.get(vlopse_question)]
            elif isinstance(operator.src, list):
                inputs = [a for a in answers if a.question_id in operator.src]
            elif isinstance(operator.src, str):
                inputs = [answer_map.get(operator.src)]
            else:
                raise TypeError(f"Unknown operation {operator}")
            output = self.transform_safe(inputs, mapper, op)
            result.append(output)

        return result
