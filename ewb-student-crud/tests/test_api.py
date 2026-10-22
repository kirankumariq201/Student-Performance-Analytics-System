import importlib
from datetime import date
import os

import pytest
from fastapi.testclient import TestClient

@pytest.fixture()
def client(tmp_path, monkeypatch):
    db = tmp_path / "test_students.db"
    monkeypatch.setenv("STUDENT_DB_PATH", str(db))
    import app.main as api
    api.DB_PATH = db
    api.init_db()
    with TestClient(api.app) as test_client:
        yield test_client

def payload(email="maya@example.com"):
    return {"name":"Maya Rao","date_of_birth":"2005-04-12","email":email,
            "phone":"+91 98765 43210","course":"Data Science"}

def test_create_list_get_update_delete(client):
    created = client.post("/students", json=payload())
    assert created.status_code == 201
    student = created.json()
    sid = student["id"]
    assert student["name"] == "Maya Rao"
    assert client.get("/students").json()[0]["id"] == sid
    assert client.get(f"/students/{sid}").status_code == 200
    updated = client.put(f"/students/{sid}", json={"course":"Python"})
    assert updated.status_code == 200
    assert updated.json()["course"] == "Python"
    assert client.delete(f"/students/{sid}").status_code == 204
    assert client.get(f"/students/{sid}").status_code == 404

def test_validation_and_duplicate_email(client):
    assert client.post("/students", json=payload()).status_code == 201
    assert client.post("/students", json=payload()).status_code == 409
    invalid = payload("not-an-email")
    assert client.post("/students", json=invalid).status_code == 422

def test_search_and_missing_record(client):
    client.post("/students", json=payload())
    assert len(client.get("/students?search=Maya").json()) == 1
    assert client.get("/students/999").status_code == 404
    assert client.delete("/students/999").status_code == 404

def test_future_birth_date_rejected(client):
    data = payload()
    data["date_of_birth"] = "2099-01-01"
    assert client.post("/students", json=data).status_code == 422
