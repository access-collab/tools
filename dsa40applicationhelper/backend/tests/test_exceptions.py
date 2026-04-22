import pytest

from app.core.mapping import Mapping
from app.core.models import (
    Answer,
)
from app.core.operator import JoinOperator, MakeISOOperator
from app.core.transform import (
    Transformation,
    TransformationError,
    ValidationErrors,
)


def test_validating_missing_argument():
    mapper = Mapping("V1", ["first-name", "last-name"])
    op = JoinOperator(" ")
    transformation = Transformation(mapper, op)
    with pytest.raises(ValidationErrors) as exc_info:
        transformation.validate_args([Answer(question_id="first-name", value="Joseph")])
    args = exc_info.value.exceptions[0].args[0]

    assert args["message"] == "missing required argument"
    assert args["loc"] == ("last-name",)


def test_transforming_missing_argument():
    mapper = Mapping("V1", ["first-name", "last-name"])
    op = JoinOperator(" ")
    transformation = Transformation(mapper, op)
    with pytest.raises(TransformationError) as exc_info:
        _ = transformation.transform([Answer(question_id="first-name", value=None)])
    exc = exc_info.value
    args = exc.args[0]
    assert args["message"] == "transformation failed"
    assert args["loc"] == ("first-name",)
    assert args["cause"] == "Cannot join None type"


def test_transforming_invalid_argument_type():
    mapper = Mapping("V1", ["first-name", "last-name"])
    op = MakeISOOperator()
    transformation = Transformation(mapper, op)
    with pytest.raises(TransformationError) as exc_info:
        _ = transformation.transform(
            [
                Answer(question_id="first-name", value="Joseph"),
                Answer(question_id="last-name", value="Weizenbaum"),
            ]
        )
    exc = exc_info.value
    args = exc.args[0]
    assert args["message"] == "transformation failed"
    assert args["loc"] == ("first-name", "last-name")
    assert args["cause"] == "Cannot create ISO from list argument."
