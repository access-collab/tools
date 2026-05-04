from typing_extensions import override

from app.core.config import get_vlopse_configuration_for
from app.core.models import PlatformMapping, UnifiedQuestion


class Mapping:
    vlopse_id: str
    dsa_ids: list[str]

    def __init__(self, vlopse_id: str, dsa_ids: list[str]) -> None:
        self.vlopse_id = vlopse_id
        self.dsa_ids = dsa_ids

    @override
    def __repr__(self):
        return f"DSA([{''.join(self.dsa_ids)}]) -> VLOPSE({self.vlopse_id})"


def hydrate_mapping(vlopse_question: str, mapping_definition: PlatformMapping):
    if isinstance(mapping_definition, str):
        return Mapping(vlopse_question, [mapping_definition])
    elif isinstance(mapping_definition.src, list):
        return Mapping(vlopse_question, mapping_definition.src)
    elif isinstance(mapping_definition.src, str):
        return Mapping(vlopse_question, [mapping_definition.src])
    raise ValueError(f"Invalid mapping defition {mapping_definition}")


class MappingValidationError(Exception):
    pass


class QuestionMapper:
    _mapping: dict[str, dict[str, PlatformMapping]]
    questions: list[UnifiedQuestion]

    @classmethod
    def from_vlopse_names(cls, vlopses: list[str], questions: list[UnifiedQuestion]):
        mapping = {
            vlopse: get_vlopse_configuration_for(vlopse).mappings for vlopse in vlopses
        }
        return cls(mapping, questions)

    def _validate(self):
        question_ids = [q.id for q in self.questions]
        invalid_mappings: set[Mapping] = set()
        # TODO: Check if a mapping refers to a question not defined by the vlopse
        for vlopse, mappings in self._mapping.items():
            print(f"Validating {vlopse}..")
            for mapping in mappings:
                for u_id in mapping.dsa_ids:
                    if u_id not in question_ids:
                        invalid_mappings.add(mapping)
                        print(
                            f"[WARN] {mapping} for {vlopse} refers to {u_id}, which is undefined!"
                        )

        if len(invalid_mappings):
            msg = f"[ERROR] {len(invalid_mappings)} invalid mappings found.: {invalid_mappings}"
            raise MappingValidationError(msg)

    def __init__(
        self,
        mapping: dict[str, dict[str, PlatformMapping]],
        questions: list[UnifiedQuestion],
    ) -> None:
        self._mapping = mapping
        self.questions = questions

    def _map(self):
        result = set[str]()
        for _, mapping_definitions in self._mapping.items():
            for vlopse_question, operator in mapping_definitions.items():
                mapping = hydrate_mapping(vlopse_question, operator)
                result.update(mapping.dsa_ids)

        return result

    def map_vlopse_to_unified(self):
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
