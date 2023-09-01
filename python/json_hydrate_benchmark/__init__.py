from typing import Any

from .json_hydrate_benchmark import serde_json


def python(base: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    return base


__all__ = ["python", "serde_json"]
