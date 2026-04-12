from pycountry import countries

from app.core.mapping import QuestionMapper
from app.core.models import Answer, MappedAnswer, MappingError
from app.core.transform import AnswerTransformer


class FormService:
    def __init__(self) -> None:
        self.question_service = QuestionService()
        pass

    def compute_options(self, question: DSAQuestion, vlopses: list[str]):
        # TODO: think this should go to mapper and check dependent questions
        if question.input_type == InputType.ISO_3166_1:
            return [c.name for c in countries]
        else:
            return None

    def get_required_questions_for(self, vlopses: list[str]):
        # TODO: QuestionMapper should not load questions but receive them
        mapper = QuestionMapper.from_vlopse_names(vlopses)
        qs = mapper.map()
        return qs

    def transform_answers_to_vlopse_answers(
        self, vlopses: list[str], answers: list[Answer]
    ):
        result: list[tuple[str, list[MappedAnswer | MappingError]]] = []
        for klops in vlopses:
            # TODO: AnswerTransformer should not load questions or mappings but receive them
            transformer = AnswerTransformer.from_vlopse_name(klops)
            result.append((klops, transformer.map(answers)))
        return result
