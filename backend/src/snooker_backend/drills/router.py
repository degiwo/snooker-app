from typing import Annotated

from fastapi import APIRouter, Depends

from snooker_backend.drills.repository import DrillRepository, get_drill_repository
from snooker_backend.drills.schemas import DrillCreate, DrillRead

router = APIRouter(prefix="/drills", tags=["drills"])
RepositoryDep = Annotated[DrillRepository, Depends(get_drill_repository)]


@router.get("")
def list_drills(repo: RepositoryDep) -> list[DrillRead]:
    return repo.list_all()


@router.post("", status_code=201)
def create_drill(drill: DrillCreate, repo: RepositoryDep) -> DrillRead:
    return repo.add(drill)
