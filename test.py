import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def test_token():
    response = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "test",
            "password": "secret",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_anonymize(token):
    print(type(token))
    headers = {"Authorization": "Bearer " + token}
    test_data = {
        "values": ["test1", "test2"],
        "password": "EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    }
    response = client.post("/anonymize", headers=headers, json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert "values" in data
    assert len(data["values"]) == len(test_data["values"])


def test_pseudonymize(token):
    print(type(token))
    headers = {"Authorization": "Bearer " + token}
    test_data = {
        "values": ["test1", "test2"],
        "password": "EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    }
    response = client.post("/pseudonymize", headers=headers, json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert "values" in data
    assert len(data["values"]) == len(test_data["values"])


def test_unpseudonymize(token):
    print(type(token))
    headers = {"Authorization": "Bearer " + token}
    test_data = {
        "values": [
            "0301f20878cb68a850a9b5f041a605e55281ff1fb209ded875d3f0544397bb02f0388b03e6ca20203baec6c5cc9c23f0b667d5f6ddbc5bce75d7a64e99aaeb916992cc141d03b9e3351df3cfac612a4be966"
        ],
        "password": "EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    }
    response = client.post("/unpseudonymize", headers=headers, json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert "values" in data
    assert len(data["values"]) == len(test_data["values"])
