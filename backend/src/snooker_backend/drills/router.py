from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from snooker_backend.drills.repository import (
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
