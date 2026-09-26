import uvicorn
from fastapi import FastAPI

from snooker_backend.models import Result
from snooker_backend.results import get_results, store_result

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Worlds"}


@app.get("/results")
def read_results():
    return get_results()


@app.post("/results")
def create_result(result: Result):
    store_result(result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
