import pytest
from fastapi.testclient import TestClient

from app.core.config import ApplicationModality, PlatformInformation
from app.main import app

client = TestClient(app)


def test_get_vlopses():
    response = client.get("/api/vlopse")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


info = PlatformInformation(
    name="testing",
    account_required=True,
    application_link="localhost",
    modality=ApplicationModality.form,
)
info = info.model_dump()


def test_post_vlopse():
    response = client.post("/api/vlopse", json={"id": "testing", "info": info})
    assert response.status_code == 200
    response = client.get("/api/vlopse")
    assert response.status_code == 200
    assert any(v["id"] == "testing" for v in response.json()), (
        "Vlopse should be created"
    )
    # Cleanup
    response = client.delete("/api/vlopse/testing")
    assert response.status_code == 200


def test_post_invalid_vlopse():
    response = client.post("/api/vlopse", json={"heh": True})
    assert response.status_code == 422


def test_post_existant():
    response = client.post("/api/vlopse", json={"id": "testing", "info": info})
    assert response.status_code == 200
    response = client.post("/api/vlopse", json={"id": "testing", "info": info})
    assert response.status_code == 409
    # Cleanup
    response = client.delete("/api/vlopse/testing")
    assert response.status_code == 200


# FIXME
def test_put():
    response = client.post("/api/vlopse", json={"id": "testing", "info": info})
    assert response.status_code == 200

    response = client.put("/api/vlopse/testing", json={"new_name": "new_testing"})
    assert response.status_code == 200
    # Cleanup
    response = client.delete("/api/vlopse/new_testing")
    assert response.status_code == 200


def test_put_non_existant():
    response = client.put("/api/vlopse/testing", json={"new_name": "new_testing"})
    assert response.status_code == 404


def test_put_new_already_exists():
    response = client.post("/api/vlopse", json={"id": "testing", "info": info})
    assert response.status_code == 200
    response = client.post("/api/vlopse", json={"id": "new_testing", "info": info})
    assert response.status_code == 200
    response = client.put("/api/vlopse/testing", json={"new_name": "new_testing"})
    assert response.status_code == 409
    # Cleanup
    response = client.delete("/api/vlopse/testing")
    assert response.status_code == 200
    response = client.delete("/api/vlopse/new_testing")
    assert response.status_code == 200


def test_put_no_name():
    response = client.put("/api/vlopse")
    assert response.status_code == 405


def test_put_no_argument():
    response = client.put("/api/vlopse/testing")
    assert response.status_code == 422


def test_delete():
    response = client.post("/api/vlopse", json={"id": "testing", "info": info})
    assert response.status_code == 200
    response = client.delete("/api/vlopse/testing")
    assert response.status_code == 200


def test_delete_nonexistant():
    response = client.delete("/api/vlopse/idontexist")
    assert response.status_code == 404


@pytest.mark.skip()
def test_get_questions():
    response = client.get("/api/vlopse/meta/questions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
