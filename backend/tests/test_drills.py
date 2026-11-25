import pytest
from fastapi.testclient import TestClient

DRILL = {"name": "Line-up", "attempts": 1, "category": "break_building"}


def _drill_create(**overrides: object) -> dict[str, object]:
    return DRILL | overrides


def _drill_update(**overrides: object) -> dict[str, object]:
    return DRILL | {"is_active": True} | overrides


def test_list_is_empty_initially(client: TestClient) -> None:
    response = client.get("/api/drills")

    assert response.status_code == 200
    assert response.json() == []


def test_create_drill_returns_created_drill(client: TestClient) -> None:
    response = client.post("/api/drills", json=_drill_create())

    assert response.status_code == 201
    body = response.json()
    for key, value in _drill_create().items():
        assert body[key] == value
    assert isinstance(body["id"], int)
    assert body["is_active"] is True
    assert body["created_at"] is not None
    assert body["created_at"] == body["updated_at"]


def test_created_drill_appears_in_list(client: TestClient) -> None:
    created = client.post("/api/drills", json=_drill_create()).json()
    response = client.get("/api/drills")

    assert response.json() == [created]


def test_name_is_trimmed(client: TestClient) -> None:
    response = client.post("/api/drills", json=_drill_create(name="   Line-Up    "))

    assert response.json()["name"] == "Line-Up"


def test_each_drill_gets_its_own_id(client: TestClient) -> None:
    first = client.post("/api/drills", json=_drill_create()).json()
    second = client.post("/api/drills", json=_drill_create(name="Another drill")).json()

    assert first["id"] != second["id"]


def test_duplicate_name_is_rejected_case_insensitive(client: TestClient) -> None:
    client.post("/api/drills", json=_drill_create())
    response = client.post("/api/drills", json=_drill_create(name="LINE-UP"))

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
    response = client.post("/api/drills", json=_drill_create(**overrides))

    assert response.status_code == 422


def test_get_drill_by_id(client: TestClient) -> None:
    created = client.post("/api/drills", json=_drill_create()).json()
    response = client.get(f"/api/drills/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_unknown_drill_returns_404(client: TestClient) -> None:
    assert client.get("/api/drills/999").status_code == 404


@pytest.mark.parametrize(
    "change",
    [
        {"name": "New Name"},
        {"setup": "new setup"},
        {"attempts": 5},
        {"max_points_per_attempt": 10},
        {"category": "safety"},
        {"is_active": False},
    ],
)
def test_update_replaces_fields(client: TestClient, change: dict[str, object]) -> None:
    created = client.post("/api/drills", json=_drill_create()).json()
    assert all(created[key] != value for key, value in change.items())

    response = client.put(f"/api/drills/{created['id']}", json=_drill_update(**change))

    assert response.status_code == 200
    body = response.json()
    assert client.get(f"/api/drills/{created['id']}").json() == body
    assert body == created | change | {"updated_at": body["updated_at"]}


def test_update_unknown_drill_returns_404(client: TestClient) -> None:
    assert client.put("/api/drills/999", json=_drill_update()).status_code == 404


def test_update_drill_with_existing_name_returns_409(client: TestClient) -> None:
    first = client.post("/api/drills", json=_drill_create(name="first")).json()
    second = client.post("/api/drills", json=_drill_create(name="second")).json()

    response = client.put(f"/api/drills/{first['id']}", json=_drill_update(name=second["name"]))

    assert response.status_code == 409


def test_update_can_change_case_of_own_name(client: TestClient) -> None:
    created = client.post("/api/drills", json=_drill_create(name="mydrill")).json()

    response = client.put(f"/api/drills/{created['id']}", json=_drill_update(name="MYDRILL"))

    assert response.status_code == 200
    assert response.json()["name"] == "MYDRILL"


def test_reactivate_inactive_drill(client: TestClient) -> None:
    created = client.post("/api/drills", json=_drill_create()).json()
    inactive = client.put(f"/api/drills/{created['id']}", json=_drill_update(is_active=False))

    assert inactive.status_code == 200
    assert inactive.json()["is_active"] is False

    reactivated = client.put(f"/api/drills/{created['id']}", json=_drill_update(is_active=True))
    assert reactivated.json()["is_active"] is True
