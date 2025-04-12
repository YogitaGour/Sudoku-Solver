import json

def load_sample_board(path="data/sample_puzzle.json"):
    with open(path, 'r') as f:
        return json.load(f)
