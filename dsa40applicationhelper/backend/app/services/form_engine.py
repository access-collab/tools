from pycountry import countries

from app.core.mapping import QuestionMapper
from app.core.models import (
    Answer,
    ErrorDetails,
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
        # unified = self.question_service.get_all_unified_for(
        #     [a.question_id for a in answers]
        # )
        ok = True
        errors: dict[str, list[ErrorDetails]] = {}
        for klops in vlopses:
            # TODO: should not load questions or mappings but receive them
            transformer = AnswerTransformer.from_vlopse_name(klops)
            transformed = transformer.map(answers)
            # for t in transformed:
            # if isinstance(t, MappingError):
            #     message =
            if any(isinstance(t, MappingError) for t in transformed):
                ok = False
                for t in transformed:
                    if isinstance(t, MappingError):
                        errors[t.question_id] = t.errors
            # result.append((klops, transformed))

        return ok, errors

    def validate_unified_question(self, answers: list[Answer], vlopses: list[str]):
        result: dict[str, str] = {}
        mapper = QuestionMapper.from_vlopse_names(vlopses, self.question_service)
        mapped = mapper.map_vlopse_to_unified()

        for a in answers:
            # TODO: this should ask the db seperately.
            qs = [(req, q) for req, q in mapped if q.id == a.question_id]

            if not len(qs):
                raise AnswerToUnknownQuestion(f"{a.question_id} not defined!")
            is_required, q = qs[0]

            if is_required and (a.value is None or a.value == ""):
                result[q.id] = "None or empty string not allowed"
                continue
            config = q.parsed_config

            if config and a.value is not None:
                error = config.validate_answer(a.value)
                if error:
                    result[q.id] = error
        return result

    def get_mapped_questions_for(self, vlopses: list[str]):
        all_questions = self.question_service.get_all_unified()
        # FIXME: Question mapper should just build a mapping and provide traces, can be annotated in a amapper service later. this form engine is way too huge anyhow
        mapper = QuestionMapper.from_vlopse_names(vlopses, self.question_service)
        qs = mapper.map_vlopse_to_unified()
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
