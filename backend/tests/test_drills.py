import pytest
from fastapi.testclient import TestClient


def _drill(**overrides: object) -> dict[str, object]:
    return {"name": "Line-up", "attempts": 1, "category": "break_building"} | overrides


def test_list_is_empty_initially(client: TestClient) -> None:
    response = client.get("/api/drills")

    assert response.status_code == 200
    assert response.json() == []


def test_create_drill_returns_created_drill(client: TestClient) -> None:
    response = client.post("/api/drills", json=_drill())

    assert response.status_code == 201
    body = response.json()
    for key, value in _drill().items():
        assert body[key] == value
    assert isinstance(body["id"], int)
    assert body["is_active"] is True
    assert body["created_at"] is not None
    assert body["created_at"] == body["updated_at"]


def test_created_drill_appears_in_list(client: TestClient) -> None:
    created = client.post("/api/drills", json=_drill()).json()
    response = client.get("/api/drills")

    assert response.json() == [created]


def test_name_is_trimmed(client: TestClient) -> None:
    response = client.post("/api/drills", json=_drill(name="   Line-Up    "))

    assert response.json()["name"] == "Line-Up"


def test_each_drill_gets_its_own_id(client: TestClient) -> None:
    first = client.post("/api/drills", json=_drill()).json()
    second = client.post("/api/drills", json=_drill(name="Another drill")).json()

    assert first["id"] != second["id"]


def test_duplicate_name_is_rejected_case_insensitive(client: TestClient) -> None:
    client.post("/api/drills", json=_drill())
    response = client.post("/api/drills", json=_drill(name="LINE-UP"))

    assert response.status_code == 409


@pytest.mark.parametrize(
    "overrides",
    [
        {"name": ""},
        {"name": "   "},
        {"name": 101 * "x"},
        {"setup": 2001 * "x"},
        {"attempts": 0},
        {"attempts": -1},
        {"attempts": None},
        {"max_points_per_attempt": 0},
        {"max_points_per_attempt": -1},
        {"category": "unknown"},
    ],
)
def test_invalid_drill_is_rejected(client: TestClient, overrides: dict[str, object]) -> None:
    response = client.post("/api/drills", json=_drill(**overrides))

    assert response.status_code == 422


def test_get_drill_by_id(client: TestClient) -> None:
    created = client.post("/api/drills", json=_drill()).json()
    response = client.get(f"/api/drills/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_unkown_drill_returns_404(client: TestClient) -> None:
    assert client.get("/api/drills/999").status_code == 404


@pytest.mark.parametrize(
    "change",
    [
        {"name": "New Name"},
        {"setup": "new setup"},
        {"attempts": 5},
        {"max_points_per_attempt": 10},
        {"category": "safety"},
    ],
)
def test_update_replaces_fields(client: TestClient, change: dict[str, object]) -> None:
    created = client.post("/api/drills", json=_drill()).json()
    assert all(created[key] != value for key, value in change.items())

    response = client.put(f"/api/drills/{created['id']}", json=_drill(**change))

    assert response.status_code == 200
    body = response.json()
    assert client.get(f"/api/drills/{created['id']}").json() == body
    assert body == created | change | {"updated_at": body["updated_at"]}


def test_update_unkown_drill_returns_404(client: TestClient) -> None:
    assert client.put("/api/drills/999", json=_drill()).status_code == 404
