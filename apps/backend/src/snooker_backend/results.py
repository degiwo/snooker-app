import json


def get_results():
    with open("/app/data/results.jsonl", "r") as f:
        return [json.loads(line) for line in f]


def store_result(result: dict):
    with open("/app/data/results.jsonl", "a") as f:
        f.write(json.dumps(result) + "\n")
