import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.skip(reason="endpoint requires full questionaire")
def test_answer_transformation():
    response = client.post(
        "/api/transform?vlopse=tiktok",
        json={
            "answers": [
                {"question_id": "first-name", "value": "Joseph"},
                {"question_id": "last-name", "value": "Weizenbaum"},
                {"question_id": "commercial-purpose", "value": "no"},
            ]
        },
    )
    assert response.status_code == 200
    data = response.json()
    vlopse_answers = data["by_vlopse"][0]
    assert vlopse_answers["name"] == "tiktok"
    answers = vlopse_answers["answers"]
    assert answers[0]["question_id"] == "T1"
    assert answers[0]["value"] == "Joseph Weizenbaum"
