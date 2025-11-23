import json
from pathlib import Path

import pytest

from server import app


@pytest.fixture(scope="session")
def client():
    app.testing = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(scope="session")
def sample_state():
    sample_path = Path(__file__).resolve().parent / "fixtures/json/sample-state.json"
    with sample_path.open() as f:
        return json.load(f)


def test_root_returns_configured_snake_details(client):
    response = client.get("/")
    assert response.status_code == 200

    data = response.get_json()
    assert data["color"] == "#3d3172"
    assert data["head"] == "trans-rights-scarf"
    assert data["tail"] == "mouse"
    assert data["apiversion"] == "1"
    assert "version" in data


def test_start_and_end_routes_acknowledge_requests(client):
    assert client.post("/start", json={"game": {}, "turn": 0, "board": {}, "you": {}}).status_code == 204
    assert client.post("/end", json={"game": {}, "turn": 0, "board": {}, "you": {}}).status_code == 204


def test_move_returns_valid_direction(client, sample_state):
    response = client.post("/move", json=sample_state)
    assert response.status_code == 200

    payload = response.get_json()
    assert payload["move"] in {"up", "down", "left", "right"}
