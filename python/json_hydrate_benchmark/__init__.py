from typing import Any

from .json_hydrate_benchmark import serde_json


def python(item: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    return item


__all__ = ["python", "serde_json"]
