from unittest.mock import MagicMock

import pytest

from app.models import DSAQuestion, InputType
from app.services import form_engine as form_engine_module
from app.services.form_engine import FormService


@pytest.fixture
def form_service(monkeypatch):
    mock_mapper = MagicMock()
    mock_mapper._map.return_value = {"research-keywords": ["T24", "Y16"]}
    monkeypatch.setattr(
        form_engine_module,
        "QuestionMapper",
        MagicMock(from_vlopse_names=lambda *args, **kwargs: mock_mapper),
    )
    service = FormService()

    def get_vlopse(vlopse_id: str):
        configs = {
            "T24": {"type": "selection", "options": ["Consumer trends", "Algorithm"], "multiple": True},
            "Y16": {
                "type": "selection",
                "options": ["Algorithm", "Astronomical Sciences"],
                "multiple": True,
            },
        }
        if vlopse_id not in configs:
            return None
        row = MagicMock(config=configs[vlopse_id])
        return row

    service.question_service.get = get_vlopse
    return service


def test_compute_options_unions_vlopse_selection_options(form_service):
    question = DSAQuestion(
        id="research-keywords",
        text="Keywords",
        input_type=InputType.multi_select,
        config=None,
    )

    options = form_service.compute_options(question, ["tiktok", "youtube"])

    assert options == ["Consumer trends", "Algorithm", "Astronomical Sciences"]
