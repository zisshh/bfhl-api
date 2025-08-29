import os
from fastapi.testclient import TestClient

from app.main import app


def _set_env_defaults():
    os.environ["BFHL_FULL_NAME"] = "john_doe"
    os.environ["BFHL_DOB_DDMMYYYY"] = "17091999"
    os.environ["BFHL_EMAIL"] = "john@xyz.com"
    os.environ["BFHL_ROLL_NUMBER"] = "ABCD123"


def test_example_a():
    _set_env_defaults()
    client = TestClient(app)
    payload = {"data": ["a", "1", "334", "4", "R", "$"]}
    resp = client.post("/bfhl", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data == {
        "is_success": True,
        "user_id": "john_doe_17091999",
        "email": "john@xyz.com",
        "roll_number": "ABCD123",
        "odd_numbers": ["1"],
        "even_numbers": ["334", "4"],
        "alphabets": ["A", "R"],
        "special_characters": ["$"],
        "sum": "339",
        "concat_string": "Ra",
    }


def test_example_b():
    _set_env_defaults()
    client = TestClient(app)
    payload = {"data": ["2", "a", "y", "4", "&", "-", "*", "5", "92", "b"]}
    resp = client.post("/bfhl", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data == {
        "is_success": True,
        "user_id": "john_doe_17091999",
        "email": "john@xyz.com",
        "roll_number": "ABCD123",
        "odd_numbers": ["5"],
        "even_numbers": ["2", "4", "92"],
        "alphabets": ["A", "Y", "B"],
        "special_characters": ["&", "-", "*"],
        "sum": "103",
        "concat_string": "ByA",
    }


def test_example_c():
    _set_env_defaults()
    client = TestClient(app)
    payload = {"data": ["A", "ABcD", "DOE"]}
    resp = client.post("/bfhl", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data == {
        "is_success": True,
        "user_id": "john_doe_17091999",
        "email": "john@xyz.com",
        "roll_number": "ABCD123",
        "odd_numbers": [],
        "even_numbers": [],
        "alphabets": ["A", "ABCD", "DOE"],
        "special_characters": [],
        "sum": "0",
        "concat_string": "EoDdCbAa",
    }


def test_empty_data():
    _set_env_defaults()
    client = TestClient(app)
    payload = {"data": []}
    resp = client.post("/bfhl", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_success"] is True
    assert data["odd_numbers"] == []
    assert data["even_numbers"] == []
    assert data["alphabets"] == []
    assert data["special_characters"] == []
    assert data["sum"] == "0"
    assert data["concat_string"] == ""


def test_invalid_request_format():
    _set_env_defaults()
    client = TestClient(app)
    # Missing "data" field
    payload = {"invalid": ["a", "1"]}
    resp = client.post("/bfhl", json=payload)
    assert resp.status_code == 422  # FastAPI validation error

