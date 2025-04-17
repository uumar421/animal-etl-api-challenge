import pytest
from transform import transform_animal


def test_transform_animal():
    # test the transform logic to ensure expected transformations
    animal = {
        "id": "1",
        "name": "Tiger",
        "friends": "2,3",
        "born_at": 1609459200000,  # 2021-01-01T00:00:00Z
    }

    transformed = transform_animal(animal)
    assert transformed["friends"] == ["2", "3"]
    assert transformed["born_at"] == "2021-01-01T00:00:00+00:00"


def test_transform_empty_friends_and_null_born_at():
    raw = {"id": 2, "name": "Zebra", "friends": "", "born_at": None}
    expected = {"id": 2, "name": "Zebra", "friends": [], "born_at": None}
    assert transform_animal(raw) == expected
