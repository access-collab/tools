from fastapi.testclient import TestClient
from pytest import fixture

from app.database import Base, engine, init_db
from app.main import app


def _wipe_db():
    Base.metadata.drop_all(bind=engine)


@fixture
def client():
    _wipe_db()
    init_db()
    client = TestClient(app)
    return client


def test_selection_question(client: TestClient):
    question_id = "T2"
    response = client.post(
        "/api/vlopse/tiktok/question",
        json={
            "id": question_id,
            "text": "Are you affiliated with an academic institution or a not-for-profit body, organisation or association whose principal aim is to conduct research on a not-for-profit basis pursuant to a public-interest mission?",
            "required": "true",
            "input_type": {
                "i_type": "selection",
                "options": [
                    "Academic institution",
                    "Not-for-profit body, organization or association (based in the EU 27 Member States only)",
                ],
            },
        },
    )
    assert response.status_code == 200
    response = client.get(f"/api/vlopse/tiktok/question/{question_id}")
    assert response.status_code == 200
    question = response.json()
    assert question["id"] == question_id


def test_post_vlopse():
    response = client.post("/api/vlopse", json={"name": "testing"})
    assert response.status_code == 200
    # Cleanup
    response = client.delete("/api/vlopse/testing")
    assert response.status_code == 200
