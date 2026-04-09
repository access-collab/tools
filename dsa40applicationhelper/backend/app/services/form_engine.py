from pathlib import Path


from app.models import UnifiedQuestion
from app.services.mapping import (
    get_vlopse_configuration_for,
)

someadapter = TypeAdapter(list[UnifiedQuestion])


_DATA_DIR = Path(__file__).parent.parent / "data"
def find_inputs_for_multiple(candidates: dict[str, Any], keys: list[str]):
    print(f"Finding multiple {keys} in {candidates}")
    return {k: v for k, v in candidates.items() if k in keys}


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
                op = _hydrate_operator(operator)
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
            op = _hydrate_operator(operator)
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


def to_frage(question: UnifiedQuestion, vlopse: str):
    stuff = get_vlopse_configuration_for(vlopse)
    q_id = question.id

    stuff["mapping"]

    # Frage(id=q_id, question.text_en, help_text=question.help_text)
