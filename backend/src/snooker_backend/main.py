from fastapi import APIRouter, FastAPI

app = FastAPI()
api = APIRouter(prefix="/api")

app.include_router(api)


@api.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
