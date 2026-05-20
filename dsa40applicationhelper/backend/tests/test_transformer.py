from app.core.models import (
    Answer,
    MappedAnswer,
    MappingError,
    PlatformMapping,
    PlatformMappingComplex,
)
from app.core.transform import AnswerTransformer

mapping: dict[str, PlatformMapping] = {
    "T1": PlatformMappingComplex(
        src=["first-name", "last-name"], operation="join-space"
    )
}
transformer = AnswerTransformer(mapping)


def test_invalid_argument():
    mapping: dict[str, PlatformMapping] = {
        "T1": PlatformMappingComplex(src="first-name", operation="join-space")
    }
    transformer = AnswerTransformer(mapping)
    res = transformer.map(
        [
            Answer(question_id="first-name", value="Joseph"),
        ]
    )

    err: MappingError = res[0]
    assert err.errors
    assert err.errors[0].loc == ["first-name", "T1"]
    # TODO: error should be more specific
    assert err.errors[0].message == "transformation failed"
    # assert res[0].value == "Joseph Weizenbaum"


def test_missing_argument():
    mapping: dict[str, PlatformMapping] = {
        "T1": PlatformMappingComplex(
            src=["first-name", "last-name"], operation="join-space"
        )
    }
    transformer = AnswerTransformer(mapping)
    res = transformer.map(
        [
            Answer(question_id="first-name", value="Joseph"),
        ]
    )

    err: MappingError = res[0]
    assert err.errors
    assert err.errors[0].loc == ["T1", "last-name"]
    assert err.errors[0].message == "missing required argument"
    # assert res[0].value == "Joseph Weizenbaum"


def test_invalid_value():
    mapping: dict[str, PlatformMapping] = {
        "T1": PlatformMappingComplex(
            src=["first-name", "last-name"], operation="join-space"
        )
    }
    transformer = AnswerTransformer(mapping)
    res = transformer.map(
        [
            Answer(question_id="first-name", value="Joseph"),
            Answer(question_id="last-name", value=None),
        ]
    )

    err = res[0]
    assert isinstance(err, MappingError)
    assert err.errors
    # TODO: loc should be only last-name
    assert err.errors[0].loc == ["first-name", "last-name", "T1"]
    # TODO: error should be more specific
    assert err.errors[0].message == "transformation failed"
    # assert res[0].value == "Joseph Weizenbaum"


def test_valid_join_spaces():
    mapping: dict[str, PlatformMapping] = {
        "T1": PlatformMappingComplex(
            src=["first-name", "last-name"], operation="join-space"
        )
    }
    transformer = AnswerTransformer(mapping)
    res = transformer.map(
        [
            Answer(question_id="first-name", value="Joseph"),
            Answer(question_id="last-name", value="Weizenbaum"),
        ]
    )

    res = res[0]
    assert isinstance(res, MappedAnswer)

    assert res.value == "Joseph Weizenbaum"


def test_valid_make_iso():
    mapping: dict[str, PlatformMapping] = {
        "T1": PlatformMappingComplex(src="country", operation="make-iso")
    }
    transformer = AnswerTransformer(mapping)
    res = transformer.map(
        [
            Answer(question_id="country", value="Germany"),
        ]
    )

    res = res[0]
    assert isinstance(res, MappedAnswer)

    assert res.value == "DEU"


def test_join_paragraph():
    mapping = {
        "X8": PlatformMappingComplex(
            src=["research-title", "research-summary"],
            operation="join-paragraph",
        )
    }
    transformer = AnswerTransformer(mapping)
    res = transformer.map(
        [
            Answer(question_id="research-title", value="My study"),
            Answer(question_id="research-summary", value="We examine trends."),
        ]
    )
    assert isinstance(res[0], MappedAnswer)
    assert res[0].value == "My study\n\nWe examine trends."


def test_join_date_range():
    mapping = {
        "X10": PlatformMappingComplex(
            src=["data-acc-start", "data-acc-end"],
            operation="join-date-range",
        )
    }
    transformer = AnswerTransformer(mapping)
    res = transformer.map(
        [
            Answer(question_id="data-acc-start", value="2024-01-01"),
            Answer(question_id="data-acc-end", value="2025-06-30"),
        ]
    )
    assert isinstance(res[0], MappedAnswer)
    assert res[0].value == "2024-01-01 to 2025-06-30"


def test_make_duration_bucket():
    mapping = {
        "Y19": PlatformMappingComplex(
            src=["tom-storage-start", "tom-storage-end"],
            operation="make-duration",
        )
    }
    transformer = AnswerTransformer(mapping)
    res = transformer.map(
        [
            Answer(question_id="tom-storage-start", value="2024-01-01"),
            Answer(question_id="tom-storage-end", value="2024-01-20"),
        ]
    )
    assert isinstance(res[0], MappedAnswer)
    assert res[0].value == "1 - 4 weeks"


def test_make_report():
    mapping = {
        "T31": PlatformMappingComplex(
            src=["research-summary", "research-sysrisk"],
            operation="make-report",
        )
    }
    transformer = AnswerTransformer(mapping)
    res = transformer.map(
        [
            Answer(question_id="research-summary", value="Overview."),
            Answer(question_id="research-sysrisk", value="Art. 34(1) alignment."),
        ]
    )
    assert isinstance(res[0], MappedAnswer)
    assert "Overview." in res[0].value
    assert "Art. 34(1)" in res[0].value


def test_invalid_make_iso():
    mapping: dict[str, PlatformMapping] = {
        "T1": PlatformMappingComplex(src="country", operation="make-iso")
    }
    transformer = AnswerTransformer(mapping)
    res = transformer.map(
        [
            Answer(question_id="country", value="German"),
        ]
    )

    err = res[0]
    assert isinstance(err, MappingError)
    assert err.errors
    # TODO: loc should be only last-name
    assert err.errors[0].loc == ["country", "T1"]
    # TODO: error should be more specific
    assert err.errors[0].message == "transformation failed"
    # assert res[0].value == "Joseph Weizenbaum"
