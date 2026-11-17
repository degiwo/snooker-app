from datetime import UTC, datetime

from snooker_backend.drills.schemas import DrillCreate, DrillRead


class DrillRepository:
    def __init__(self):
        self._data: dict[int, DrillRead] = {}
        self._next_id: int = 1

    def add(self, drill: DrillCreate) -> DrillRead:
        now = datetime.now(UTC)
        created = DrillRead(
            **drill.model_dump(),
            id=self._next_id,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        self._data[self._next_id] = created
        self._next_id += 1
        return created

    def list_all(self) -> list[DrillRead]:
        return list(self._data.values())


_repository = DrillRepository()


def get_drill_repository() -> DrillRepository:
    return _repository
