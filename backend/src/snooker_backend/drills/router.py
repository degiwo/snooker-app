from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from snooker_backend.drills.repository import (
    DrillNotFoundError,
    DrillRepository,
    DuplicateDrillNameError,
    get_drill_repository,
)
from snooker_backend.drills.schemas import DrillCreate, DrillRead

router = APIRouter(prefix="/drills", tags=["drills"])
RepositoryDep = Annotated[DrillRepository, Depends(get_drill_repository)]


@router.get("")
def list_drills(repo: RepositoryDep) -> list[DrillRead]:
    return repo.list_all()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_drill(drill: DrillCreate, repo: RepositoryDep) -> DrillRead:
    try:
        return repo.add(drill)
    except DuplicateDrillNameError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="A drill with this name already exists."
        ) from None


@router.get("/{drill_id}")
def get_drill(drill_id: int, repo: RepositoryDep) -> DrillRead:
    try:
        return repo.get(drill_id)
    except DrillNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="A drill with this id does not exist."
        ) from None


@router.put("/{drill_id}")
def update_drill(drill_id: int, drill: DrillCreate, repo: RepositoryDep) -> DrillRead:
    try:
        return repo.update(drill_id, drill)
    except DrillNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="A drill with this id does not exist."
        ) from None
