from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from snooker_backend.drills.repository import DrillRepository, get_drill_repository
from snooker_backend.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    repository = DrillRepository()
    app.dependency_overrides[get_drill_repository] = lambda: repository
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
