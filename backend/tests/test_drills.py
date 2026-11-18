from fastapi.testclient import TestClient

drill = {"name": "Line-up", "attempts": 1, "category": "break_building"}


def test_list_is_empty_initially(client: TestClient) -> None:
    response = client.get("/api/drills")

    assert response.status_code == 200
    assert response.json() == []


def test_create_drill_returns_created_drill(client: TestClient) -> None:
    response = client.post("/api/drills", json=drill)

    assert response.status_code == 201
    body = response.json()
    for key, value in drill.items():
        assert body[key] == value
    assert isinstance(body["id"], int)
    assert body["is_active"] is True
    assert body["created_at"] is not None
    assert body["created_at"] == body["updated_at"]


def test_created_drill_appears_in_list(client: TestClient) -> None:
    created = client.post("/api/drills", json=drill).json()
    response = client.get("/api/drills")

    assert response.json() == [created]


def test_each_drill_gets_its_own_id(client: TestClient) -> None:
    first = client.post("/api/drills", json=drill).json()
    second = client.post("/api/drills", json=drill).json()

    assert first["id"] != second["id"]
