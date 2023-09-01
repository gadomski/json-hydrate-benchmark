from typing import Any, Callable

import json_hydrate_benchmark
import pytest

JsonHydrate = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
pytestmark = pytest.mark.parametrize(
    "json_hydrate", [json_hydrate_benchmark.python, json_hydrate_benchmark.serde_json]
)


@pytest.fixture
def base() -> dict[str, Any]:
    return {"a": "first", "b": "second", "c": "third"}


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
