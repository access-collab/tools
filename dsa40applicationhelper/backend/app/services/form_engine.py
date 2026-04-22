from pycountry import countries

from app.core.mapping import QuestionMapper
from app.core.models import (
    Answer,
    MappingError,
    MappingResult,
)
from app.core.transform import AnswerTransformer
from app.models import DSAQuestion, InputType, VLOPSEQuestion
from app.services.questions import QuestionService


class AnswerToUnknownQuestion(BaseException):
    pass


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

    def validate_vlopse_question(self, question: VLOPSEQuestion, answer: Answer): ...
    def map_unified_to_vlopse_and_validate(
        self, answers: list[Answer], vlopses: list[str]
    ):
        unified = self.question_service.get_all_unified_for(
            [a.question_id for a in answers]
        )
        mapper = QuestionMapper.from_vlopse_names(vlopses, unified)
        print(f"Mapping {answers} to {unified}..")
        qs = mapper.map()
        print(f"Mapped {qs} for {vlopses}")
        for q in qs:
            print(q)
        return []

    def validate_unified_question(self, answers: list[Answer]):
        result = {}
        unifieds = self.question_service.get_all_unified()
        for a in answers:
            qs = [q for q in unifieds if q.id == a.question_id]

            if not len(qs):
                raise AnswerToUnknownQuestion(f"{a.question_id} not defined!")
            q = qs[0]
            if a.value is None or a.value == "":
                result[q.id] = "None or empty string not allowed"
                continue
            config = q.parsed_config
            if config:
                error = config.validate_answer(a.value)
                if error:
                    result[q.id] = error
        return result

    def get_required_questions_for(self, vlopses: list[str]):
        all_questions = self.question_service.get_all_unified()
        # TODO: QuestionMapper should not load questions but receive them
        mapper = QuestionMapper.from_vlopse_names(vlopses, all_questions)
        qs = mapper.map()
        print(f"Mapped {qs} for {vlopses}")
        return qs

    def enhance_with_text(self, val: MappingError | MappingResult):
        q = self.question_service.get(val.question_id)
        if q:
            text = str(q.text)
        else:
            text = "N/A"
        v = val.model_dump()
        v["text"] = text
        return v

    def transform_answers_to_vlopse_answers(
        self, vlopses: list[str], answers: list[Answer]
    ):
        result = []
        for klops in vlopses:
            # TODO: should not load questions or mappings but receive them
            transformer = AnswerTransformer.from_vlopse_name(klops)
            transformed = [self.enhance_with_text(t) for t in transformer.map(answers)]
            result.append((klops, transformed))
        return result
