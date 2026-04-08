from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.routers.form import AnswerRequest
from app.services.form_engine import Answer

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "db": "ok",
        "api": "ok",
    }


def test_questions_no_vlopse_selected():
    response = client.get("/api/questions")
    assert response.status_code == 422


def test_transformation_wo_questions_wo_vlopses():
    response = client.post("/api/transform")
    assert response.status_code == 422


def test_transformation_wo_questions():
    response = client.post("/api/transform?vlopse=tiktok&vlopse=meta")
    assert response.status_code == 422


@pytest.mark.skip(reason="Not implemented yet")
def test_transformation_id_not_in_all_targets():
    # FIXME: first-name will be in all probably, so find another one
    answers = AnswerRequest(answers=[Answer(question_id="first-name", value="Joseph")])

    response = client.post(
        "/api/transform?vlopse=tiktok&vlopse=meta", json=answers.model_dump()
    )
    assert response.status_code == 200
    response = response.json()
    print(response)


@pytest.mark.skip(reason="Not implemented yet")
def test_transformation_invalid_id():
    # FIXME: first-name will be in all probably, so find another one
    answers = AnswerRequest(answers=[Answer(question_id="doesntexist", value="Joseph")])

    response = client.post(
        "/api/transform?vlopse=tiktok&vlopse=meta", json=answers.model_dump()
    )
    assert response.status_code == 322  # FIXME


@pytest.mark.skip(reason="Not implemented yet")
def test_transformation_invalid_vlopse():
    # FIXME: first-name will be in all probably, so find another one
    answers = AnswerRequest(answers=[Answer(question_id="first-name", value="Joseph")])

    response = client.post(
        "/api/transform?vlopse=deadlock&vlopse=meta", json=answers.model_dump()
    )
    assert response.status_code == 322  # FIXME
