from datetime import UTC, datetime

from snooker_backend.drills.schemas import DrillCreate, DrillRead


class DuplicateDrillNameError(Exception):
    """A drill with the same name (case-insensitive) already exists."""


class DrillNotFoundError(Exception):
    """The requested drill cannot be found."""


class DrillRepository:
    def __init__(self):
        self._data: dict[int, DrillRead] = {}
        self._next_id: int = 1

    def add(self, drill: DrillCreate) -> DrillRead:
        if self._name_exists(drill.name):
            raise DuplicateDrillNameError(drill.name)

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

    def get(self, drill_id: int) -> DrillRead:
        if drill_id not in self._data:
            raise DrillNotFoundError

        return self._data[drill_id]

    def update(self, drill_id: int, drill: DrillCreate) -> DrillRead:
        existing = self.get(drill_id)

        if self._name_exists(drill.name, exclude_id=drill_id):
            raise DuplicateDrillNameError(drill.name)

        updated = DrillRead(
            **drill.model_dump(),
            id=existing.id,
            is_active=existing.is_active,
            created_at=existing.created_at,
            updated_at=datetime.now(UTC),
        )
        self._data[drill_id] = updated
        return updated

    def _name_exists(self, name: str, exclude_id: int | None = None) -> bool:
        key = name.casefold()
        return any(d.name.casefold() == key for d in self._data.values() if d.id != exclude_id)


_repository = DrillRepository()


def get_drill_repository() -> DrillRepository:
    return _repository
