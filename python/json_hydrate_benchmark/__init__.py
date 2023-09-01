from typing import Any

from .json_hydrate_benchmark import serde_json


def python(base: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    return _hydrate_dict(base, item)


def _hydrate_dict(base: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    for key, value in base.items():
        if key in item:
            item[key] = _hydrate(value, item[key])
        else:
            item[key] = value
    return item


def _hydrate_list_or_tuple(
    base: list[Any] | tuple[Any, ...], item: list[Any] | tuple[Any, ...]
) -> list[Any] | tuple[Any, ...]:
    raise NotImplementedError


def _hydrate(base: Any, item: Any) -> Any:
    if isinstance(item, dict):
        if isinstance(base, dict):
            return _hydrate_dict(base, item)
        else:
            raise ValueError(f"base is not a dict: {type(base)}")
    elif isinstance(item, (list, tuple)):
        if isinstance(base, (list, tuple)):
            return _hydrate_list_or_tuple(base, item)
        else:
            raise ValueError(f"base is not a list or tuple: {type(base)}")
    else:
        return item


__all__ = ["python", "serde_json"]
