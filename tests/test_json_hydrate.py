from typing import Any, Callable

import json_hydrate_benchmark
import pytest

JsonHydrate = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
pytestmark = pytest.mark.parametrize(
    "json_hydrate", [json_hydrate_benchmark.python, json_hydrate_benchmark.serde_json]
)


@pytest.fixture
def base() -> dict[str, str]:
    return {"a": "first", "b": "second", "c": "third"}


def test_equal_hydrate(json_hydrate: JsonHydrate, base: dict[str, str]) -> None:
    result = json_hydrate(base, base)
    assert result == base


def test_full_hydrate(json_hydrate: JsonHydrate, base: dict[str, str]) -> None:
    result = json_hydrate(base, {})
    assert result == base
