import pytest

from app.services.form_engine import Answer, AnswerTransformer
from app.services.mapping import PlatformMapping, PlatformMappingComplex

mapping: dict[str, PlatformMapping] = {
    "T1": PlatformMappingComplex(
        src=["first-name", "last-name"], operation="join-space"
    )
}
transformer = AnswerTransformer(mapping)


def test_missing_arguments():
    with pytest.raises(TypeError, match=r"Missing arg.*'last-name'"):
        _ = transformer.map([Answer(question_id="first-name", value="Loiz")])


def test_valid_join_spaces():
    res = transformer.map(
        [
            Answer(question_id="first-name", value="Loiz"),
            Answer(question_id="last-name", value="Ziegler"),
        ]
    )
    assert res[0].value == "Loiz Ziegler"


# def test_invalid_arguments():
#
#     with pytest.raises(TypeError, match=r"Missing arg.*'last-name'"):
#         res = mapper.map([Answer(question_id="first-name", value="Loiz"), Answer(question_id="last-name", value=)])
