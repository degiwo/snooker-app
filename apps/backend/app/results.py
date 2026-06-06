import json


def store_result(result: dict):
    with open("results.json", "w") as f:
        json.dump(result, f)
