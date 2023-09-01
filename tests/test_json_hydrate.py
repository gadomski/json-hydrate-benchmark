import json
from pathlib import Path
from typing import Any, Callable, cast

import json_hydrate_benchmark
import pytest

JsonHydrate = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
pytestmark = pytest.mark.parametrize(
    "json_hydrate",
    [
        json_hydrate_benchmark.python,
        json_hydrate_benchmark.serde_json,
        json_hydrate_benchmark.pyo3,
    ],
)


@pytest.fixture
def base() -> dict[str, Any]:
    return {"a": "first", "b": "second", "c": "third"}


def load_json(path: Path) -> dict[str, Any]:
    with open(Path(__file__).parent / "data" / path) as f:
        return cast(dict[str, Any], json.load(f))


def test_equal_hydrate(json_hydrate: JsonHydrate, base: dict[str, Any]) -> None:
    result = json_hydrate(base, base)
    assert result == base


def test_full_hydrate(json_hydrate: JsonHydrate, base: dict[str, Any]) -> None:
    result = json_hydrate(base, {})
    assert result == base


def test_full_nested(json_hydrate: JsonHydrate, base: dict[str, Any]) -> None:
    base["c"] = {"d": "third"}
    result = json_hydrate(base, {})
    assert result == base


def test_nested_exta_keys(json_hydrate: JsonHydrate, base: dict[str, Any]) -> None:
    base["c"] = {"d": "third"}
    item = {"c": {"e": "fourth", "f": "fifth"}}
    result = json_hydrate(base, item)
    assert result == {
        "a": "first",
        "b": "second",
        "c": {"d": "third", "e": "fourth", "f": "fifth"},
    }


def test_list_of_dicts_extra_keys(json_hydrate: JsonHydrate) -> None:
    base = {"a": [{"b1": 1, "b2": 2}, "foo", {"c1": 1, "c2": 2}, "bar"]}
    item = {"a": [{"b3": 3}, "far", {"c3": 3}, "boo"]}
    result = json_hydrate(base, item)
    assert result == {
        "a": [
            {"b1": 1, "b2": 2, "b3": 3},
            "far",
            {"c1": 1, "c2": 2, "c3": 3},
            "boo",
        ],
    }


def test_marked_non_merged_fields(json_hydrate: JsonHydrate) -> None:
    base = {
        "a": "first",
        "b": "second",
        "c": {"d": "third", "e": "fourth"},
    }
    item = {"c": {"e": "𒍟※", "f": "fifth"}}
    result = json_hydrate(base, item)
    assert result == {
        "a": "first",
        "b": "second",
        "c": {"d": "third", "f": "fifth"},
    }


def test_landsat(json_hydrate: JsonHydrate) -> None:
    collection = load_json(Path("landsat-c2-l1.json"))
    base_item = json_hydrate_benchmark.base_item(collection)
    dehydrated = load_json(Path("dehydrated") / "LM04_L1GS_001001_19830527_02_T2.json")
    expected = load_json(Path("hydrated") / "LM04_L1GS_001001_19830527_02_T2.json")
    actual = json_hydrate(base_item, dehydrated)
    assert actual == expected
