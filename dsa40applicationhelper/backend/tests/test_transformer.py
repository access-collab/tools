import pytest

from app.core.models import Answer, PlatformMapping, PlatformMappingComplex
from app.core.transform import AnswerTransformer

mapping: dict[str, PlatformMapping] = {
    "T1": PlatformMappingComplex(
        src=["first-name", "last-name"], operation="join-space"
    )
}
transformer = AnswerTransformer(mapping)


def test_missing_arguments():
    with pytest.raises(TypeError, match=r"Missing arg.*'last-name'"):
        _ = transformer.map([Answer(question_id="first-name", value="Joseph")])


def test_valid_join_spaces():
    res = transformer.map(
        [
            Answer(question_id="first-name", value="Joseph"),
            Answer(question_id="last-name", value="Weizenbaum"),
        ]
    )
    assert res[0].value == "Joseph Weizenbaum"


@pytest.mark.skip(reason="Not implemented yet")
def test_invalid_arguments():
    with pytest.raises(TypeError, match=r"Missing arg.*'last-name'"):
        res = transformer.map(
            [
                Answer(question_id="first-name", value="Joseph"),
                Answer(question_id="last-name", value=None),
            ]
        )
