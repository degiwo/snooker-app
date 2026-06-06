import json


def get_results():
    with open("results.json", "r") as f:
        return json.load(f)


def store_result(result: dict):
    with open("results.json", "w") as f:
        json.dump(result, f)
