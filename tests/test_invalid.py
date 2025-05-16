from pathlib import Path
import rfc3987_helpers as h
import json
import pytest


@pytest.fixture
def invalid_data():
    with open(Path("tests", "invalid.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def test_not_is_valid(invalid_data):
    for term, invalid_examples in invalid_data.items():
        for invalid_example in invalid_examples:
            actual = not h.is_valid(term=term, value=invalid_example["value"])
            print("")
            print(
                f"Testing {term} with {invalid_example['value']} : {invalid_example['reason']}"
            )
            assert (
                actual is True
            ), f"Failed term: {term} for '{invalid_example['value']}' : {invalid_example['reason']}"
