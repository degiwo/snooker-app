import json

from snooker_backend.models import Result


def get_results():
    with open("/app/data/results.jsonl", "r") as f:
        return [Result(**json.loads(line)) for line in f]


def store_result(result: Result):
    with open("/app/data/results.jsonl", "a") as f:
        f.write(result.model_dump_json() + "\n")
