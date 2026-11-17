from fastapi import APIRouter, FastAPI

from snooker_backend.drills.router import router as drills_router

app = FastAPI(docs_url="/api/docs", redoc_url=None, openapi_url="/api/openapi.json")
api = APIRouter(prefix="/api")


@api.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


api.include_router(drills_router)
app.include_router(api)
